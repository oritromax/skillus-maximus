# Gates 6–8: Verify, DEPLOY, ship

> **Status of this reference:** written from the method's rules and the platform files. **It hasn't
> been run end to end yet**; the reference build had not reached Gate 6 when this was written. The first real project to reach
> this phase is the test. Port what you learn into this file afterwards.

## Gate 6: SECURITY verification pass
Precondition: every PLAN implementation task ✅ (or explicitly deferred by the human with a decision).

1. The agent walks SECURITY.md heading by heading. For each control it **runs the verification named
   in the line** and collects evidence: the test name + its output, the header dump, the audit output,
   the manual check steps + result.
2. It produces `docs/security-verification-<date>.md` (or a PLAN task-log entry if it's short):

   | Control (heading.n) | Verified by | Evidence (command + real output excerpt) | Result |
   |---|---|---|---|

   Result is one of ✅ pass · ❌ fail · ⚠️ partial · N/A (with cite).
3. A ❌ or ⚠️ means stop: open a fix task in PLAN, implement it through the loop, and re-verify.
4. The agent **doesn't tick SECURITY.md boxes**; it's immutable to the agent. The human ticks them
   from the evidence report (or instructs the orchestrating agent to tick specific lines, which is their authorship act).
5. Gate 6 closes when every applicable box is ticked **and the check was actually performed**.

Also run before Gate 6 closes: dependency audit at the agreed threshold, a secrets scan of the repo
history (`gitleaks detect` or equivalent), `.env`/keys absent from git, and the full suite + E2E on a
clean checkout.

## Gate 7: DEPLOY.md
DEPLOY.md is drafted by the agent against the guardrails already recorded (standing rules + constraints
fixed by earlier gates) and approved by the human. Use the platform file's DEPLOY section.

**Clarify first** (one batch, only open items): target host/platform and account; domain/DNS; who
holds production secrets and where (never in the repo); backup + restore expectation; monitoring and
alerting destination; release cadence; for mobile/desktop: store accounts, signing key custody, release
tracks/channels.

Sections (`templates/DEPLOY.md`):
1. **Environments:** local / staging / production (and for apps: beta/stable channels, store tracks).
2. **Prerequisites:** accounts, access, tools, certificates.
3. **Configuration:** every env var by name and purpose (never values), and where each is set.
4. **Build & release steps:** exact commands, in order, and where they run.
5. **Data:** migrations (run before the new code serves; backward compatible with the running
   version), seed policy, backups (schedule, location, **tested restore** with the command).
6. **Smoke checks:** exact commands/URLs and the expected results after each deploy.
7. **Rollback:** the exact procedure **and its honest limits** (a migration that can't be reversed;
   binaries can't be unshipped; stores can only halt rollouts). Decide forward-fix vs rollback per
   change type.
8. **Observability:** logs, error tracking, uptime check, the alerts and where they go.
9. **Scheduled jobs:** how each is scheduled in this environment and how failures surface.
10. **Open questions**

**Prove it in staging.** Gate 7 isn't approved on prose: the agent executes the runbook against
staging (or the internal/beta track) and pastes the output of every step and smoke check. A runbook
step that hasn't run is ⬜, same rule as the commands table.

## Gate 8: Deploy
- Dev/staging per DEPLOY.md: allowed once Gate 7 is approved.
- **Production, public release, or store submission: only on the human's explicit instruction
  naming the target** ("deploy to prod on <host>", "submit 1.0.0 to the App Store"). That instruction is the
  confirmation.
- Execute the runbook exactly, paste each step's output, run the smoke checks, and record the release
  in PLAN (version, commit, time, smoke results).
- Any smoke failure means following the rollback section, reporting, and stopping.

## After v1
- New work starts with a SPEC change (new decisions, new ACs), not with code. Small features follow
  the same gates, compressed: SPEC diff → TESTING rows → SECURITY delta (if any) → PLAN tasks.
- Keep DEPLOY.md current every time a step changes; a stale runbook is worse than none.
- Lessons that would have changed an earlier gate get written into this skill.
