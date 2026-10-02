# RULES.md — Immutable Principles & Boundaries — {{PROJECT}}

**Owner: human. Immutable.** The agent may **suggest** additions when a new requirement surfaces something unanticipated — only the human adds them.

Always-on context. Keep it short.

---

## Precedence

`RULES.md` (safety) > `SECURITY.md` (immutable) > `SPEC.md` (the contract) > `AGENTS.md` (mechanics).
Any other conflict: **stop and flag it — do not guess.**

---

## Principles

1. **Never guess.** Anything unspecified → ask, or mark `[NEEDS CLARIFICATION: …]`.
2. **Done means verifiable, not describable.** Prove it — tests, builds, migrations, deploys — before claiming it.
3. **Gates are gates.** No skipping ahead, no "while I'm here".
4. **A failed check stops the work.** Report it. No silent retries, no workarounds.
5. **The spec is the contract.** Code follows `SPEC.md`; if the code needs something the spec doesn't say, the spec changes first — by the human.

---

## ✅ Always

- Read `AGENTS.md` + `RULES.md` at session start; load every other document just-in-time.
- Work one `PLAN.md` task at a time, and update `PLAN.md` in the same turn.
- Run the tests per `TESTING.md` every iteration, and show the real output.
- Verify against `SECURITY.md` before anything ships.
- Work on a `feature/<name>` branch; commits authored solely as the local git user.
- State assumptions explicitly when proceeding under uncertainty.

## ⚠️ Ask first

- Any change to the data structure, schema, a migration, or a persisted file/on-device format.
- Adding, removing, or upgrading a dependency.
- Changing anything in `SPEC.md`, `RULES.md`, `AGENTS.md`, or `SECURITY.md`.
- Widening scope beyond the approved `PLAN.md` task.
- Anything touching auth, sessions, permissions, or third-party integrations.
- Any deploy, release, or store submission; any destructive or hard-to-reverse operation.

## 🚫 Never

- Never commit on `main`/`master`; never merge — that is the human's.
- Never commit `.env`, signing keys, keystores, or expose secrets, tokens, or credentials in code, logs, tests, or output.
- Never edit `RULES.md` or `SECURITY.md`.
- Never create git worktrees.
- Never add an agent/AI identity as author, committer, co-author, or contributor; never put an agent name in a branch name.
- Never deploy to production or publish a release without explicit human approval.
- Never claim something works without having run it.
- Never delete, skip, or weaken a failing test.
- Never write application code before the `SPEC.md` → `DESIGN.md` → `TESTING.md`/`SECURITY.md` → `PLAN.md` gates are all approved.
