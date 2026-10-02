# AGENTS.md — Operating Manual — {{PROJECT}}

**This file is the entry point.** Every session starts here, not from a chat prompt.
Read this file + `RULES.md` at the start of every session. Read everything else just-in-time.

Owner: **human** (the agent may suggest changes, never edit).
Platform: **{{PLATFORM}}** · Created: {{DATE}}

---

## (a) Document Index

| File | What it is | Owner | Read it when |
|---|---|---|---|
| `AGENTS.md` | This operating manual + index to every other file | Human | **Always** — start of every session |
| `RULES.md` | Immutable principles + ✅ Always / ⚠️ Ask first / 🚫 Never | Human (immutable) | **Always** — start of every session |
| `SPEC.md` | What the system is + system-level how (data, interfaces, auth, flows). **Source of truth.** | Human | Any question of behaviour, scope, data, interfaces, auth, acceptance criteria |
| `DESIGN.md` | UI/visual (or interface) contract — screens, tokens, components, states | Agent drafts, human reviews | Touching UI, layout, styling, visual states, command output |
| `TESTING.md` | Proof plan — levels, AC → test map, per-iteration loop, failure policy | Agent drafts, human reviews | Writing/running tests; **every implementation iteration** |
| `SECURITY.md` | Pre-ship security checklist, every control with how it is verified | Human (immutable) | Before anything ships; touching auth, secrets, input, data exposure |
| `PLAN.md` | Task board — atomic, ordered, verifiable tasks + task log | **Agent** | Start of every implementation task; update as you go |
| `DEPLOY.md` | Deployment / release runbook | Agent drafts, human approves | Before any deploy, release or store submission |

### Conflict precedence

```
RULES.md (safety)  >  SECURITY.md (immutable)  >  SPEC.md (the contract)  >  AGENTS.md (mechanics)
```

Any conflict not resolved by that ordering: **stop and flag it — do not guess.**
Anything unspecified: ask, or mark `[NEEDS CLARIFICATION: …]`. Never guess.

---

## (b) Context-Loading Policy

- You are **aware of every file** in the index at all times; you **read** each only when the operation needs it.
- **Always-on:** `AGENTS.md` + `RULES.md` — deliberately short.
- Do not bulk-read the document set "for context".

| Operation | Load |
|---|---|
| Session start / orientation | `AGENTS.md`, `RULES.md` |
| "What should this do?" | `+ SPEC.md` |
| Building or changing UI | `+ DESIGN.md` (`+ SPEC.md` for behaviour) |
| Writing/running tests | `+ TESTING.md` |
| Picking the next task, reporting progress | `+ PLAN.md` |
| Pre-ship verification | `+ SECURITY.md` |
| Deploying / releasing | `+ DEPLOY.md`, `+ SECURITY.md` |

---

## (c) Tech Stack

[TBD until SPEC approval]

Chosen after `SPEC.md` approval. Every row names the SPEC line that forces it. Versions are **target majors**; installed versions are recorded here as tasks install them. No version is claimed before it is installed.

| Layer | Choice | Target | Forced by |
|---|---|---|---|

---

## (d) Commands

[TBD until SPEC approval]

> Each row is ⬜ until it has actually run successfully in a session; then ✅. **Do not cite an unverified command as proof that anything works.**

| Purpose | Command | Verified |
|---|---|---|

---

## (e) Directory Map

[TBD until SPEC approval]

---

## (f) File Ownership & Boundaries

| File | Human owns | Agent drafts | Agent may edit freely |
|---|---|---|---|
| `SPEC.md` | ✅ | ✅ (initial draft) | 🚫 — propose diffs, human applies |
| `RULES.md` | ✅ immutable | 🚫 | 🚫 — may **suggest** additions only |
| `AGENTS.md` | ✅ | ✅ (initial draft) | 🚫 — propose diffs, human applies (exception: recording verified commands/versions in (c)/(d)) |
| `SECURITY.md` | ✅ immutable | proposal only | 🚫 — may **suggest** additions only |
| `DESIGN.md` | reviews | ✅ | after approval, with review |
| `TESTING.md` | reviews | ✅ | after approval, with review |
| `PLAN.md` | does **not** hand-edit | ✅ | ✅ — **agent-owned**, keep it current |
| `DEPLOY.md` | approves | ✅ | after approval, with review |

