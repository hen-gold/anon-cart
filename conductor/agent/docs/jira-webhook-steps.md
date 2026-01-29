# Jira webhook → n8n: quick steps

**Note:** Our organization does not support a Jira trigger (webhook) yet. For now, use **polling** via the **Conductor – Scheduled sync** workflow (runs 1–2×/day; includes Jira sync). When Jira webhooks are supported, you can use the steps below.

Use this after the **Conductor – Jira webhook sync** workflow exists in n8n (already created).

---

## Step 1: Get the Production Webhook URL from n8n

1. Open **https://n8n-product.wixprod.net/home/workflows**
2. Click **Conductor – Jira webhook sync** to open the workflow.
3. Click the **Webhook** node (first node).
4. In the node panel, find **Production URL** (or **Webhook URLs** → Production).
5. Copy the URL. It should look like:
   ```text
   https://n8n-product.wixprod.net/webhook/conductor-jira
   ```
   (Exact path may differ if you changed the webhook path when creating the workflow.)
6. **If the workflow is Inactive:** Turn **Activate workflow** ON (top right). The Production URL is only registered when the workflow is active.

---

## Step 2: Create the webhook in Jira

1. Log in to **https://wix.atlassian.net** (you need **Administer Jira** permission for webhooks).
2. Go to **Settings** (gear) → **System**.
3. Under **Advanced**, open **WebHooks**.
   - Direct link (after login): **https://wix.atlassian.net/secure/admin/ViewWebHooks.jspa**
4. Click **Create a WebHook** (or **Add webhook**).
5. Fill in:
   - **Name:** `Conductor n8n` (or any name you like)
   - **URL:** paste the Production URL from Step 1 (e.g. `https://n8n-product.wixprod.net/webhook/conductor-jira`)
   - **Events:** enable at least:
     - **Issue created**
     - **Issue updated**
   - **JQL filter (optional):** `project = DOM2` so only DOM2 issues trigger the webhook.
6. Save.

---

## Step 3: Verify

- Create or update a DOM2 issue in Jira.
- In n8n, open **Executions** and confirm a new run for **Conductor – Jira webhook sync**.
- Optionally check the repo for updated `conductor/tracks.md` or `conductor/sources/jira/child-issues.md` (after the Execute Command path is set and the agent runs successfully).

---

## Troubleshooting

- **No Production URL in n8n:** Activate the workflow first; then open the Webhook node again.
- **Jira "dead link" or no WebHooks:** You may need Jira admin access. Ask your Jira admin to create the webhook or grant you **Administer Jira**.
- **Webhook not firing:** Confirm the URL has no `:5678` port (use `https://n8n-product.wixprod.net/...`). Ensure you’re on VPN if Wix n8n is internal-only.
