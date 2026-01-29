"""
Slack Synchronization Module

Monitors Slack channel communications and extracts key information.
Uses Slack Web API (slack-sdk) with SLACK_BOT_TOKEN.
"""

import logging
import os
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)


def _get_client():
    """Create Slack WebClient; returns None if token missing."""
    token = os.environ.get("SLACK_BOT_TOKEN")
    if not token:
        logger.debug("SLACK_BOT_TOKEN not set")
        return None
    try:
        from slack_sdk import WebClient
        return WebClient(token=token)
    except ImportError:
        logger.warning("slack_sdk not installed; run pip install slack-sdk")
        return None


class SlackSync:
    """Synchronizes Slack channel communications."""

    def __init__(self, config, project_root=None):
        """Initialize with configuration and optional project root."""
        self.config = config
        self.project_root = Path(project_root) if project_root else None
        self.slack_config = config.get("slack", {})
        self.context_files = config.get("sync", {}).get("context_files", {})
        self._agent_dir = Path(__file__).parent.parent

    def _resolve_path(self, relative_path: str) -> Path:
        if self.project_root:
            return self.project_root / relative_path
        return Path(relative_path)

    def sync(self):
        """
        Sync Slack communications.

        Returns:
            list: List of change entries for changelog
        """
        changes = []

        try:
            messages = self._read_recent_messages()
            key_info = self._extract_key_information(messages)

            if key_info.get("decisions"):
                decision_changes = self._update_decisions(key_info["decisions"])
                changes.extend(decision_changes)

            self._store_slack_summary(key_info)
            return changes

        except Exception as e:
            logger.error(f"Error syncing Slack: {e}")
            return changes

    def _read_recent_messages(self, hours=24):
        """Read recent messages from Slack channel via Web API."""
        channel_id = self.slack_config.get("channel_id")
        if not channel_id:
            logger.warning("No Slack channel ID configured")
            return []

        client = _get_client()
        if not client:
            return []

        try:
            import state_manager
            state = state_manager.load_state("slack_last_ts", self._agent_dir)
            oldest_ts = state.get("last_ts")
            if not oldest_ts:
                # First run: last 24 hours
                oldest_ts = (datetime.now() - timedelta(hours=hours)).timestamp()
        except ImportError:
            oldest_ts = (datetime.now() - timedelta(hours=hours)).timestamp()

        try:
            result = client.conversations_history(
                channel=channel_id,
                oldest=str(oldest_ts),
                limit=200,
            )
        except Exception as e:
            logger.error(f"Slack conversations.history failed: {e}")
            return []

        messages = []
        latest_ts = None
        for m in result.get("messages", []):
            if m.get("type") == "message" and m.get("subtype") != "channel_join":
                messages.append(m)
                try:
                    ts = float(m.get("ts", 0) or 0)
                    if latest_ts is None or ts > latest_ts:
                        latest_ts = ts
                except (TypeError, ValueError):
                    pass

        if latest_ts is not None:
            try:
                import state_manager
                state_manager.save_state("slack_last_ts", {"last_ts": latest_ts}, self._agent_dir)
            except ImportError:
                pass

        logger.info(f"Read {len(messages)} messages from Slack channel {channel_id}")
        return messages

    def _extract_key_information(self, messages):
        """Extract decisions, blockers, status updates from messages."""
        key_info = {
            "decisions": [],
            "blockers": [],
            "status_updates": [],
            "dependencies": [],
            "action_items": [],
        }
        for m in messages:
            text = (m.get("text") or "").lower()
            user = m.get("user", "unknown")
            ts = m.get("ts", "")
            entry = {"text": m.get("text", ""), "user": user, "ts": ts}
            if any(k in text for k in ["decided", "decision", "we will", "going with"]):
                key_info["decisions"].append(entry)
            if any(k in text for k in ["blocked", "blocker", "blocking", "cannot proceed"]):
                key_info["blockers"].append(entry)
            if any(k in text for k in ["status", "progress", "completed", "done", "finished"]):
                key_info["status_updates"].append(entry)
            if any(k in text for k in ["action item", "action items", "todo", "assign"]):
                key_info["action_items"].append(entry)
        return key_info

    def _update_decisions(self, decision_messages):
        """Append decisions to decisions.md and return change entries."""
        rel = self.context_files.get("decisions", "conductor/decisions.md")
        decisions_path = self._resolve_path(rel)
        decisions_path.parent.mkdir(parents=True, exist_ok=True)

        changes = []
        for d in decision_messages:
            text = d.get("text", "")[:500]
            ts = datetime.now().strftime("%Y-%m-%d %H:%M")
            entry = f"\n### {ts} - Decision (from Slack)\n- **Source**: user {d.get('user', 'unknown')}\n- **Decision**: {text}\n"
            try:
                with open(decisions_path, "a") as f:
                    f.write(entry)
                changes.append({
                    "type": "Slack Decision",
                    "timestamp": ts,
                    "change": text[:200],
                    "context_updated": str(decisions_path.name),
                })
            except IOError as e:
                logger.warning(f"Could not append to decisions.md: {e}")
        if changes:
            logger.info(f"Appended {len(changes)} decisions to {decisions_path}")
        return changes

    def _store_slack_summary(self, key_info):
        """Store Slack summary in .state/slack_summary.json for daily digest."""
        summary = {
            "date": datetime.now().isoformat(),
            "messages_count": len(key_info.get("decisions", [])) + len(key_info.get("blockers", [])) + len(key_info.get("status_updates", [])),
            "decisions": [d.get("text", "")[:300] for d in key_info.get("decisions", [])],
            "blockers": [b.get("text", "")[:300] for b in key_info.get("blockers", [])],
            "status_updates": [s.get("text", "")[:300] for s in key_info.get("status_updates", [])],
            "action_items": [a.get("text", "")[:300] for a in key_info.get("action_items", [])],
        }
        try:
            import state_manager
            state_manager.save_state("slack_summary", summary, self._agent_dir)
        except ImportError:
            pass
        logger.info(f"Stored Slack summary: {len(summary['decisions'])} decisions, {len(summary['blockers'])} blockers")
