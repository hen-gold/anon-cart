# Slack DM Setup for Daily Digest

This guide explains how to set up automatic Slack DM delivery for daily digest reports.

## Quick Setup

1. **Set your Slack email in config.yaml**:
   ```yaml
   slack:
     digest_recipient_email: "your-email@example.com"
   ```

2. **Ensure DM sending is enabled**:
   ```yaml
   reporting:
     send_slack_dm: true
   ```

## How It Works

The agent generates the daily digest and automatically attempts to send it via Slack DM when:
- The digest is generated (daily at configured time, or manually with `--mode digest`)
- `send_slack_dm` is set to `true` in config
- A recipient email is configured

## Sending via MCP-S Tools

When running the agent in Cursor (which has MCP-S Slack tools), the DM will be sent automatically. The agent uses the MCP-S Slack `send-message` tool to deliver the digest.

### Manual Sending

If you need to manually send a digest via Slack DM, you can use Cursor's MCP-S Slack tools:

1. Generate the digest:
   ```bash
   python conductor/agent/sync-agent.py --mode digest
   ```

2. Use MCP-S Slack tool to send DM:
   - Tool: `mcp_MCP-S-SLACK_slack__slack_send-message`
   - Parameters:
     - `to`: Your Slack email (from config)
     - `subject`: "Daily Digest - YYYY-MM-DD"
     - `body`: Content from the digest file

### Using the Helper Script

The `send_slack_dm.py` helper script prepares the message for sending. In a Cursor environment with MCP-S tools, you can:

1. Run the agent to generate digest
2. The agent will automatically attempt to send via MCP-S tools if available

## Troubleshooting

### DM Not Received

1. **Check configuration**:
   - Verify `slack.digest_recipient_email` is set correctly
   - Ensure `reporting.send_slack_dm` is `true`

2. **Check logs**:
   - Look for "Daily digest ready to send via Slack DM" in logs
   - Check for any error messages

3. **Verify MCP-S access**:
   - Ensure you're running in an environment with MCP-S Slack tools
   - Check that MCP-S Slack is properly configured

4. **Manual test**:
   - Try sending a test DM using MCP-S Slack tools directly
   - Verify your Slack email is correct

### Running Outside Cursor

If running the agent outside of Cursor (standalone Python script), the Slack DM sending will be logged but not actually sent, as MCP-S tools are not available. In this case:

1. The digest file is still generated
2. Logs will indicate the message that would be sent
3. You can manually send using MCP-S tools in Cursor, or
4. Use a Slack API integration (requires Slack app setup)

## Configuration Example

```yaml
slack:
  channel_id: C0A6AMMMTFY
  channel_url: https://wix.slack.com/archives/C0A6AMMMTFY
  workspace: wix.slack.com
  read_only: true
  digest_recipient_email: "your-email@wix.com"  # Your Slack email

reporting:
  daily_digest_time: "18:00"
  send_slack_dm: true  # Enable Slack DM delivery
```

## Notes

- The agent requires MCP-S Slack tools to actually send DMs
- When running in Cursor, MCP-S tools are automatically available
- The digest is always saved to file regardless of DM sending status
- DM sending failures are logged but don't stop digest generation
