# DEPLOY.md — Deployment / Release Runbook — {{PROJECT}}

**Agent drafts against human guardrails, human approves.** Nothing deploys, releases or is submitted except by this runbook.
**Status: ⬜ PLACEHOLDER — constraints are recorded as earlier gates fix them; the runbook fills at Gate 7, after the SECURITY verification pass.**

---

## Standing rules (in force now)

- Dev/staging only without further approval once this runbook is approved. **Production, a public release, or a store submission requires the human's explicit approval naming the target.**
- Secrets never live in the repo or this file — names only; values live in the environment's secret store.
- A runbook step is ⬜ until it has actually been executed against staging and its output shown.

## Constraints already fixed by approved gates

## 1. Environments
## 2. Prerequisites
## 3. Configuration (names and purpose only — never values)
## 4. Build & release steps
## 5. Data — migrations, backups, tested restore
## 6. Smoke checks
## 7. Rollback — procedure and its honest limits
## 8. Observability
## 9. Scheduled jobs
## 10. Open questions
