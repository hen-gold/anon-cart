# Slack Integration

## Overview

This directory contains documentation and information about the Slack channel used for team communication on the SF Purchase Flow (DOM2-6162) project.

## Channel Information

- **Channel**: Main team communication channel
- **Channel ID**: C0A6AMMMTFY
- **URL**: https://wix.slack.com/archives/C0A6AMMMTFY
- **Workspace**: wix.slack.com

See [channel-info.md](channel-info.md) for detailed channel information and access instructions.

## Purpose

The Slack channel serves as the primary real-time communication method for:
- Team coordination between BED, FED, UX, and Premium teams
- Status updates and progress sharing
- Discussion of blockers and dependencies
- Architectural and design decisions
- Quick questions and clarifications

## Agent Access

Agents can read from this channel using MCP-S Slack tools:

### Primary Tools
- `slack_get_channel_history` - Get recent messages
- `slack_search-messages` - Search for specific content
- `slack_get_thread_replies` - Read message threads

### Access Pattern
1. Read recent messages to get current status
2. Search for specific topics or issues
3. Read threads for full context

See [channel-info.md](channel-info.md) for detailed access instructions.

## Update Frequency

- **Method**: Manual/On-Demand
- **Agent Behavior**: Agents read from Slack when needed for context
- **No Automatic Syncing**: Messages are read directly from Slack, not synced to repository

## Directory Structure

```
slack/
├── README.md              # This file - integration overview
├── channel-info.md       # Detailed channel info and access instructions
└── updates/              # Future: synced message summaries (if needed)
    └── README.md         # Explanation of updates directory
```

## Integration with Context-Driven Development

This Slack channel is part of the project's source data, alongside:
- Jira issues and epics
- Google Docs and Sheets
- Repository analysis
- Master documentation

All sources are read-only and used to inform context-driven development decisions.

## Important Notes

- **Read-Only**: Agents should only read from Slack unless explicitly asked to post
- **Private Workspace**: This is a private Wix workspace channel
- **Context**: Always read messages in context of the DOM2-6162 epic
- **Real-Time**: Channel content updates frequently - check for latest messages when needed
