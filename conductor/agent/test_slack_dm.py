#!/usr/bin/env python3
"""
Test Slack DM Sending

Quick test script to verify Slack DM delivery works.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add agent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from reporting.daily_digest import DailyDigest
import yaml

def main():
    """Test Slack DM sending."""
    config_path = Path(__file__).parent / 'config.yaml'
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Create a test digest
    digest = DailyDigest(config)
    
    # Create test content
    date_str = datetime.now().strftime('%Y-%m-%d')
    test_content = "# Daily Digest - " + date_str + "\n\n"
    test_content += "## Test Message\n\n"
    test_content += "This is a test message to verify Slack DM delivery is working correctly.\n\n"
    test_content += "## Code Changes\n\n"
    test_content += "- No code changes detected (test mode)\n\n"
    test_content += "## Jira Updates\n\n"
    test_content += "- No Jira updates detected (test mode)\n\n"
    test_content += "## Slack Communications\n\n"
    test_content += "- Test message sent successfully\n\n"
    test_content += "## Summary\n\n"
    test_content += "- Total changes: 0 (test)\n"
    test_content += "- Blockers: 0\n"
    test_content += "- Decisions: 0\n"
    test_content += "- Context files updated: 0\n\n"
    test_content += "---\n"
    test_content += "_This is a test message from the Context Synchronization Agent_\n"
    
    # Format for Slack
    message = digest._format_slack_message(test_content, "test-digest.md")
    
    print("=" * 60)
    print("TEST SLACK DM MESSAGE")
    print("=" * 60)
    print("Recipient: " + config.get('slack', {}).get('digest_recipient_email', 'NOT SET'))
    print("Message length: " + str(len(message)) + " characters")
    print("\n" + "=" * 60)
    print("MESSAGE CONTENT:")
    print("=" * 60)
    print(message)
    print("=" * 60)
    print("\nTo send this message via Slack DM, use MCP-S Slack tools:")
    print("  Tool: mcp_MCP-S-SLACK_slack__slack_send-message")
    print("  to: " + config.get('slack', {}).get('digest_recipient_email', ''))
    print("  subject: Test Daily Digest - " + date_str)
    print("  body: (see message above)")
    print("\n" + "=" * 60)
    
    return message

if __name__ == '__main__':
    main()
