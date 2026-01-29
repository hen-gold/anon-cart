# Environment Variables

The sync agent reads credentials and optional paths from environment variables. Do not store secrets in `config.yaml`.

| Variable | Required | Description |
|----------|----------|-------------|
| `JIRA_EMAIL` | Yes (for Jira sync) | Jira account email |
| `JIRA_API_TOKEN` | Yes (for Jira sync) | Jira API token (Atlassian) |
| `JIRA_BASE_URL` | No | Jira base URL; defaults to `jira.base_url` in config (e.g. `https://wix.atlassian.net`) |
| `SLACK_BOT_TOKEN` | Yes (for Slack sync / digest DM) | Slack Bot User OAuth Token (`xoxb-...`) |
| `GOOGLE_APPLICATION_CREDENTIALS` | One of these for Google sync | Path to service account JSON file |
| `GOOGLE_SERVICE_ACCOUNT_KEY` | One of these for Google sync | Base64-encoded JSON service account key |
| `GITHUB_TOKEN` | No (for code sync) | GitHub personal access token for commit listing |
| `CONDUCTOR_PROJECT_ROOT` | No | Repo root for resolving context file paths; default inferred from config file location |

## Example

```bash
export JIRA_EMAIL="you@example.com"
export JIRA_API_TOKEN="your-jira-token"
export JIRA_BASE_URL="https://wix.atlassian.net"
export SLACK_BOT_TOKEN="xoxb-..."
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
# Optional:
export CONDUCTOR_PROJECT_ROOT="/path/to/anon-cart"
export GITHUB_TOKEN="ghp_..."
```
