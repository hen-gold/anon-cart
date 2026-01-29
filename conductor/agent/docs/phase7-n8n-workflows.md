# Phase 7: n8n Workflows – Conductor Sync and Reporting

**Instance:** https://n8n-product.wixprod.net  
**Purpose:** Run the Conductor agent from n8n (Jira webhook, scheduled sync, daily digest) so sync and reporting work 24/7 and in real time when the repo host is not your laptop.

---

## Prerequisites

1. **Agent deployed on the same host as n8n** (or a host reachable by n8n’s Execute Command).  
   - Clone `anon-cart` (or your conductor repo) on that host.  
   - Install deps: `pip install -r conductor/agent/requirements.txt`.  
   - Set env vars (see [ENV.md](ENV.md)): `JIRA_EMAIL`, `JIRA_API_TOKEN`, `JIRA_BASE_URL`, `SLACK_BOT_TOKEN`, and optionally `GOOGLE_APPLICATION_CREDENTIALS` / `GOOGLE_SERVICE_ACCOUNT_KEY`, `GITHUB_TOKEN`, `CONDUCTOR_PROJECT_ROOT`.

2. **Paths to use in workflows**  
   - `PROJECT_ROOT`: repo root (e.g. `/opt/anon-cart` or `$HOME/anon-cart`).  
   - `AGENT_DIR`: `PROJECT_ROOT/conductor/agent`.  
   - Sync agent script: `AGENT_DIR/sync-agent.py`.  
   - Run from **project root** so `conductor/CHANGELOG.md` and `conductor/reports/` resolve correctly.  
   - In Execute Command, set **working directory** to `PROJECT_ROOT` and run:  
     `python3 conductor/agent/sync-agent.py --mode <mode>`  
     (or use absolute path: `python3 /opt/anon-cart/conductor/agent/sync-agent.py --mode <mode>`).

3. **Execute Command enabled** on n8n-product.wixprod.net (already verified; see [n8n-execute-command-checklist.md](n8n-execute-command-checklist.md)).

---

## Workflows to Create

| # | Workflow        | Trigger           | Action                                      |
|---|-----------------|-------------------|---------------------------------------------|
| 1 | Jira webhook    | Webhook (POST)    | Execute Command: sync-agent `--mode jira`   |
| 2 | Scheduled sync  | Cron Sun–Thu 9,18 (1–2×/day) | Execute Command: sync-agent `--mode scheduled` |
| 3 | Daily digest    | Cron daily 18:00  | Execute Command: sync-agent `--mode digest` |

**Note:** If your org does not support a Jira trigger (webhook) yet, use **scheduled sync** only: it runs full sync (including Jira) 1–2×/day and keeps n8n executions low. See [jira-webhook-steps.md](jira-webhook-steps.md) for when webhooks are available.

---

## 1. Jira Webhook → Sync (real-time Jira updates)

**Goal:** When Jira sends a webhook (e.g. issue created/updated in DOM2), n8n runs the agent in Jira-only mode so `tracks.md`, `child-issues.md`, and track metadata stay up to date.

### Option A: Create workflow manually

1. In n8n: **Workflows** → **Add workflow**.
2. **Trigger: Webhook**
   - Add node **Webhook**.
   - **HTTP Method:** POST.
   - **Path:** e.g. `conductor-jira` (full URL will be like `https://n8n-product.wixprod.net/webhook/conductor-jira`).
   - **Respond:** Immediately (or “When last node finishes” if you want to wait for sync).
   - Save the workflow and **Activate** it; copy the **Production Webhook URL**.
3. **Filter (optional but recommended)**  
   - Add an **IF** or **Code** node after the Webhook: only continue if body matches your project/events (e.g. `body.project?.key === 'DOM2'` and `body.webhookEvent` in `['jira:issue_created','jira:issue_updated']`). This avoids running sync for unrelated Jira events.
4. **Action: Execute Command**
   - Add **Execute Command**.
   - **Command:**  
     `python3 conductor/agent/sync-agent.py --mode jira`  
     (if cwd is project root), or  
     `python3 /absolute/path/to/anon-cart/conductor/agent/sync-agent.py --mode jira`.  
   - **Execute once per run:** On (one sync per webhook call).
   - If your n8n node supports **working directory**, set it to `PROJECT_ROOT`; otherwise use absolute path in the command and `cd PROJECT_ROOT && python3 conductor/agent/sync-agent.py --mode jira`.
5. **Connect:** Webhook → (Filter) → Execute Command.
6. **Save** and **Activate**.

### Option B: Import JSON

1. In n8n: **Workflows** → **Add workflow** → **⋮** (menu) → **Import from File** (or **Import from URL** if you host the file).
2. Select `docs/n8n-workflows/jira-webhook-sync.json` from this repo (path relative to `conductor/agent/`).
3. **If import fails** (e.g. node type or parameter format differs in your n8n version), create the workflow manually using Option A; the logic is the same.
3. Open the **Execute Command** node and set:
   - **Command** to your path (e.g. `python3 conductor/agent/sync-agent.py --mode jira` with cwd = project root, or absolute path).
   - **Working directory** to project root if the node supports it.
