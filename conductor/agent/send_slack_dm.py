#!/usr/bin/env python3
"""
Slack DM Sender Helper

Sends daily digest file via Slack DM using Slack Web API (SLACK_BOT_TOKEN).
Can be run standalone: python send_slack_dm.py <digest_file_path> [config_path]
"""

import os
import sys
import logging
from pathlib import Path
import yaml

logger = logging.getLogger(__name__)


def send_digest_via_slack(digest_file_path, config_path=None):
    """
    Send daily digest file via Slack DM using Slack Web API.

    Args:
        digest_file_path: Path to the daily digest markdown file
        config_path: Path to config.yaml (optional)

    Returns:
        bool: True if sent (or formatted and token missing), False on error
    """
    if config_path is None:
        config_path = Path(__file__).parent / "config.yaml"

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    slack_config = config.get("slack", {})
    recipient_user_id = slack_config.get("digest_recipient_user_id", "")

    if not recipient_user_id:
        logger.error("No slack.digest_recipient_user_id configured")
        return False

    digest_file = Path(digest_file_path)
    if not digest_file.exists():
        logger.error("Digest file not found: %s", digest_file)
        return False

    with open(digest_file, "r") as f:
        digest_content = f.read()

    from reporting.daily_digest import DailyDigest
    digest_module = DailyDigest(config)
    message = digest_module._format_slack_message(digest_content, str(digest_file))
    if len(message) > 39000:
        message = message[:38900] + "\n\n... (truncated)"

    token = os.environ.get("SLACK_BOT_TOKEN")
    if not token:
        logger.warning("SLACK_BOT_TOKEN not set; message not sent")
        logger.info("Message prepared for %s (length %d)", recipient_user_id, len(message))
        return True

    try:
        from slack_sdk import WebClient
        client = WebClient(token=token)
        open_r = client.conversations_open(users=[recipient_user_id])
        if not open_r.get("ok"):
            logger.error("Slack conversations.open failed: %s", open_r)
            return False
        channel_id = open_r.get("channel", {}).get("id")
        if not channel_id:
            logger.error("No channel id from conversations.open")
            return False
        post_r = client.chat_postMessage(channel=channel_id, text=message)
        if not post_r.get("ok"):
            logger.error("Slack chat.postMessage failed: %s", post_r)
            return False
        logger.info("Digest sent via Slack DM to %s", recipient_user_id)
        return True
    except Exception as e:
        logger.error("Error sending Slack DM: %s", e)
        return False


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: send_slack_dm.py <digest_file_path> [config_path]")
        sys.exit(1)
    
    digest_path = sys.argv[1]
    config_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    send_digest_via_slack(digest_path, config_path)
