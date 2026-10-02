# The method: the constitution

Everything else in this skill applies these rules. AGENTS.md carries the gates, hard rules and git
blocks **verbatim**, because future sessions start from AGENTS.md and not from this skill or the chat.

## The eight documents

All eight live at the repo root. They are flat on purpose: any harness finds them without configuration.

| File | What it is | Owner | Read it when |
|---|---|---|---|
| `AGENTS.md` | The agent's operating manual and the index to every other file | Human (agent drafts first version) | **Always**, at session start |
| `RULES.md` | Immutable principles + ✅ Always / ⚠️ Ask first / 🚫 Never | Human, immutable | **Always**, at session start |
| `SPEC.md` | What the system is plus the system-level how (data, interfaces, auth, flows). The source of truth | Human (agent drafts) | Any question about behaviour, scope, data, endpoints, auth or ACs |
| `DESIGN.md` | UI/visual contract only: screens, tokens, components, states, special cases. For no-UI projects, the interface contract (CLI UX, API ergonomics) | Agent drafts, human reviews | Touching UI, layout, styling, visual states, command output |
| `TESTING.md` | Test philosophy, levels, the AC → test map, the per-iteration loop, failure policy | Agent drafts, human reviews | Writing or running tests; every implementation iteration |
| `SECURITY.md` | Pre-ship checklist: threat surface, declines, controls, each with how it is verified | Human, immutable (agent proposes only) | Before shipping; when touching auth, secrets, input, data exposure |
| `PLAN.md` | Task board: atomic, ordered, verifiable tasks, plus gate progress and the task log | **Agent** owns; the human doesn't hand-edit | Picking the next task; reporting progress |
| `DEPLOY.md` | Deployment/distribution runbook | Agent drafts against human guardrails, human approves | Before any deploy, release or store submission |

Ownership in one line: the human owns SPEC, RULES, AGENTS and SECURITY (the agent drafts and suggests,
the human approves and edits). The agent drafts DESIGN and TESTING and the human reviews them. PLAN is
the agent's. DEPLOY is drafted by the agent and approved by the human.

**Why RULES and SECURITY are immutable to the agent:** they are the constraints the agent is checked
against. An agent that can edit its own constraints has none. The friction this creates (the agent must
hand over a *proposal*) is the design. Don't route around it by "just applying the obvious fix".

**Why PLAN is agent-owned:** it is the agent's working memory and progress log. A human hand-editing it
desynchronises the agent's model of what is done. The human steers PLAN through gate approval and
review comments, not edits.

## Precedence

```
RULES.md (safety)  >  SECURITY.md (immutable)  >  SPEC.md (the contract)  >  AGENTS.md (mechanics)
```
DESIGN, TESTING, PLAN and DEPLOY sit below SPEC. When they conflict with it, SPEC wins and the
conflicting doc is wrong. Any conflict the ordering doesn't resolve: **stop and flag it, don't guess.**
Anything unspecified gets asked, or marked `[NEEDS CLARIFICATION: …]`.

## Markers

| Marker | Meaning | Allowed past gate? |
|---|---|---|
| `[NEEDS CLARIFICATION: …]` | A decision the human owes. Nothing on it gets guessed | Only if the human explicitly accepts it as a known open item at the gate, and only when no task in the next phase depends on it |
| `[AGENT-PROPOSED: … — reason]` | The agent added something not derivable from SPEC or the discussion | Yes, once the human accepts it (the marker is then removed) |
| `[TBD until <gate>]` | Deliberately deferred to a known later gate | Yes, until that gate |
| `[DERIVED: from Rn/Dn]` | A rule the agent derived rather than read; confirmed at the gate | Yes, after confirmation |

## The gates (verbatim block for AGENTS.md)

> Workflow gates. Don't skip any; wait for my approval at each:
>
> 0. The eight documents are scaffolded and AGENTS.md is populated.
> 1. SPEC.md → I approve. Then the stack is chosen from the SPEC (AGENTS.md (c)–(e)) → I approve.
> 2. DESIGN.md (UI only) → I approve.
> 3. TESTING.md, then the SECURITY.md proposal (I write SECURITY.md) → I approve both before implementation begins.
> 4. PLAN.md (you generate it from SPEC + DESIGN + TESTING + SECURITY as atomic, ordered tasks; you own and update it) → I approve before implementation.
> 5. Implement one task at a time; update PLAN.md as you go; run tests per TESTING.md every iteration. "Done" means verifiable, not describable: prove it (tests, builds, migrations, deploys) before you claim anything is done. Stop for my review at the cadence recorded in PLAN.md.
> 6. Verify against SECURITY.md before anything ships: every control is evidenced by a real run, and I tick the boxes.
> 7. DEPLOY.md → I approve before the first deploy, release or store submission.
> 8. Deploy only per DEPLOY.md, to dev/staging only. Production, a public release or a store submission requires my explicit approval naming the target.
>
> If a gate check fails, report the failure and stop. Don't retry silently.

