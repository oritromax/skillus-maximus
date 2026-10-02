# SECURITY.md — Pre-Ship Security Checklist — {{PROJECT}}

**Owner: human. Immutable.** The agent may suggest additions — only the human adds them.
**Status: ⬜ BASELINE ONLY — the checklist fills at Gate 3 from the agent's proposal, written by the human.**

Nothing ships until every applicable box is checked **and the check was actually performed**, not assumed.

---

## Baseline (applies regardless of stack — in force now)

- [ ] `.env` and every secret/credential/signing key are git-ignored and never committed — verified by a secrets scan of the full history before ship.
- [ ] No secrets, tokens or personal data in logs, test fixtures, or error output — verified by fixture review and log assertions in the test suite.
- [ ] Every dependency is pinned via a committed lockfile and added only with approval (RULES ⚠️) — verified by the audit command in `AGENTS.md` (d).

## Threat surface this checklist answers

| # | Entry point | Who can reach it | Top risks here | Worst realistic outcome |
|---|---|---|---|---|

## Consciously out of scope — no control is proposed for these

| Excluded | Cite | Why it shrinks the surface |
|---|---|---|

Control format: `- [ ] <control> — <what it stops (risk #, AC/D)> — verified by <how, per TESTING.md>`

## 1. Authentication & session handling
## 2. Authorization / access control per role
## 3. Input validation & output encoding
## 4. Rate limiting & abuse protection
## 5. Logging & PII policy
## 6. Data at rest / in transit
## 7. Third-party integration trust boundaries
## 8. Dependency & supply-chain review
## 9. Platform surface

## Decisions taken at Gate 3

## Verification rule

Every box is ticked by the human from evidence produced at Gate 6 — a real run per control. A box ticked on assumption is a defect.
