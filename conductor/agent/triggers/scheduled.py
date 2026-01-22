"""
Scheduled Trigger Handler

Handles scheduled/scheduled synchronization runs.
"""

import logging
import schedule
import time
from datetime import datetime

logger = logging.getLogger(__name__)


class ScheduledTrigger:
    """Manages scheduled synchronization triggers."""
    
    def __init__(self, agent, config):
        """
        Initialize scheduled trigger.
        
        Args:
            agent: SyncAgent instance
            config: Configuration dict
        """
        self.agent = agent
        self.config = config
        self.reporting_config = config.get('reporting', {})
        self.sync_config = config.get('sync', {})
        
    def setup_schedules(self):
        """Set up all scheduled tasks."""
        # Daily digest schedule
        digest_time = self.reporting_config.get('daily_digest_time', '18:00')
        schedule.every().day.at(digest_time).do(self._run_daily_sync)
        
        # Periodic sync schedules
        intervals = self.sync_config.get('check_intervals', {})
        
        # Code commits check
        if 'code_commits' in self.sync_config.get('enabled_triggers', []):
            code_interval = intervals.get('code_commits', 3600)
            schedule.every(code_interval).seconds.do(self._run_code_sync)
        
        # Jira updates check
        if 'jira_updates' in self.sync_config.get('enabled_triggers', []):
            jira_interval = intervals.get('jira_updates', 1800)
            schedule.every(jira_interval).seconds.do(self._run_jira_sync)
        
        # Document changes check
        if 'doc_changes' in self.sync_config.get('enabled_triggers', []):
            doc_interval = intervals.get('doc_changes', 3600)
            schedule.every(doc_interval).seconds.do(self._run_docs_sync)
        
        logger.info("Scheduled tasks configured")
    
    def run(self):
        """Run scheduled tasks continuously."""
        logger.info("Starting scheduled trigger loop...")
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def _run_daily_sync(self):
        """Run daily scheduled sync."""
        logger.info("Running daily scheduled sync...")
        try:
            self.agent.run_scheduled_sync()
        except Exception as e:
            logger.error(f"Error in daily sync: {e}")
    
    def _run_code_sync(self):
        """Run code sync check."""
        logger.debug("Running scheduled code sync check...")
        try:
            self.agent.sync_code_commits()
        except Exception as e:
            logger.error(f"Error in code sync: {e}")
    
    def _run_jira_sync(self):
        """Run Jira sync check."""
        logger.debug("Running scheduled Jira sync check...")
        try:
            self.agent.sync_jira_updates()
        except Exception as e:
            logger.error(f"Error in Jira sync: {e}")
    
    def _run_docs_sync(self):
        """Run document sync check."""
        logger.debug("Running scheduled document sync check...")
        try:
            self.agent.sync_document_changes()
        except Exception as e:
            logger.error(f"Error in document sync: {e}")


def run_scheduled_agent(config_path=None):
    """
    Run agent with scheduled triggers.
    
    Args:
        config_path: Path to config file
    """
    from sync_agent import SyncAgent
    
    agent = SyncAgent(config_path)
    trigger = ScheduledTrigger(agent, agent.config)
    
    trigger.setup_schedules()
    trigger.run()


if __name__ == '__main__':
    import sys
    config_path = sys.argv[1] if len(sys.argv) > 1 else None
    run_scheduled_agent(config_path)
