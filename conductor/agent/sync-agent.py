#!/usr/bin/env python3
"""
Context Synchronization Agent

Monitors changes across repositories, Jira, and Slack, automatically updates
relevant context documents, and generates daily digests and a live changelog.
"""

import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path
import yaml

# Add agent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from sync.code_sync import CodeSync
from sync.jira_sync import JiraSync
from sync.docs_sync import DocsSync
from sync.slack_sync import SlackSync
from reporting.daily_digest import DailyDigest
from reporting.changelog import Changelog

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SyncAgent:
    """Main context synchronization agent."""
    
    def __init__(self, config_path=None):
        """Initialize agent with configuration."""
        if config_path is None:
            config_path = Path(__file__).parent / 'config.yaml'
        
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Initialize sync modules
        self.code_sync = CodeSync(self.config)
        self.jira_sync = JiraSync(self.config)
        self.docs_sync = DocsSync(self.config)
        self.slack_sync = SlackSync(self.config)
        
        # Initialize reporting modules
        self.changelog = Changelog(self.config)
        self.daily_digest = DailyDigest(self.config)
        
        # Track changes for reporting
        self.changes = []
    
    def sync_code_commits(self):
        """Sync code commits from monitored repositories."""
        logger.info("Syncing code commits...")
        try:
            changes = self.code_sync.sync()
            if changes:
                self.changes.extend(changes)
                logger.info(f"Code sync completed: {len(changes)} changes detected")
            return changes
        except Exception as e:
            logger.error(f"Error syncing code commits: {e}")
            return []
    
    def sync_jira_updates(self):
        """Sync Jira ticket updates."""
        logger.info("Syncing Jira updates...")
        try:
            changes = self.jira_sync.sync()
            if changes:
                self.changes.extend(changes)
                logger.info(f"Jira sync completed: {len(changes)} changes detected")
            return changes
        except Exception as e:
            logger.error(f"Error syncing Jira updates: {e}")
            return []
    
    def sync_document_changes(self):
        """Sync document changes from Google Docs/Sheets."""
        logger.info("Syncing document changes...")
        try:
            changes = self.docs_sync.sync()
            if changes:
                self.changes.extend(changes)
                logger.info(f"Document sync completed: {len(changes)} changes detected")
            return changes
        except Exception as e:
            logger.error(f"Error syncing documents: {e}")
            return []
    
    def sync_slack_communications(self):
        """Sync and summarize Slack communications."""
        logger.info("Syncing Slack communications...")
        try:
            changes = self.slack_sync.sync()
            if changes:
                self.changes.extend(changes)
                logger.info(f"Slack sync completed: {len(changes)} changes detected")
            return changes
        except Exception as e:
            logger.error(f"Error syncing Slack: {e}")
            return []
    
    def update_changelog(self, changes):
        """Update the live changelog with new changes."""
        if changes:
            logger.info(f"Updating changelog with {len(changes)} entries...")
            self.changelog.add_entries(changes)
    
    def generate_daily_digest(self, force=False):
        """Generate daily digest if it's time or forced."""
        if force or self.daily_digest.should_generate():
            logger.info("Generating daily digest...")
            digest = self.daily_digest.generate()
            if digest:
                logger.info(f"Daily digest generated: {digest}")
            return digest
        return None
    
    def run_full_sync(self):
        """Run full synchronization across all sources."""
        logger.info("Starting full context synchronization...")
        
        # Sync all sources
        code_changes = self.sync_code_commits()
        jira_changes = self.sync_jira_updates()
        doc_changes = self.sync_document_changes()
        slack_changes = self.sync_slack_communications()
        
        # Update changelog
        all_changes = code_changes + jira_changes + doc_changes + slack_changes
        if all_changes:
            self.update_changelog(all_changes)
        
        # Generate daily digest if needed
        self.generate_daily_digest()
        
        logger.info(f"Full sync completed: {len(all_changes)} total changes")
        return all_changes
    
    def run_scheduled_sync(self):
        """Run scheduled synchronization (daily check)."""
        logger.info("Running scheduled synchronization...")
        
        # Run full sync
        changes = self.run_full_sync()
        
        # Always generate daily digest for scheduled runs
        self.generate_daily_digest(force=True)
        
        return changes


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Context Synchronization Agent')
    parser.add_argument(
        '--mode',
        choices=['full', 'code', 'jira', 'docs', 'slack', 'scheduled', 'digest'],
        default='full',
        help='Sync mode to run'
    )
    parser.add_argument(
        '--config',
        type=str,
        help='Path to config file (default: config.yaml in agent directory)'
    )
    parser.add_argument(
        '--force-digest',
        action='store_true',
        help='Force generation of daily digest'
    )
    
    args = parser.parse_args()
    
    # Initialize agent
    agent = SyncAgent(args.config)
    
    # Run based on mode
    if args.mode == 'full':
        changes = agent.run_full_sync()
    elif args.mode == 'code':
        changes = agent.sync_code_commits()
        agent.update_changelog(changes)
    elif args.mode == 'jira':
        changes = agent.sync_jira_updates()
        agent.update_changelog(changes)
    elif args.mode == 'docs':
        changes = agent.sync_document_changes()
        agent.update_changelog(changes)
    elif args.mode == 'slack':
        changes = agent.sync_slack_communications()
        agent.update_changelog(changes)
    elif args.mode == 'scheduled':
        changes = agent.run_scheduled_sync()
    elif args.mode == 'digest':
        agent.generate_daily_digest(force=True)
        changes = []
    
    if args.force_digest:
        agent.generate_daily_digest(force=True)
    
    logger.info(f"Agent execution completed: {len(changes)} changes processed")
    return 0 if changes or args.mode == 'digest' else 1


if __name__ == '__main__':
    sys.exit(main())
