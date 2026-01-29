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
- Required packages: `pip install -r requirements.txt` (PyYAML, schedule, flask; jira, slack-sdk, google-api-python-client, google-auth, PyGithub for API integrations)

### Setup
1. Set configuration in `config.yaml`.
2. Set environment variables for API access (see [docs/ENV.md](docs/ENV.md)): `JIRA_EMAIL`, `JIRA_API_TOKEN`, `SLACK_BOT_TOKEN`, and optionally `GOOGLE_APPLICATION_CREDENTIALS` or `GOOGLE_SERVICE_ACCOUNT_KEY`, `GITHUB_TOKEN`. Do not store secrets in the repo.
3. Install dependencies: `pip install -r requirements.txt`
4. Run from project root (or set `CONDUCTOR_PROJECT_ROOT`) so context file paths resolve correctly.

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

### Scheduled Execution (local)

Run agent with scheduled triggers:

```bash
python triggers/scheduled.py
```

Or use the wrapper script from project root: `./conductor/agent/run-daily-sync.sh`

### GitHub Actions (scheduled and real-time)

The repo includes workflows that run the agent on GitHub’s runners: scheduled sync, daily digest, on-demand dispatch (e.g. from Jira via API), and optional Jira poll. See [docs/github-actions.md](docs/github-actions.md) for workflow list, required secrets, and how to trigger `repository_dispatch`.

### Webhook Handlers (optional)

Run Flask webhook handlers locally (see `triggers/github_webhook.py`, `triggers/jira_webhook.py`) to invoke the agent from GitHub or Jira webhooks.

## Configuration

Edit `config.yaml` to configure:
- Repository URLs and branches
- Jira epic and project keys
- Slack channel ID
- Google Doc/Sheet IDs
- Sync intervals
- Reporting settings
- **Slack DM**: Set `slack.digest_recipient_user_id` (Slack user ID) and `reporting.send_slack_dm: true`; the agent sends the daily digest via Slack Web API when `SLACK_BOT_TOKEN` is set. See [docs/ENV.md](docs/ENV.md).

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
- **Frequency**: Daily at configured time (or when run with `--mode digest`)
- **Content**: Summary of all changes and communications (from changelog and Slack state)
- **Slack DM**: Sent via Slack Web API to `slack.digest_recipient_user_id` when `SLACK_BOT_TOKEN` is set and `reporting.send_slack_dm` is true

## API Integration

The agent uses direct REST/API clients (no MCP-S required when run on a server):

- **Jira**: Jira REST API (`jira` library) with `JIRA_EMAIL`, `JIRA_API_TOKEN`, `JIRA_BASE_URL`
- **Slack**: Slack Web API (`slack-sdk`) with `SLACK_BOT_TOKEN` for channel history and sending digest DM
- **Google**: Google Drive/Docs/Sheets API with `GOOGLE_APPLICATION_CREDENTIALS` or `GOOGLE_SERVICE_ACCOUNT_KEY`
- **GitHub**: GitHub API (`PyGithub`) with `GITHUB_TOKEN` for code sync

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
- Check configuration in `config.yaml` and environment variables (see [docs/ENV.md](docs/ENV.md))
- Ensure the agent runs from project root (or set `CONDUCTOR_PROJECT_ROOT`) so paths to `conductor/tracks.md`, `conductor/CHANGELOG.md`, etc. resolve correctly
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

## Slack DM Integration

The agent sends daily digests via Slack Web API (no MCP-S required). To enable:

1. Set `slack.digest_recipient_user_id` in `config.yaml` to your Slack user ID (e.g. `U06LKHPJG3W`)
2. Set `reporting.send_slack_dm` to `true` in config
3. Set the `SLACK_BOT_TOKEN` environment variable (Bot User OAuth Token, `xoxb-...`)

When the agent runs with `--mode digest` or `--mode scheduled`, it will generate the digest file and send it as a DM to that user.

## Important Notes

- **Read-Only Access**: Agent only reads from source repositories (wix-private)
- **Write Access**: Agent can write to context repository (hen-gold/anon-cart)
- **Privacy**: All source access is read-only, no modifications to original sources
- **Logging**: All operations are logged for debugging and audit
- **Slack DM**: Requires `SLACK_BOT_TOKEN` and `slack.digest_recipient_user_id` (see [docs/ENV.md](docs/ENV.md))

## Future Enhancements

- More sophisticated change detection
- Machine learning for decision extraction
- Trend analysis in daily digests
- Integration with more sources
- Real-time notifications
