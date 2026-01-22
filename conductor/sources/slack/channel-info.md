# Slack Channel Information

## Channel Details

- **Channel URL**: https://wix.slack.com/archives/C0A6AMMMTFY
- **Channel ID**: C0A6AMMMTFY
- **Workspace**: wix.slack.com
- **Purpose**: Main communication channel between teams for SF Purchase Flow (DOM2-6162)

## Channel Purpose

This is the primary Slack channel for team communication regarding the SF Purchase Flow epic (DOM2-6162). Teams use this channel to:

- Share updates on work progress
- Coordinate between BED, FED, UX, and Premium teams
- Discuss blockers and dependencies
- Share decisions and architectural discussions
- Provide status updates on tracks and issues

## Access Instructions for Agents

### Using MCP-S Slack Tools

Agents can access this channel using the following MCP-S Slack tools:

#### Get Channel History
```javascript
slack_get_channel_history(channel_id: "C0A6AMMMTFY", limit: 50)
```
- Retrieves recent messages from the channel
- Default limit is 10, can specify up to needed amount
- Returns messages in chronological order

#### Search Messages
```javascript
slack_search-messages(in: "#channel-name", searchText: "DOM2-6162", after: "2026-01-01")
```
- Search for specific content in channel messages
- Supports filters: `in`, `from`, `after`, `before`, `exactPhrase`
- Useful for finding discussions about specific topics or issues

#### Get Thread Replies
```javascript
slack_get_thread_replies(channel_id: "C0A6AMMMTFY", thread_ts: "timestamp")
```
- Get all replies in a message thread
- Thread timestamp format: `1234567890.123456`

### Channel ID

The channel ID `C0A6AMMMTFY` can be used directly with all Slack MCP-S tools that require a channel_id parameter.

### Finding Channel ID (if needed)

If you need to find the channel ID by name:
```javascript
slack_find-channel-id(channelName: "channel-name")
```

## Reading Channel Updates

### Recommended Approach

1. **Check Recent Messages**: Use `slack_get_channel_history` to get the latest messages
2. **Search for Specific Topics**: Use `slack_search-messages` to find discussions about:
   - Specific Jira issues (e.g., "DOM2-6598")
   - Team updates (e.g., "BED", "FED")
   - Blockers or dependencies
   - Status updates

3. **Read Threads**: If a message has replies, use `slack_get_thread_replies` to get full context

### Update Frequency

- **Access Method**: Manual/On-Demand
- **When to Check**: 
  - When starting work on a track
  - When checking for team updates
  - When looking for decisions or discussions
  - When investigating blockers or dependencies

## Message Format

Slack messages typically contain:
- Text content
- User information (who posted)
- Timestamp
- Thread replies (if any)
- Reactions (if any)
- Links to Jira, GitHub, Google Docs, etc.

## Important Notes

- **Read-Only Access**: Agents should only read from this channel unless explicitly asked to post
- **Privacy**: This is a private Wix workspace channel
- **Context**: Messages should be read in context of the project (DOM2-6162 epic)
- **Updates**: Channel content changes frequently - always check for latest messages when needed

## Integration with Project

This channel complements other sources:
- **Jira**: Formal issue tracking and status
- **Google Docs**: Design and architecture documents
- **Repositories**: Code implementation
- **Slack**: Real-time team communication and updates

## Example Use Cases

1. **Check for Blockers**: Search for "blocker" or "blocked" to find current blockers
2. **Team Updates**: Search for team names (BED, FED, UX) to find team-specific updates
3. **Issue Discussions**: Search for Jira issue keys (e.g., "DOM2-6598") to find related discussions
4. **Status Updates**: Get recent messages to see latest team status updates
5. **Decision Tracking**: Search for "decision" or "decided" to find architectural or product decisions
