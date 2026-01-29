"""
Jira Synchronization Module

Monitors Jira ticket updates and synchronizes with context documents.
Uses Jira REST API (jira library) with credentials from environment.
"""

import logging
import os
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# Map Jira status names to our section names (Done, In Progress, PR Pending, Backlog)
STATUS_MAP = {
    "done": "Done",
    "closed": "Done",
    "in progress": "In Progress",
    "code review": "PR Pending",
    "pr pending": "PR Pending",
    "review": "PR Pending",
    "to do": "Backlog",
    "open": "Backlog",
    "backlog": "Backlog",
}


def _normalize_status(jira_status_name):
    """Map Jira status to our status bucket."""
    if not jira_status_name:
        return "Backlog"
    key = jira_status_name.lower().strip()
    return STATUS_MAP.get(key, "Backlog")


def _get_client(base_url, email, api_token):
    """Create Jira client; returns None if credentials missing."""
    try:
        from jira import JIRA
    except ImportError:
        logger.warning("jira package not installed; run pip install jira")
        return None
    if not email or not api_token:
        logger.debug("Jira credentials not set (JIRA_EMAIL, JIRA_API_TOKEN)")
        return None
    return JIRA(server=base_url, basic_auth=(email, api_token))


def _issue_to_dict(issue):
    """Convert Jira issue to a simple dict for state and markdown."""
    summary = getattr(issue.fields, "summary", "") or ""
    status_name = getattr(issue.fields.status, "name", None) or "Unknown"
    priority_name = getattr(issue.fields.priority, "name", None) if getattr(issue.fields, "priority", None) else "Unassigned"
    assignee = "Unassigned"
    if getattr(issue.fields, "assignee", None):
        assignee = getattr(issue.fields.assignee, "displayName", None) or str(issue.fields.assignee)
    story_points = 0
    try:
        sp = getattr(issue.fields, "customfield_10016", None) or getattr(issue.fields, "customfield_10020", None)
        if sp is not None:
            story_points = int(sp)
    except (TypeError, ValueError):
        pass
    return {
        "key": issue.key,
        "summary": summary,
        "status": _normalize_status(status_name),
        "priority": priority_name or "Unassigned",
        "assignee": assignee,
        "story_points": story_points,
        "raw_status": status_name,
    }


