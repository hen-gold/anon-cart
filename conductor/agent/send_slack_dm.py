#!/usr/bin/env python3
"""
Slack DM Sender Helper

Helper script to send daily digest via Slack DM using MCP-S tools.
This can be called from the agent or run independently.
"""

import sys
import logging
from pathlib import Path
import yaml

logger = logging.getLogger(__name__)


def send_digest_via_slack(digest_file_path, config_path=None):
    """
    Send daily digest file via Slack DM.
    
    This function is designed to be called with MCP-S Slack tools available.
    In a Cursor/MCP environment, this can use the MCP-S Slack send-message tool.
    
    Args:
        digest_file_path: Path to the daily digest markdown file
        config_path: Path to config.yaml (optional)
    """
    if config_path is None:
        config_path = Path(__file__).parent / 'config.yaml'
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    slack_config = config.get('slack', {})
    recipient_email = slack_config.get('digest_recipient_email', '')
    recipient_user_id = slack_config.get('digest_recipient_user_id', '')
    
    if not recipient_email and not recipient_user_id:
        logger.error("No Slack recipient configured")
        return False
    
    # Read digest file
    digest_file = Path(digest_file_path)
    if not digest_file.exists():
        logger.error(f"Digest file not found: {digest_file}")
        return False
    
    with open(digest_file, 'r') as f:
        digest_content = f.read()
    
    # Format for Slack
    from reporting.daily_digest import DailyDigest
    digest_module = DailyDigest(config)
    message = digest_module._format_slack_message(digest_content, str(digest_file))
    
    # Note: Actual sending requires MCP-S Slack tool access
    # In Cursor, this would be done via:
    # mcp_MCP-S-SLACK_slack__slack_send-message
    # 
    # Example usage in Cursor/MCP environment:
    # - Use the MCP-S Slack send-message tool
    # - Pass recipient_email or recipient_user_id
    # - Pass message as body
    
    logger.info(f"Digest ready to send to {recipient_email or recipient_user_id}")
    logger.info(f"Message:\n{message}")
    
    return True


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: send_slack_dm.py <digest_file_path> [config_path]")
        sys.exit(1)
    
    digest_path = sys.argv[1]
    config_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    send_digest_via_slack(digest_path, config_path)
