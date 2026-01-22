# Context Synchronization Agent

Automated agent that monitors changes across repositories, Jira, and Slack, automatically updates relevant context documents, and generates daily digests and a live changelog.

## Overview

The context synchronization agent ensures that all context-driven development artifacts stay up-to-date with changes in:
- **Code Repositories**: BED (premium-server/premium-cart) and FED (premium-cart-anonymous)
- **Jira**: Epic DOM2-6162 and all child issues
- **Google Docs**: Master document and dependencies spreadsheet
- **Slack**: Team communication channel C0A6AMMMTFY

## Features

### Context Synchronization
- **Code Commit Monitoring**: Detects commits and updates repository summaries
- **Jira Update Monitoring**: Tracks issue status changes and updates tracks.md
- **Document Change Monitoring**: Watches Google Docs/Sheets for updates
- **Slack Communication**: Extracts decisions and key information from Slack

### Reporting
- **Daily Digest**: Comprehensive daily report of all changes and communications
- **Live Changelog**: Real-time record of all changes in CHANGELOG.md

## Installation

### Prerequisites
- Python 3.8+
- Required packages (install via `pip install -r requirements.txt`):
  - PyYAML
  - schedule (for scheduled triggers)
  - flask (for webhook handlers, optional)

### Setup
1. Ensure configuration is set in `config.yaml`
2. Install dependencies: `pip install -r requirements.txt`
3. Make script executable: `chmod +x sync-agent.py`

## Usage

### Manual Execution

Run the agent manually:

```bash
# Full sync (all sources)
python sync-agent.py --mode full

# Sync specific source
python sync-agent.py --mode code    # Code commits only
python sync-agent.py --mode jira    # Jira updates only
python sync-agent.py --mode docs    # Documents only
python sync-agent.py --mode slack    # Slack only

# Generate daily digest
python sync-agent.py --mode digest

# Force daily digest generation
python sync-agent.py --mode digest --force-digest
```

### Scheduled Execution

Run agent with scheduled triggers:

```bash
python triggers/scheduled.py
```

This will:
- Run daily sync at configured time (default: 6 PM)
- Periodically check for code commits, Jira updates, and document changes
- Generate daily digest automatically

### Webhook Handlers

#### GitHub Webhooks

Set up GitHub webhook pointing to:
```
POST /webhook/github
```

Events to subscribe:
- `push` - Code commits
- `pull_request` - PR merges

#### Jira Webhooks

Configure Jira webhook for:
- Issue updated events
- Issue created events

Filter for project: DOM2

## Configuration

Edit `config.yaml` to configure:
- Repository URLs and branches
- Jira epic and project keys
- Slack channel ID
- Google Doc/Sheet IDs
- Sync intervals
- Reporting settings

## Architecture

### Modules

- **sync-agent.py**: Main agent script, orchestrates all operations
- **sync/**: Synchronization modules
  - `code_sync.py`: Code commit monitoring
  - `jira_sync.py`: Jira update monitoring
  - `docs_sync.py`: Document change monitoring
  - `slack_sync.py`: Slack communication summary
- **reporting/**: Reporting modules
  - `daily_digest.py`: Daily digest generation
  - `changelog.py`: Live changelog management
- **triggers/**: Trigger handlers
  - `github_webhook.py`: GitHub webhook handler
  - `jira_webhook.py`: Jira webhook handler
  - `scheduled.py`: Scheduled trigger handler

## Output Files

### CHANGELOG.md
- **Location**: `conductor/CHANGELOG.md`
- **Format**: Reverse chronological (newest first)
- **Content**: All changes with timestamps and details

### Daily Digests
- **Location**: `conductor/reports/daily-digest-YYYY-MM-DD.md`
- **Frequency**: Daily at configured time
- **Content**: Summary of all changes and communications

## Integration with MCP-S Tools

The agent uses MCP-S tools for accessing external services:

- **Jira**: MCP-S Jira tools for issue queries
- **Google Workspace**: MCP-S Google Workspace tools for Docs/Sheets
- **Slack**: MCP-S Slack tools for channel reading
- **GitHub**: GitHub API or MCP-S tools for repository access

## Context Files Updated

The agent automatically updates:

- `conductor/sources/bed/premium-cart-summary.md` - BED repository changes
- `conductor/sources/fed/premium-cart-anonymous-summary.md` - FED repository changes
- `conductor/tech-stack.md` - Dependency changes
- `conductor/tracks.md` - Jira status changes
- `conductor/sources/jira/child-issues.md` - Jira issue updates
- `conductor/sources/docs/master-document.md` - Master document updates
- `conductor/sources/docs/dependencies.md` - Dependencies updates
- `conductor/product.md` - Product vision changes
- `conductor/decisions.md` - Decisions from Slack
- `conductor/CHANGELOG.md` - All changes logged

## Troubleshooting

### Agent not detecting changes
- Check configuration in `config.yaml`
- Verify MCP-S tool access and permissions
- Check logs in `conductor/agent/logs/sync-agent.log`

### Daily digest not generating
- Check `daily_digest_time` in config
- Verify reports directory exists
- Check if digest was already generated today

### Webhook not receiving events
- Verify webhook URL is correct
- Check webhook secret (if configured)
- Review webhook event subscriptions

## Development

### Adding New Sync Sources

1. Create new module in `sync/` directory
2. Implement `sync()` method
3. Add to `sync-agent.py` initialization
4. Update config.yaml with new source settings

### Extending Reporting

1. Add new report type in `reporting/` directory
2. Integrate with main agent script
3. Update configuration as needed

## Important Notes

- **Read-Only Access**: Agent only reads from source repositories (wix-private)
- **Write Access**: Agent can write to context repository (hen-gold/anon-cart)
- **Privacy**: All source access is read-only, no modifications to original sources
- **Logging**: All operations are logged for debugging and audit

## Future Enhancements

- More sophisticated change detection
- Machine learning for decision extraction
- Trend analysis in daily digests
- Integration with more sources
- Real-time notifications