## Hard rules (verbatim block for AGENTS.md)

> Hard rules. Obey them at all times:
>
> - RULES.md and SECURITY.md are immutable. You may suggest additions when a new requirement surfaces something we hadn't anticipated, but only I add them.
> - Never expose secrets or commit the .env file (or any signing key, keystore, provisioning profile or credential file).
> - Always ask before changing the data structure, creating a migration, or changing a persisted on-device/on-disk format.
> - Always ask before adding, removing or upgrading a dependency.
> - Never guess anything unspecified. Ask, or mark [NEEDS CLARIFICATION].
> - Load files just-in-time to keep context and API cost down.

## Git (verbatim block for AGENTS.md)

> Git is human-owned. The local git user is the only author, never you:
>
> - Never commit on main/master. For each piece of work create a feature branch (feature/<name>), and once it is complete and verified, open a PR to the default branch.
> - You commit freely on feature branches, authored solely as the local git user (user.name / user.email). Never use an agent identity: no custom author/committer, no signing as yourself, no Co-Authored-By trailers, no AI attribution in messages or PR bodies, no agent name in branch names.
> - Committing to main and merging are mine. You create the PR; I approve and merge it.
> - Never create git worktrees; work in the primary checkout.

## Definition of Done (verbatim block for AGENTS.md)

A task is done only when it is **verifiable, not describable**. Before marking anything ✅ in PLAN.md:
1. Tests pass. Paste the actual command output.
2. Build, typecheck and lint pass. Paste the actual output.
3. The SPEC acceptance criteria the task claims are demonstrably met, named by AC number.
4. PLAN.md is updated in the same turn, with a task-log entry (what was done, what was decided, what
   input the human gave).

If a check fails, **report the failure and stop.** Don't retry silently, work around it, or lower the bar.

## Context-loading policy (for AGENTS.md (b))

- The agent knows every file exists but reads each only when the operation needs it.
- Always-on: AGENTS.md + RULES.md, both kept short. RULES.md stays under ~60 lines.
- Never bulk-read the doc set "for context".

| Operation | Load |
|---|---|
| Session start / orientation | AGENTS, RULES |
| "What should this do?" | + SPEC |
| Building or changing UI | + DESIGN (+ SPEC for behaviour) |
| Writing or running tests | + TESTING |
| Picking the next task, reporting | + PLAN |
| Pre-ship verification | + SECURITY |
| Deploying / releasing | + DEPLOY, + SECURITY |

## RULES.md: what belongs in it

Principles (5, short), then three tiers. The template carries the proven set. Add project-specific
lines only when SPEC creates a new risk class. Examples: "⚠️ Ask before any change to the sync
protocol" for a local-first app; "🚫 Never ship a build signed with the debug key" for mobile;
"🚫 Never send a push notification to real users from a dev build".

Keep it short. If RULES.md grows past one screen it stops being read, and always-on context
becomes always-ignored context.

## Why this works (for when the human asks, or a doubter needs answering)

- **Gates move every decision to the cheapest moment to make it.** Changing a line in a SPEC is
  minutes; changing a shipped data model is weeks.
- **Explicit unknowns beat silent assumptions.** An agent fills every gap with the most plausible guess.
  Plausible is not correct, and the guesses compound.
- **Verifiable-not-describable** turns an agent's confidence into evidence. Agents describe success
  fluently whether or not it happened.
- **Small always-on context with just-in-time loading** keeps cost down and keeps the rules from
  drowning in the spec.

**Honest counter-view (say it, don't hide it):** this is heavy for a weekend hack. For a throwaway,
use a spike. The method pays off when the thing has to keep working, has more than one user, or will be
built over more than a few sessions. For a small project, compress it rather than skip it: one
clarification round, a shorter SPEC, TESTING and SECURITY in one sitting. Keep the gates and the
verification.
