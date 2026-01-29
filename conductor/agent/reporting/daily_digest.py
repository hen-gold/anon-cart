"""
Daily Digest Module

Generates daily digest reports with summaries of all changes.
"""

import logging
from datetime import datetime, timedelta
from pathlib import Path
from reporting.id_resolver import IDResolver

logger = logging.getLogger(__name__)


class DailyDigest:
    """Generates daily digest reports."""

    def __init__(self, config, project_root=None):
        """Initialize with configuration and optional project root for path resolution."""
        self.config = config
        self.project_root = Path(project_root) if project_root else None
        rel = config.get("reporting", {}).get("reports_dir", "conductor/reports")
        self.reports_dir = (Path(project_root) / rel) if project_root else Path(rel)
        self.digest_time = config.get("reporting", {}).get("daily_digest_time", "18:00")
        self.send_slack_dm = config.get("reporting", {}).get("send_slack_dm", False)
        self.slack_config = config.get("slack", {})
        self.last_digest_date = None
        self.id_resolver = IDResolver(config)
        
    def should_generate(self):
        """
        Check if daily digest should be generated.
        
        Returns:
            bool: True if digest should be generated
        """
        now = datetime.now()
        current_time = now.strftime('%H:%M')
        
        # Check if it's time for daily digest
        if current_time >= self.digest_time:
            # Check if we already generated today
            today = now.date()
            if self.last_digest_date != today:
                return True
        
        return False
    
    def generate(self):
        """
        Generate daily digest.
        
        Returns:
            Path: Path to generated digest file
        """
        today = datetime.now().date()
        digest_file = self.reports_dir / f"daily-digest-{today.strftime('%Y-%m-%d')}.md"
        
        try:
            # Collect data from various sources
            code_changes = self._collect_code_changes()
            jira_changes = self._collect_jira_changes()
            slack_summary = self._collect_slack_summary()
            context_updates = self._collect_context_updates()
            
            # Generate digest content
            content = self._format_digest(
                today,
                code_changes,
                jira_changes,
                slack_summary,
                context_updates
            )
            
            # Resolve all IDs in the content before writing
            content = self.id_resolver.resolve_all_ids(content)
            
            # Write digest file
            self.reports_dir.mkdir(parents=True, exist_ok=True)
            with open(digest_file, 'w') as f:
                f.write(content)
            
            self.last_digest_date = today
            logger.info(f"Daily digest generated: {digest_file}")
            
            # Send Slack DM if configured
            if self.send_slack_dm:
                self._send_slack_dm(content, digest_file)
            
            return digest_file
            
        except Exception as e:
            logger.error(f"Error generating daily digest: {e}")
            return None
    
    def _get_recent_changelog_entries(self, days=1):
        """Get recent changelog entries (last N days) for digest data."""
        try:
            from reporting.changelog import Changelog
            changelog = Changelog(self.config, self.project_root)
            return changelog.get_recent_changes(days=days)
        except Exception as e:
            logger.debug("Could not load changelog for digest: %s", e)
            return []

    def _collect_code_changes(self):
        """Collect code changes from changelog (last 24 hours)."""
        entries = self._get_recent_changelog_entries(1)
        bed, fed = [], []
        for e in entries:
            if "Code" in (e.get("type") or "") or "Commit" in (e.get("type") or ""):
                repo = e.get("repository") or ""
                item = {"message": e.get("change", "")[:200], "sha": e.get("commit", "")[:7]}
                if "bed" in repo.lower() or "premium" in repo.lower():
                    bed.append(item)
                else:
                    fed.append(item)
        return {"bed": bed, "fed": fed, "total": len(bed) + len(fed)}

    def _collect_jira_changes(self):
        """Collect Jira changes from changelog (last 24 hours)."""
        entries = self._get_recent_changelog_entries(1)
        status_changes, new_issues, priority_changes, assignee_changes, created = [], [], [], [], []
        for e in entries:
            if (e.get("type") or "") != "Jira Update":
                continue
            issue = e.get("issue") or ""
            change = e.get("change")
            if isinstance(change, dict):
                if "status" in change:
                    status_changes.append({"issue": issue, "old": change["status"].get("old"), "new": change["status"].get("new")})
                if "priority" in change:
                    priority_changes.append({"issue": issue, "old": change["priority"].get("old"), "new": change["priority"].get("new")})
                if "assignee" in change:
                    assignee_changes.append({"issue": issue, "old": change["assignee"].get("old"), "new": change["assignee"].get("new")})
            if change == {"new": True} or (isinstance(change, dict) and change.get("new")):
                created.append({"issue": issue})
        total = len(status_changes) + len(new_issues) + len(priority_changes) + len(assignee_changes) + len(created)
        return {
            "status_changes": status_changes,
            "new_issues": new_issues,
            "priority_changes": priority_changes,
            "assignee_changes": assignee_changes,
            "created": created,
            "total": total,
        }

    def _collect_slack_summary(self):
        """Collect Slack summary from .state/slack_summary.json."""
        agent_dir = Path(__file__).parent.parent
        try:
            import state_manager
            data = state_manager.load_state("slack_summary", agent_dir)
        except ImportError:
            data = {}
        decisions = [{"decision": t, "context": "", "author": ""} for t in data.get("decisions", [])[:20]]
        blockers = data.get("blockers", [])[:20]
        status_updates = data.get("status_updates", [])[:20]
        action_items = [{"item": t, "owner": "", "context": ""} for t in data.get("action_items", [])[:20]]
        return {
            "messages_count": data.get("messages_count", 0),
            "decisions": decisions,
            "blockers": blockers,
            "status_updates": status_updates,
            "dependencies": data.get("dependencies", []),
            "action_items": action_items,
        }

    def _collect_context_updates(self):
        """Collect context file updates from changelog (last 24 hours)."""
        entries = self._get_recent_changelog_entries(1)
        updates = []
        for e in entries:
            cu = e.get("context_updated")
            if cu and cu not in updates:
                updates.append(cu)
        return updates
    
    def _format_digest(self, date, code_changes, jira_changes, slack_summary, context_updates):
        """
        Format daily digest content.
        
        Args:
            date: Date for digest
            code_changes: Code changes data
            jira_changes: Jira changes data
            slack_summary: Slack summary data
            context_updates: Context updates list
            
        Returns:
            str: Formatted digest content
        """
        content = f"# Daily Digest - {date.strftime('%Y-%m-%d')}\n\n"
        
        # Code Changes section
        content += "## Code Changes\n\n"
        if code_changes['total'] > 0:
            if code_changes['bed']:
                content += f"- [BED] {len(code_changes['bed'])} commits in premium-server/premium-cart\n"
                for commit in code_changes['bed'][:5]:  # Limit to 5
                    content += f"  - {commit.get('message', 'Unknown')} (commit {commit.get('sha', 'unknown')[:7]})\n"
            
            if code_changes['fed']:
                content += f"- [FED] {len(code_changes['fed'])} commits in premium-cart-anonymous\n"
                for commit in code_changes['fed'][:5]:
                    content += f"  - {commit.get('message', 'Unknown')} (commit {commit.get('sha', 'unknown')[:7]})\n"
        else:
            content += "- No code changes detected\n"
        
        content += "\n"
        
        # Jira Updates section
        content += "## Jira Updates\n\n"
        if jira_changes['total'] > 0:
            # New issues created
            if jira_changes.get('created'):
                for issue in jira_changes['created']:
                    assignee = issue.get('assignee', 'Unassigned')
                    # Resolve user ID if it's a Slack user ID
                    assignee = self.id_resolver.resolve_user_id(assignee) if assignee.startswith('U') else assignee
                    priority = issue.get('priority', '')
                    priority_str = f" ({priority})" if priority else ""
                    content += f"- **{issue.get('issue', 'Unknown')}**: Created - {issue.get('summary', 'No summary')} (Assignee: {assignee}{priority_str})\n"
            
            # Status changes
            if jira_changes.get('status_changes'):
                for change in jira_changes['status_changes'][:10]:
                    assignee = change.get('assignee', '')
                    # Resolve user ID if it's a Slack user ID
                    assignee = self.id_resolver.resolve_user_id(assignee) if assignee and assignee.startswith('U') else assignee
                    assignee_str = f" (Assignee: {assignee})" if assignee else ""
                    content += f"- **{change.get('issue', 'Unknown')}**: Status changed from `{change.get('old', '?')}` → `{change.get('new', '?')}`{assignee_str}\n"
            
            # Priority changes
            if jira_changes.get('priority_changes'):
                for change in jira_changes['priority_changes'][:5]:
                    content += f"- **{change.get('issue', 'Unknown')}**: Priority changed from `{change.get('old', '?')}` → `{change.get('new', '?')}`\n"
            
            # Assignee changes
            if jira_changes.get('assignee_changes'):
                for change in jira_changes['assignee_changes'][:5]:
                    old_assignee = change.get('old', 'Unassigned')
                    new_assignee = change.get('new', 'Unassigned')
                    # Resolve user IDs
                    old_assignee = self.id_resolver.resolve_user_id(old_assignee) if old_assignee.startswith('U') else old_assignee
                    new_assignee = self.id_resolver.resolve_user_id(new_assignee) if new_assignee.startswith('U') else new_assignee
                    content += f"- **{change.get('issue', 'Unknown')}**: Assignee changed from `{old_assignee}` → `{new_assignee}`\n"
        else:
            content += "- No Jira updates detected\n"
        
        content += "\n"
        
        # Slack Communications section
        content += "## Slack Communications\n\n"
        if slack_summary['messages_count'] > 0:
            channel_id = self.slack_config.get('channel_id', '')
            channel_name = self.id_resolver.resolve_channel_id(channel_id) if channel_id else '#anon-cart'
            content += f"- Key discussions: {slack_summary['messages_count']} messages in channel {channel_name}\n"
            
            # Decisions with actual decision text
            if slack_summary.get('decisions'):
                content += f"\n### Decisions ({len(slack_summary['decisions'])})\n\n"
                for decision in slack_summary['decisions']:
                    decision_text = decision.get('decision', 'No decision text')
                    author = decision.get('author', 'Unknown')
                    # Resolve user IDs in author field
                    author = self.id_resolver.resolve_user_id(author) if author.startswith('U') else author
                    context = decision.get('context', '')
                    context_str = f" ({context})" if context else ""
                    content += f"- **Decision**: {decision_text} (by {author}{context_str})\n"
            
            if slack_summary.get('blockers'):
                content += f"\n- Blockers: {len(slack_summary['blockers'])} blocker(s) discussed\n"
                # Resolve user IDs in blocker descriptions
                for blocker in slack_summary.get('blockers', [])[:5]:
                    blocker_text = blocker.get('text', '')
                    blocker_text = self.id_resolver.resolve_all_ids(blocker_text)
                    content += f"  - {blocker_text}\n"
            
            if slack_summary.get('status_updates'):
                content += f"- Status updates: {len(slack_summary['status_updates'])} update(s)\n"
        else:
            content += "- No significant Slack communications detected\n"
        
        content += "\n"
        
        # Open Action Items section
        content += "## Open Action Items\n\n"
        action_items = []
        
        # Collect action items from Slack
        if slack_summary.get('action_items'):
            action_items.extend(slack_summary['action_items'])
        
        # Collect action items from Jira (issues assigned but not done)
        if jira_changes.get('status_changes'):
            for change in jira_changes['status_changes']:
                if change.get('new') not in ['Done', 'Closed', 'Resolved']:
                    action_items.append({
                        'item': f"Work on {change.get('issue', 'Unknown')}: {change.get('summary', '')}",
                        'owner': change.get('assignee', 'Unassigned'),
                        'source': 'Jira'
                    })
        
        if action_items:
            for item in action_items[:15]:  # Limit to 15 items
                owner = item.get('owner', 'Unassigned')
                # Resolve user IDs (handle comma-separated list)
                if owner and ',' in owner:
                    owners = [o.strip() for o in owner.split(',')]
                    resolved_owners = []
                    for o in owners:
                        if o.startswith('U'):
                            resolved_owners.append(self.id_resolver.resolve_user_id(o))
                        else:
                            resolved_owners.append(o)
                    owner = ', '.join(resolved_owners)
                elif owner and owner.startswith('U'):
                    owner = self.id_resolver.resolve_user_id(owner)
                
                source = item.get('source', '')
                # Resolve channel IDs in source
                if source == 'Slack':
                    source = '#anon-cart'  # Use channel name instead
                source_str = f" [{source}]" if source else ""
                content += f"- **{item.get('item', 'Unknown action')}** (Owner: {owner}{source_str})\n"
        else:
            content += "- No open action items identified\n"
        
        content += "\n"
        
        # Context Updates section
        content += "## Context Updates\n\n"
        if context_updates:
            for update in context_updates:
                content += f"- Updated: {update}\n"
        else:
            content += "- No context updates\n"
        
        content += "\n"
        
        # Summary section
        total_changes = code_changes['total'] + jira_changes['total']
        blockers = len(slack_summary.get('blockers', []))
        decisions = len(slack_summary.get('decisions', []))
        
        content += "## Summary\n\n"
        content += f"- Total changes: {total_changes}\n"
        content += f"- Blockers: {blockers}\n"
        content += f"- Decisions: {decisions}\n"
        content += f"- Context files updated: {len(context_updates)}\n"
        
        return content
    
    def _send_slack_dm(self, digest_content, digest_file):
        """
        Send daily digest via Slack DM using Slack Web API.
        Uses conversations.open + chat.postMessage with SLACK_BOT_TOKEN.
        """
        import os
        recipient_user_id = self.slack_config.get("digest_recipient_user_id", "")
        if not recipient_user_id:
            logger.warning("No digest_recipient_user_id configured for daily digest DM")
            return
        try:
            message = self._format_slack_message(digest_content, digest_file)
            if len(message) > 39000:
                message = message[:38900] + "\n\n... (truncated; see full digest in repo)"
            token = os.environ.get("SLACK_BOT_TOKEN")
            if not token:
                logger.warning("SLACK_BOT_TOKEN not set; skipping Slack DM")
                return
            from slack_sdk import WebClient
            client = WebClient(token=token)
            open_r = client.conversations_open(users=[recipient_user_id])
            if not open_r.get("ok"):
                logger.error("Slack conversations.open failed: %s", open_r)
                return
            channel_id = open_r.get("channel", {}).get("id")
            if not channel_id:
                logger.error("No channel id from conversations.open")
                return
            post_r = client.chat_postMessage(channel=channel_id, text=message)
            if not post_r.get("ok"):
                logger.error("Slack chat.postMessage failed: %s", post_r)
                return
            logger.info("Daily digest sent via Slack DM to %s", recipient_user_id)
        except Exception as e:
            logger.error("Error sending Slack DM: %s", e)
    
    def _format_slack_message(self, digest_content, digest_file):
        """
        Format digest content for Slack message matching the specified format.
        
        Args:
            digest_content: Full digest markdown content
            digest_file: Path to digest file
            
        Returns:
            str: Formatted Slack message
        """
        lines = digest_content.split('\n')
        
        # Build message header
        message = f"*anon-cart Daily Status {datetime.now().strftime('%Y-%m-%d')}*\n\n"
        
        # Extract Jira Updates section
        jira_start = None
        jira_end = None
        for i, line in enumerate(lines):
            if line.strip() == '## Jira Updates':
                jira_start = i
            elif jira_start and line.startswith('## ') and jira_end is None:
                jira_end = i
                break
        
        if jira_start and jira_end:
            message += "*Jira Updates:*\n"
            current_item = None
            for i, line in enumerate(lines[jira_start+1:jira_end]):
                stripped = line.strip()
                if not stripped:
                    if current_item:
                        message += "\n"  # Add spacing after item
                        current_item = None
                    continue
                
                # Main Jira item (starts with - **DOM2-XXX**)
                if stripped.startswith('- **') and 'DOM2-' in stripped:
                    if current_item:
                        message += "\n"  # Add spacing between items
                    # Format: • *DOM2-6652*: Created - [BED] ... (Assignee: ...)
                    # Remove "**" and convert to Slack bold
                    line_clean = line.replace('- **', '• *').replace('**:', '*:')
                    # Ensure code blocks are preserved (statuses, priorities)
                    message += f"{line_clean}\n"
                    current_item = True
                # Sub-details (indented with -)
                elif stripped.startswith('- ') and current_item and not stripped.startswith('- **'):
                    # Convert to open circle bullet (indented) - use ◦ for sub-items
                    # Remove the leading "- " and add proper indentation
                    sub_text = stripped[2:]  # Remove "- "
                    message += f"  ◦ {sub_text}\n"
                elif stripped.startswith('##'):
                    break
        
        message += "\n"
        
        # Extract Decisions section (under Slack Communications)
        decisions_start = None
        decisions_end = None
        slack_section_start = None
        for i, line in enumerate(lines):
            if line.strip() == '## Slack Communications':
                slack_section_start = i
            elif slack_section_start and '### Decisions' in line:
                decisions_start = i
            elif decisions_start and (line.startswith('### ') or line.startswith('## ')) and decisions_end is None:
                decisions_end = i
                break
            elif decisions_start and i == len(lines) - 1:
                decisions_end = i + 1
        
        if decisions_start and decisions_end:
            message += "*Decisions:*\n"
            for line in lines[decisions_start+1:decisions_end]:
                stripped = line.strip()
                if not stripped:
                    continue
                
                # Format decision line - remove "**Decision**: " prefix
                if stripped.startswith('- **Decision**:'):
                    decision_text = stripped.replace('- **Decision**:', '').strip()
                    # Format: • Use `BrowserRouter` for ... (by FED team)
                    # Ensure code blocks are preserved for technical terms
                    message += f"• {decision_text}\n"
                # Skip sub-items (indented lines starting with -)
                elif stripped.startswith('- ') and not stripped.startswith('- **'):
                    # This is a sub-item under a decision, skip for main decisions list
                    continue
        
        message += "\n"
        
        # Extract Action Items section
        action_start = None
        action_end = None
        for i, line in enumerate(lines):
            if line.strip() == '## Open Action Items':
                action_start = i
            elif action_start and line.startswith('## ') and action_end is None:
                action_end = i
                break
            elif action_start and i == len(lines) - 1:
                action_end = i + 1
        
        if action_start and action_end:
            message += "*Open Action Items:*\n"
            for line in lines[action_start+1:action_end]:
                stripped = line.strip()
                if not stripped or not stripped.startswith('-'):
                    continue
                
                # Format: • *Action item* (Owner: ...) [#anon-cart]
                action_line = line.replace('- **', '• *').replace('**', '*')
                message += f"{action_line}\n"
            message += "\n"
        
        # Summary section
        summary_start = None
        for i, line in enumerate(lines):
            if line.strip() == '## Summary':
                summary_start = i
                break
        
        if summary_start:
            message += "*Summary:*\n"
            for line in lines[summary_start+1:]:
                stripped = line.strip()
                if not stripped or not stripped.startswith('-'):
                    continue
                summary_line = line.replace('- ', '• ')
                message += f"{summary_line}\n"
        
        # Add link to full digest
        message += f"\n📄 Full digest: `{digest_file}`\n"
        message += "\n_Generated by Context Synchronization Agent_"
        
        # Resolve all IDs in the message
        message = self.id_resolver.resolve_all_ids(message)
        
        return message
