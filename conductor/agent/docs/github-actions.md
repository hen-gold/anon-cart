# GitHub Actions – Conductor Sync and Reporting

This document describes the GitHub Actions workflows that run the Conductor sync agent on GitHub’s runners: scheduled sync, daily digest, on-demand dispatch, and optional Jira poll.

## Workflows

| Workflow | File | Trigger | Action |
|----------|------|---------|--------|
| **Scheduled sync** | `.github/workflows/scheduled-sync.yml` | Cron Sun–Thu 9, 12, 15, 20 UTC; `workflow_dispatch` | `sync-agent.py --mode scheduled` (full sync + digest), then commit & push |
| **Daily digest** | `.github/workflows/daily-digest.yml` | Cron daily 18:00 UTC; `workflow_dispatch` | `sync-agent.py --mode digest`, then commit & push |
| **Dispatch** | `.github/workflows/conductor-dispatch.yml` | `repository_dispatch` (event types below); `workflow_dispatch` | Run agent by event type / input, then commit & push |
| **Jira poll** (optional) | `.github/workflows/jira-poll.yml` | Cron every 30 min; `workflow_dispatch` | `sync-agent.py --mode jira`, then commit & push |

## Repository dispatch (real-time)

The **Conductor – Dispatch** workflow is triggered by `repository_dispatch`. External systems (e.g. Jira Automation or a small service) can trigger it by calling the GitHub API.

**Endpoint:** `POST /repos/hen-gold/anon-cart/dispatches`

**Event types and agent mode:**

| `event_type` | Agent mode |
|--------------|------------|
| `jira-update` | `--mode jira` |
| `full-sync` | `--mode full` |
| `digest` | `--mode digest` |

**Example (curl):**

```bash
# Jira update only
curl -X POST -H "Authorization: token YOUR_GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/hen-gold/anon-cart/dispatches \
  -d '{"event_type":"jira-update","client_payload":{}}'

# Full sync
curl -X POST -H "Authorization: token YOUR_GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/hen-gold/anon-cart/dispatches \
  -d '{"event_type":"full-sync","client_payload":{}}'
```

**Example (GitHub CLI):**

```bash
gh api repos/hen-gold/anon-cart/dispatches -f event_type=jira-update
gh api repos/hen-gold/anon-cart/dispatches -f event_type=full-sync
```

**Jira → GitHub:** Configure Jira (or Jira Automation) to send the webhook to an endpoint you control. That service then calls the GitHub API as above with `event_type: jira-update` (or `full-sync`). The workflow runs and commits any conductor changes.

## Required secrets

Configure these in **Settings → Secrets and variables → Actions** for the repository:

| Secret | Required for | Notes |
|--------|--------------|--------|
| `JIRA_EMAIL` | Jira sync | Jira account email |
| `JIRA_API_TOKEN` | Jira sync | Jira API token (Atlassian) |
| `JIRA_BASE_URL` | Optional | e.g. `https://wix.atlassian.net`; can be in config |
| `SLACK_BOT_TOKEN` | Slack sync + digest DM | Slack Bot User OAuth Token (`xoxb-...`) |
| `GOOGLE_SERVICE_ACCOUNT_KEY` | Docs sync | Base64-encoded service account JSON |
| `REPO_ACCESS_TOKEN` | Optional | PAT with access to wix-private repos for code sync; if unset, `GITHUB_TOKEN` is used for the agent |

The default `GITHUB_TOKEN` is used for pushing commits and does not need to be set as a secret.

## Permissions

Workflows request `contents: write` so they can push commits to the repository after sync.

## Concurrency

All Conductor workflows use `concurrency: group: conductor-sync` with `cancel-in-progress: false` so multiple runs do not overwrite each other’s commits.

## See also

- [ENV.md](ENV.md) – Environment variables used by the agent
- [README.md](../README.md) – Agent overview and usage
