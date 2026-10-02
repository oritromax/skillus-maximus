# Brownfield: adopting the method on an existing codebase

> **Status: adapted, not proven.** It is derived from the greenfield method. Treat this as a starting
> procedure and refine it after the first real use.

The difference: in greenfield the SPEC precedes the code. In brownfield **the code is the current
truth, and much of it is undocumented.** The first job is to recover the contract, not to invent one.

## Procedure
1. **Don't scaffold over anything.** `scaffold.py` refuses to overwrite existing docs. Merge any
   existing README/ARCHITECTURE/CONTRIBUTING knowledge into the eight files instead of discarding it.
2. **Recovery pass (coding agent, read-only).** Produce `docs/as-is.md`: stack and versions, the commands
   that actually work (run them), the directory map, entities/schema (from migrations or the DB),
   routes/commands, auth model, background jobs, integrations, test suite state (run it; record
   pass/fail/skip honestly), deploy method. Every claim cites a file:line or a command output.
3. **AGENTS.md from reality:** (c)–(e) are filled from the recovery pass with the commands table's
   Verified column set from actual runs. RULES.md gets brownfield additions: "⚠️ Ask before changing
   behaviour not covered by a test"; "🚫 Never 'clean up' code outside the task".
4. **SPEC as-is + to-be.** Write SPEC for the **current behaviour** of the area being changed (not the
   whole system), marked `[AS-IS, recovered from …]`, then the change as new decisions/ACs. Unknown
   current behaviour → `[NEEDS CLARIFICATION]`, or a characterization test that pins it down.
5. **Characterization tests before changes.** For the area being touched, write tests that pin the
   *current* behaviour (even if it's odd), so changes are deliberate. TESTING.md records the baseline
   (what passed and failed before we touched anything).
6. **SECURITY baseline audit:** the same headings, but Step 1 includes existing findings (audit
   output, secrets in history, missing authz). The existing debt is listed separately from controls
   for the change.
7. **PLAN scoped to the change,** with Phase 0 = make the tests and commands reliably runnable.
8. **Scope discipline:** the method covers the area being changed and grows as more of the system is
   touched. Don't attempt a full-system SPEC up front; that's a rewrite plan in disguise.

## Intake questions (brownfield)
- What are we changing, and why now?
- Which parts of the system are in scope for this effort?
- Is there a test suite, and do you trust it?
- Who else commits here (other people, CI bots)? The git rules may need to respect an existing
  branching model, so ask and record it.
- Is production live? What's the deploy method today, and who can deploy?