---

## Workflow Gates — verbatim from the founding prompt

> Workflow gates — do not skip, wait for my approval at each:
>
> 0. The eight documents are scaffolded and AGENTS.md is populated.
> 1. SPEC.md → I approve. Then the stack is chosen from the SPEC (AGENTS.md (c)–(e)) → I approve.
> 2. DESIGN.md (UI only) → I approve.
> 3. TESTING.md, then the SECURITY.md proposal (I write SECURITY.md) → I approve both before implementation begins.
> 4. PLAN.md (you generate it from SPEC + DESIGN + TESTING + SECURITY as atomic, ordered tasks; you own and update it) → I approve before implementation.
> 5. Implement one task at a time; update PLAN.md as you go; run tests per TESTING.md every iteration. "Done" means verifiable, not describable — prove it (tests, builds, migrations, deploys) before you claim anything is done. Stop for my review at the cadence recorded in PLAN.md.
> 6. Verify against SECURITY.md before anything ships — every control evidenced by a real run; I tick the boxes.
> 7. DEPLOY.md → I approve before the first deploy, release or store submission.
> 8. Deploy only per DEPLOY.md — dev/staging only; production, a public release or a store submission requires my explicit approval naming the target.
>
> If a gate check fails, report the failure and stop — do not retry silently.

### Gate status

| Gate | Status |
|---|---|
| 0. Documents scaffolded | ✅ {{DATE}} |
| 1. `SPEC.md` approved + stack approved | ⬜ |
| 2. `DESIGN.md` approved | ⬜ |
| 3. `TESTING.md` + `SECURITY.md` approved | ⬜ |
| 4. `PLAN.md` approved | ⬜ |
| 5. Implementation | ⬜ |
| 6. `SECURITY.md` verification | ⬜ |
| 7. `DEPLOY.md` approved | ⬜ |
| 8. Deploy (dev/staging; prod needs explicit approval) | ⬜ |

---

## Hard Rules — verbatim from the founding prompt

> - RULES.md and SECURITY.md are immutable — you may suggest additions when a new requirement surfaces something we hadn't anticipated, but only I add them.
> - Never expose secrets or commit the .env file (or any signing key, keystore, provisioning profile or credential file).
> - Always ask before changing the data structure, creating a migration, or changing a persisted on-device/on-disk format.
> - Always ask before adding, removing or upgrading a dependency.
> - Never guess anything unspecified — ask, or mark [NEEDS CLARIFICATION].
> - Load files just-in-time to keep context and API cost down.

---

## Git — verbatim from the founding prompt

> - Never commit on main/master. For each piece of work create a feature branch (feature/<name>), and once it is complete and verified, open a PR to the default branch.
> - You commit freely on feature branches, authored solely as the local git user (user.name / user.email) — never any agent identity: no custom author/committer, no signing as yourself, no Co-Authored-By trailers, no AI attribution in messages or PR bodies, no agent name in branch names.
> - Committing to main and merging are mine. You create the PR; I approve and merge it.
> - Never create git worktrees; work in the primary checkout.

---

## Definition of Done

A task is done only when it is **verifiable, not describable**. Before marking anything ✅ in `PLAN.md`:

1. Tests pass — paste the actual command output.
2. Build / typecheck / lint pass — paste the actual output.
3. The `SPEC.md` acceptance criteria the task claims are demonstrably met, named by AC number.
4. `PLAN.md` is updated in the same turn, with a task-log entry.

If a check fails: **report the failure and stop.** Do not retry silently, do not work around it, do not lower the bar.
