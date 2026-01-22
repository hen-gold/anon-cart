"""
Daily Digest Module

Generates daily digest reports with summaries of all changes.
"""

import logging
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)


class DailyDigest:
    """Generates daily digest reports."""
    
    def __init__(self, config):
        """Initialize with configuration."""
        self.config = config
        self.reports_dir = Path(config.get('reporting', {}).get('reports_dir', 'conductor/reports'))
        self.digest_time = config.get('reporting', {}).get('daily_digest_time', '18:00')
        self.send_slack_dm = config.get('reporting', {}).get('send_slack_dm', False)
        self.slack_config = config.get('slack', {})
        self.last_digest_date = None
        
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
    
    def _collect_code_changes(self):
        """Collect code changes from changelog or sync modules."""
        # TODO: Collect code changes from:
        # - CHANGELOG.md entries from last 24 hours
        # - Or from sync modules directly
        
        return {
            'bed': [],
            'fed': [],
            'total': 0
        }
    
    def _collect_jira_changes(self):
        """Collect Jira changes from last 24 hours."""
        # TODO: Collect Jira changes from:
        # - CHANGELOG.md entries
        # - Or from Jira sync module
        
        return {
            'status_changes': [],
            'new_issues': [],
            'priority_changes': [],
            'total': 0
        }
    
    def _collect_slack_summary(self):
        """Collect Slack communication summary."""
        # TODO: Collect from Slack sync module's stored summary
        
        return {
            'messages_count': 0,
            'decisions': [],
            'blockers': [],
            'status_updates': [],
            'dependencies': []
        }
    
    def _collect_context_updates(self):
        """Collect context file updates from last 24 hours."""
        # TODO: Collect from CHANGELOG.md or track updates
        
        return []
    
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
            if jira_changes['status_changes']:
                for change in jira_changes['status_changes'][:10]:
                    content += f"- {change.get('issue', 'Unknown')}: Status changed {change.get('old', '?')} → {change.get('new', '?')}\n"
            
            if jira_changes['new_issues']:
                content += f"- {len(jira_changes['new_issues'])} new issues created\n"
            
            if jira_changes['priority_changes']:
                for change in jira_changes['priority_changes'][:5]:
                    content += f"- {change.get('issue', 'Unknown')}: Priority changed {change.get('old', '?')} → {change.get('new', '?')}\n"
        else:
            content += "- No Jira updates detected\n"
        
        content += "\n"
        
        # Slack Communications section
        content += "## Slack Communications\n\n"
        if slack_summary['messages_count'] > 0:
            content += f"- Key discussions: {slack_summary['messages_count']} messages\n"
            if slack_summary['decisions']:
                content += f"- Decisions: {len(slack_summary['decisions'])} decision(s) discussed\n"
            if slack_summary['blockers']:
                content += f"- Blockers: {len(slack_summary['blockers'])} blocker(s) discussed\n"
            if slack_summary['status_updates']:
                content += f"- Status updates: {len(slack_summary['status_updates'])} update(s)\n"
        else:
            content += "- No significant Slack communications detected\n"
        
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
        Send daily digest via Slack DM.
        
        Args:
            digest_content: Full digest content (markdown)
            digest_file: Path to digest file
        """
        recipient_email = self.slack_config.get('digest_recipient_email', '')
        recipient_user_id = self.slack_config.get('digest_recipient_user_id', '')
        
        if not recipient_email and not recipient_user_id:
            logger.warning("No Slack recipient configured for daily digest DM")
            return
        
        try:
            # Format message for Slack
            # Slack has a message length limit, so we'll send a summary + link
            message = self._format_slack_message(digest_content, digest_file)
            
            # TODO: Use MCP-S Slack tools to send DM
            # This requires the agent to be run in an environment with MCP-S access
            # Example using MCP-S Slack tool:
            # 
            # from mcp_slack import send_message
            # 
            # if recipient_email:
            #     send_message(
            #         to=recipient_email,
            #         subject=f"Daily Digest - {datetime.now().strftime('%Y-%m-%d')}",
            #         body=message
            #     )
            
            # For now, log the message that would be sent
            logger.info(f"Daily digest ready to send via Slack DM to {recipient_email or recipient_user_id}")
            logger.debug(f"Message preview:\n{message[:500]}...")
            
            # Note: Actual sending requires MCP-S Slack integration
            # The agent should be run in an environment that has access to MCP-S tools
            # or the sending can be done via a separate script that uses MCP-S tools
            
        except Exception as e:
            logger.error(f"Error sending Slack DM: {e}")
    
    def _format_slack_message(self, digest_content, digest_file):
        """
        Format digest content for Slack message.
        
        Args:
            digest_content: Full digest markdown content
            digest_file: Path to digest file
            
        Returns:
            str: Formatted Slack message
        """
        # Extract summary section
        lines = digest_content.split('\n')
        summary_start = None
        for i, line in enumerate(lines):
            if line.strip() == '## Summary':
                summary_start = i
                break
        
        # Build message with summary and link to full digest
        message = f"📊 *Daily Digest - {datetime.now().strftime('%Y-%m-%d')}*\n\n"
        
        if summary_start:
            # Include summary section
            summary_lines = lines[summary_start+1:]
            for line in summary_lines:
                if line.strip() and not line.startswith('#'):
                    # Convert markdown to Slack format
                    slack_line = line.replace('- ', '• ')
                    message += f"{slack_line}\n"
        
        # Add link to full digest (if hosted or accessible)
        message += f"\n📄 Full digest saved to: `{digest_file}`\n"
        message += "\n_Generated by Context Synchronization Agent_"
        
        return message