4. Save, Activate, and copy the **Production Webhook URL**.

### Configure Jira to send events to n8n

1. Jira: **Settings** → **System** → **WebHooks** (or **Apps** → **Webhooks**).
2. **Create a webhook**:
   - **Name:** e.g. `Conductor n8n`
   - **URL:** the n8n Production Webhook URL (e.g. `https://n8n-product.wixprod.net/webhook/conductor-jira`).
   - **Events:** e.g. **Issue created**, **Issue updated** (and optionally **Issue deleted**).
   - **JQL filter (optional):** `project = DOM2` so only DOM2 events are sent.
3. Save. New/updated DOM2 issues will POST to n8n and trigger the sync.

---

## 2. Scheduled Sync (Sun–Thu at 9:00, 12:00, 15:00, 20:00)

**Goal:** Run full sync and daily digest on a schedule (same as local cron: 9, 12, 15, 20 Sun–Thu).

### Option A: Create workflow manually

1. **Trigger: Schedule**
   - Add **Schedule Trigger**.
   - **Trigger rule:** Custom (cron).
   - **Cron expression:** `0 9,12,15,20 * * 0-4`  
     (minute 0, hours 9/12/15/20, every day of month, every month, Sun(0)–Thu(4)).
2. **Action: Execute Command**
   - **Command:**  
     `python3 conductor/agent/sync-agent.py --mode scheduled`  
     (with cwd = project root) or absolute path as above.
   - **Execute once:** On.
3. Connect Schedule Trigger → Execute Command.
4. **Save** and **Activate**.

### Option B: Import JSON

1. Import `n8n-workflows/scheduled-sync.json`.
2. Edit **Execute Command**: set command and working directory (or absolute path).
3. Save and Activate.

---

## 3. Daily Digest Only (daily at 18:00)

**Goal:** Generate the daily digest (and send Slack DM if configured) every day at 18:00, even if you don’t run the full scheduled sync at that time.

### Option A: Create workflow manually

1. **Trigger: Schedule**
   - Add **Schedule Trigger**.
   - **Cron expression:** `0 18 * * *` (every day at 18:00).
2. **Action: Execute Command**
   - **Command:**  
     `python3 conductor/agent/sync-agent.py --mode digest`  
     (with cwd = project root) or absolute path.
   - **Execute once:** On.
3. Connect Schedule Trigger → Execute Command.
4. **Save** and **Activate**.

### Option B: Import JSON

1. Import `n8n-workflows/daily-digest.json`.
2. Edit **Execute Command**: set command and working directory (or absolute path).
3. Save and Activate.

---

## Path and env summary

| Item | Value |
|------|--------|
| Project root (example) | `/opt/anon-cart` or `$HOME/anon-cart` |
| Agent script | `conductor/agent/sync-agent.py` |
| Run from | Project root (so `conductor/CHANGELOG.md`, `conductor/reports/` are correct) |
| Env vars | See [ENV.md](ENV.md); must be set in the environment where n8n runs (e.g. systemd, Docker, or n8n’s process). |

---

## Verification

1. **Jira webhook:** Create or update a DOM2 issue in Jira → check n8n **Executions** for a run → check repo for updated `conductor/tracks.md` or `conductor/sources/jira/child-issues.md`.
2. **Scheduled sync:** Trigger the “Scheduled Sync” workflow manually once → confirm Execute Command succeeds and `conductor/reports/` or `conductor/CHANGELOG.md` updates.
3. **Daily digest:** Trigger “Daily Digest” workflow manually once → confirm digest file in `conductor/reports/` and (if configured) Slack DM.

---

## Troubleshooting

- **Execute Command fails (e.g. “python3: command not found”)**  
  Use full path to `python3` (e.g. `/usr/bin/python3`) or ensure the n8n process env has `PATH` that includes Python.

- **“No such file or directory” for sync-agent.py**  
  Use absolute path for the script, or set **Working directory** in Execute Command to project root.

- **Changelog/reports written under wrong path**  
  Agent infers project root from config path or `CONDUCTOR_PROJECT_ROOT`. Run from project root and/or set `CONDUCTOR_PROJECT_ROOT` to the repo root.

- **Jira webhook not firing**  
  Confirm Jira webhook URL is the n8n **Production** URL, workflow is **Active**, and Jira has permission to reach n8n (no firewall blocking).

- **n8n runs in Docker**  
  Execute Command runs inside the n8n container. Either mount the repo into the container and use paths inside the container, or run the agent on the host and trigger it from the host (e.g. cron calling n8n webhook, or n8n using a different integration that can trigger the host). See n8n docs for “Execute Command” and Docker.

---

## Files in this phase

- **phase7-n8n-workflows.md** (this file) – step-by-step guide.
- **n8n-workflows/jira-webhook-sync.json** – Jira webhook workflow (import and set paths).
- **n8n-workflows/scheduled-sync.json** – Scheduled sync (cron 9,12,15,20 Sun–Thu).
- **n8n-workflows/daily-digest.json** – Daily digest (cron 18:00).

After creating or importing the workflows, replace placeholder paths in the Execute Command nodes with your actual `PROJECT_ROOT` and script path.