class JiraSync:
    """Synchronizes Jira ticket updates."""

    def __init__(self, config, project_root=None):
        """Initialize with configuration and optional project root for resolving paths."""
        self.config = config
        self.jira_config = config.get("jira", {})
        self.context_files = config.get("sync", {}).get("context_files", {})
        self.project_root = Path(project_root) if project_root else None
        self._agent_dir = Path(__file__).parent.parent

    def _resolve_path(self, relative_path: str) -> Path:
        """Resolve a config path (e.g. conductor/tracks.md) against project root or cwd."""
        if self.project_root:
            return self.project_root / relative_path
        return Path(relative_path)

    def sync(self):
        """
        Sync Jira ticket updates.

        Returns:
            list: List of change entries for changelog
        """
        changes = []

        try:
            epic_changes = self._sync_epic()
            changes.extend(epic_changes)

            child_changes = self._sync_child_issues()
            changes.extend(child_changes)

            return changes

        except Exception as e:
            logger.error(f"Error syncing Jira: {e}")
            return changes

    def _sync_epic(self):
        """Sync epic updates (minimal: we focus on child issues)."""
        epic_key = self.jira_config.get("epic_key")
        if not epic_key:
            return []
        logger.info(f"Syncing epic {epic_key}...")
        return []

    def _sync_child_issues(self):
        """Sync child issue updates via Jira REST API; update context files and return change list."""
        epic_key = self.jira_config.get("epic_key")
        base_url = os.environ.get("JIRA_BASE_URL") or self.jira_config.get("base_url", "")
        email = os.environ.get("JIRA_EMAIL", "")
        api_token = os.environ.get("JIRA_API_TOKEN", "")

        if not base_url or not epic_key:
            logger.warning("Jira base_url or epic_key not configured")
            return []

        client = _get_client(base_url, email, api_token)
        if not client:
            return []

        try:
            import state_manager
            last_state = state_manager.load_state("jira_last_state", self._agent_dir)
        except ImportError:
            last_state = {}

        jql = f'parent = {epic_key} ORDER BY rank'
        logger.info(f"Fetching child issues: {jql}")
        try:
            issues = client.search_issues(jql, maxResults=False)
        except Exception as e:
            logger.error(f"Jira search failed: {e}")
            return []

        current_issues = []
        change_entries = []

        for issue in issues:
            d = _issue_to_dict(issue)
            current_issues.append(d)
            last_d = last_state.get(issue.key, {})
            diff = self._detect_issue_changes(d, last_d)
            if diff:
                ts = datetime.now().strftime("%Y-%m-%d %H:%M")
                change_entries.append({
                    "type": "Jira Update",
                    "issue": issue.key,
                    "timestamp": ts,
                    "change": diff,
                    "context_updated": "tracks.md, child-issues.md",
                })
                if last_d:
                    self._update_track_directory(issue.key, d)

        # Build new state key -> dict for next run
        new_state = {d["key"]: {k: d[k] for k in ("status", "assignee", "priority", "summary")} for d in current_issues}

        try:
            import state_manager
            state_manager.save_state("jira_last_state", new_state, self._agent_dir)
        except ImportError:
            pass

        # Update context files from full issue list
        by_status = {}
        for d in current_issues:
            s = d["status"]
            by_status.setdefault(s, []).append(d)
        self._update_tracks_md(by_status, epic_key)
        self._update_child_issues_md(by_status)

        # Ensure track dirs exist for all issues and metadata is written
        tracks_base = self._resolve_path("conductor/tracks")
        for d in current_issues:
            key = d["key"]
            track_dir = tracks_base / key
            if not track_dir.exists():
                track_dir.mkdir(parents=True, exist_ok=True)
            self._write_metadata_json(track_dir, d)

        return change_entries

    def _detect_issue_changes(self, current_issue, last_issue):
        """Detect changes between current and last known issue state."""
        if not last_issue:
            return {"new": True}
        changes = {}
        if current_issue.get("status") != last_issue.get("status"):
            changes["status"] = {"old": last_issue.get("status"), "new": current_issue.get("status")}
        if current_issue.get("assignee") != last_issue.get("assignee"):
            changes["assignee"] = {"old": last_issue.get("assignee"), "new": current_issue.get("assignee")}
        if current_issue.get("priority") != last_issue.get("priority"):
            changes["priority"] = {"old": last_issue.get("priority"), "new": current_issue.get("priority")}
        return changes

    def _update_tracks_md(self, issues_by_status, epic_key):
        """Write tracks.md from issues grouped by status."""
        tracks_path = self._resolve_path(self.context_files.get("tracks", "conductor/tracks.md"))
        tracks_path.parent.mkdir(parents=True, exist_ok=True)

        done = issues_by_status.get("Done", [])
        in_progress = issues_by_status.get("In Progress", [])
        pr_pending = issues_by_status.get("PR Pending", [])
        backlog = issues_by_status.get("Backlog", [])
        total = len(done) + len(in_progress) + len(pr_pending) + len(backlog)
        pct = (100 * len(done) // total) if total else 0

        lines = [
            "# Tracks Registry",
            "",
            "Registry of all work units (tracks) for the SF Purchase Flow (DOM2-6162) epic.",
            "",
            "## Overview",
            "",
            f"- **Total Tracks**: {total}",
            f"- **Progress**: {pct}% ({len(done)} done, {len(in_progress)} in progress, {len(pr_pending)} PR pending, {len(backlog)} backlog)",
            f"- **Epic**: {epic_key} - SF Purchase Flow",
            "- **Parent Initiative**: DOM2-5958 (Domains Storefront Track)",
            "",
            "## Track Status",
            "",
        ]

        def section(title, icon, items):
            out = [f"### {icon} {title} ({len(items)} tracks)", ""]
            for i, d in enumerate(items, 1):
                out.append(f"{i}. **{d['key']}** - {d['summary']}")
                out.append(f"   - Priority: {d['priority']} | Story Points: {d['story_points']}")
                out.append(f"   - Assignee: {d['assignee']}")
                out.append(f"   - Status: {d['status']}")
                out.append("")
            return out

        lines.extend(section("Done", "✅", done))
        lines.extend(section("In Progress", "🔄", in_progress))
        lines.extend(section("PR Pending", "⏳", pr_pending))
        lines.extend(section("Backlog", "📋", backlog))

        lines.append("## Statistics")
        lines.append("")
        lines.append("- **Done**: %d tracks" % len(done))
        lines.append("- **In Progress**: %d tracks" % len(in_progress))
        lines.append("- **PR Pending**: %d tracks" % len(pr_pending))
        lines.append("- **Backlog**: %d tracks" % len(backlog))
        lines.append("- **Total**: %d tracks" % total)

        with open(tracks_path, "w") as f:
            f.write("\n".join(lines))
        logger.info(f"Wrote {tracks_path}")

    def _update_child_issues_md(self, issues_by_status):
        """Write child-issues.md from issues grouped by status."""
        child_path = self._resolve_path(self.context_files.get("child_issues", "conductor/sources/jira/child-issues.md"))
        child_path.parent.mkdir(parents=True, exist_ok=True)

        done = issues_by_status.get("Done", [])
        in_progress = issues_by_status.get("In Progress", [])
        pr_pending = issues_by_status.get("PR Pending", [])
        backlog = issues_by_status.get("Backlog", [])
        total = len(done) + len(in_progress) + len(pr_pending) + len(backlog)
        pct = (100 * len(done) // total) if total else 0

        lines = [
            "# DOM2-6162 Child Issues",
            "",
            "Complete list of all child issues for the SF Purchase Flow epic.",
            "",
            "## Summary",
            "",
            f"- **Total Issues**: {total}",
            f"- **Done**: {len(done)} ({pct}%)",
            f"- **In Progress**: {len(in_progress)}",
            f"- **PR Pending**: {len(pr_pending)}",
            f"- **Backlog**: {len(backlog)}",
            "",
            "## Complete Issue List",
            "",
        ]

        def section(title, items):
            out = [f"### {title} ({len(items)})", ""]
            for i, d in enumerate(items, 1):
                out.append(f"{i}. **{d['key']}** - {d['summary']}")
                out.append(f"   - Priority: {d['priority']} | Story Points: {d['story_points']} | Assignee: {d['assignee']}")
                out.append("")
            return out

        lines.extend(section("Done", done))
        lines.extend(section("In Progress", in_progress))
        lines.extend(section("PR Pending", pr_pending))
        lines.extend(section("Backlog", backlog))

        with open(child_path, "w") as f:
            f.write("\n".join(lines))
        logger.info(f"Wrote {child_path}")

    def _update_track_directory(self, issue_key, issue_dict):
        """Update or create track directory metadata for an issue."""
        tracks_base = self._resolve_path("conductor/tracks")
        track_dir = tracks_base / issue_key
        track_dir.mkdir(parents=True, exist_ok=True)
        self._write_metadata_json(track_dir, issue_dict)

    def _write_metadata_json(self, track_dir, issue_dict):
        """Write metadata.json for a track."""
        import json
        meta = {
            "key": issue_dict["key"],
            "summary": issue_dict["summary"],
            "status": issue_dict["status"],
            "priority": issue_dict["priority"],
            "storyPoints": issue_dict["story_points"],
            "assignee": issue_dict["assignee"],
            "epic": self.jira_config.get("epic_key", "DOM2-6162"),
            "type": "Story",
            "team": "Unknown",
            "updated": datetime.now().strftime("%Y-%m-%d"),
        }
        path = track_dir / "metadata.json"
        with open(path, "w") as f:
            json.dump(meta, f, indent=2)
        logger.debug(f"Wrote {path}")
