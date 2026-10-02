# Gate 4: PLAN.md (the task board)

PLAN.md is **agent-owned**. The agent creates and maintains it, ticks tasks as they're proven, and
keeps the task log. The human approves it at the gate and steers it through review, never by editing.

Input: the approved SPEC + DESIGN + TESTING + SECURITY. PLAN is generated from all four, not from SPEC
alone: security controls and test infrastructure are tasks too.

A good plan makes implementation obvious. **If the implementer has to guess, the plan is incomplete.**

## Procedure

### 1. Ordering principle: write it down first
Tasks are ordered so **each one is verifiable the moment it lands**. Derive the project's specific
consequences and state them at the top of PLAN, e.g.:
1. **The invariant and its proof come before any feature built on it.** Building on an unproven
   guarantee means writing code whose correctness can't yet be shown.
2. **Authorization lands before the endpoints it protects are fleshed out,** so no route ever exists
   without an access rule.
3. **The UI comes after the API it renders.** DESIGN is exact enough that screens are assembly, not
   discovery, but they need something real to talk to.
4. **Distribution comes first for desktop/mobile:** a signed hello-world through the real pipeline in
   Phase 0 (the long pole is calendar time).
5. **The server before clients, primary surface before secondary** (hybrids).

### 2. Phases
A typical shape (adapt it, don't force it):
- **Phase 0, Foundation:** toolchain + every AGENTS (d) command run once; local services; schema +
  first migration; **the invariant + its guard test**; seed; the platform's Phase 0 from the platform
  file; CI if wanted.
- **Phase 1, Identity & access:** auth, sessions, the authorization table test.
- **Phase 2…n, Domain core → secondary flows → effects (email/push) → background jobs → admin.**
- **Interface phase(s):** tokens copied verbatim from DESIGN, components, screens, E2E journeys.
- **Hardening & ship readiness:** the SECURITY verification pass (its own task), packaging/release
  dry run, DEPLOY drafting (Gate 7) as a task.

### 3. Task shape
Each task is a table row:

| # | Task | Proves / enforces | Verified by | Status |
|---|---|---|---|---|
| T4 | `EXCLUDE USING gist` over room + time range | GO1 at the data layer (AC1, AC3) | Migration applied; two overlapping inserts in `psql`, second rejected | ⬜ |

Rules:
- **Atomic:** one reviewable unit, typically ≤ ~1–3 hours of agent work and one coherent diff. Split
  anything whose verification needs "and also".
- **"Proves / enforces" cites AC numbers, SECURITY control headings, or decisions.** Every SPEC AC
  appears in at least one task; `check_docs.py --gate 4` fails otherwise.
- **"Verified by" is an exact command or observable check,** not "tests pass".
- Explicit dependencies where order isn't obvious ("needs T8").
- Nothing in PLAN that isn't traceable to SPEC/DESIGN/TESTING/SECURITY. Anything else is
  `[AGENT-PROPOSED]` and needs approval.

### 4. Gate progress table
At the top, mirroring AGENTS.md: Gates 0–8 with status and a one-line note (counts: decisions, ACs,
screens, controls, tasks).

### 5. Review cadence (decide with the human now)
One question to the human: how often should the build stop for their review?
- **Per task** (default for the invariant and auth phases; safest, slowest)
- **Per phase** (default for the rest once the core is proven)
- **At named checkpoints** (listed in PLAN)
- **Mixed**: per task through Phase 1, then per phase.

Record the answer in PLAN under "Review cadence". The demo's lesson: "continue with plan" across
several tasks with no pause created proof debt the review had to repay.

### 6. Branching
Default: one feature branch per phase (`feature/p1-auth`), a PR at phase end, and the human merges. Ask if they
prefer per-task branches. Record it in PLAN. No agent names in branch names.

### 7. Task log section
An empty "Task log" heading. Each completed task gets an entry: branch, what was done, what was decided
(and by whom), the human input given, the verification output summary with a pointer to the real
output, and follow-ups/findings. This is the project's decision history.

### 8. Gate
Run `check_docs.py --gate 4`. Present: phase list, task count per phase, the AC coverage result, the
ordering principle, the cadence, open items. Wait for approval. Then implementation starts at T1.

## Reference point (the reference build)
45 tasks in 9 phases (Foundation → Auth & access → Booking core → Approval → Attendees &
notifications → Scheduled jobs → Admin → Interface → Hardening), with a three-point ordering
principle, a "Notes carried into implementation" section, and a growing task log.
