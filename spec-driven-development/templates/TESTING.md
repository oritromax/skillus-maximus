# TESTING.md — {{PROJECT}}

**Agent drafts, human reviews.**
**Status: ⬜ PLACEHOLDER — fills at Gate 3, after DESIGN approval.**

---

## 1. Philosophy

**"Done" means verifiable, not describable.** Every claim that something works is backed by the output of a command actually run in the session that claims it.

1. **The test suite proves the acceptance criteria, not the implementation.** Every `SPEC.md` AC maps to at least one named test (§4). An AC with no test is an unmet AC.
2. **The invariant (GO1) gets the strictest proof** — against the real dependency, never a mock that cannot exhibit the failure.
3. **A failing test stops the work.** Reported — never deleted, skipped, weakened, or worked around (§11).

## 2. What gets tested, and at what level

| Level | Runs against | Covers | Speed |
|---|---|---|---|

### 2.1 What belongs at each level
### 2.2 The E2E journeys — and only these

## 3. Coverage expectations

- 100% of `SPEC.md` acceptance criteria — the only coverage metric that gates a task.
- 100% of state-machine legal transitions, plus each illegal transition refused.
- Line coverage reported, not targeted.

## 4. Acceptance criteria → test map

| AC | Level | Test proves |
|---|---|---|

## 5. The invariant test — special handling

## 6. Testing time-dependent behaviour

## 7. External effects (email / push / webhooks / files)

## 8. Platform-specific checks

## 9. Test structure, naming, and data

- Test names state the criterion and carry the AC number: `refuses X when Y (AC12)`.
- No real credentials, personal data, or real email addresses in fixtures — ever.

## 10. Running tests

Commands are those in `AGENTS.md` (d). **Unverified until PLAN.md T1 has run them.**

## 11. The per-iteration loop

After **every** implementation task, before it is ticked in `PLAN.md`:

1. Full unit + integration suite.
2. Typecheck + lint.
3. E2E when the task touched a screen; platform checks when it touched packaging/update/permissions.
4. **Paste the real output.** Not a summary.
5. Only then tick the task in `PLAN.md`, naming the ACs it satisfied.

## 12. When a test fails

**Report the failure and stop.** Never: delete/skip/`.only` around it; loosen an assertion to match wrong behaviour; change an AC to fit the implementation; report done with a known failure outstanding. A test that contradicts the SPEC is a finding — only the human decides which is wrong.
