# n8n Execute Command Checklist – Results

**Date:** 2026-01-28  
**Instance:** https://n8n-product.wixprod.net

---

## Checklist results

| Check | Result | Details |
|-------|--------|---------|
| **Execute Command node exists** | ✅ Pass | Node appears in search ("Execute Command" – "Executes a command on the host"). |
| **Can add node to workflow** | ✅ Pass | Node was added to a new workflow (trigger: "When clicking Execute workflow" → Execute Command). |
| **Execution allowed** | ✅ Pass | Test command `echo hello` ran successfully. Output: exitCode 0, stdout "hello", stderr empty. |

---

## Test performed

1. Opened n8n workflows, created a new workflow ("My workflow 50").
2. Searched for "Execute Command" – node found and added.
3. Set command to `echo hello`.
4. Ran "Execute step" for the Execute Command node.
5. Execution completed: table output showed exitCode 0, stdout "hello".

---

## Conclusion

- **n8n-product.wixprod.net allows the Execute Command node** and execution of commands on the host.
- You can use **Option A (same host)** for the sync agent: run the agent on the same host as n8n and trigger it with an Execute Command node (e.g. `python3 /path/to/sync-agent.py --mode scheduled`).

**Next step (policy):** Confirm with your n8n/platform owner that you are allowed to run your own code (Python, clone repo, env vars) on that host. The product allows it; policy may still restrict what you deploy there.

---

## Test workflow

- A temporary workflow was used: **My workflow 50** (trigger + Execute Command with `echo hello`). You can delete it from the workflows list if you no longer need it.
