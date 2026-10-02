---
name: spec-driven-development
description: Take a raw project requirement to an approved, verifiable eight-document spec (AGENTS, RULES, SPEC, DESIGN, TESTING, SECURITY, PLAN, DEPLOY) through human-gated interviews, then drive the build one proven task at a time. Use when starting a new web, desktop, mobile, API/CLI or hybrid project, when asked to "spec this out" or "turn this idea into a spec", or when resuming a repo that already has these documents.
version: 1.0.0
author: Nidal Siddique Oritro [ https://github.com/oritromax ]
license: MIT
tags: [spec-driven, agentic-development, requirements, specification, testing, security, planning, web, desktop, mobile]
---

# Spec-Driven Agentic Development

This skill takes a raw project requirement, messy and half-formed the way requirements really arrive,
and turns it into an approved, verifiable document set. It then drives the build through gates.

The core claim is simple: **an agent is only as good as the contract it builds against.** The human
decides every unknown *before* any code exists, and every "done" is backed by output that actually ran.
A description of success doesn't count.

The method has been run end to end through planning on a real reference build, a multi-user
meeting-room booking system. Before any feature code was written, it had 28 human decisions, 44
acceptance criteria, 63 security controls and 45 planned tasks. Implementation then ran task by task
against that plan. The numbers quoted throughout the references come from that build.

## When to Use

**Use it for:**
- A new app or project, starting from an idea or a client ask. Typical phrasings: "kick off X", "I'm
  starting a new project", "spec this out", "turn this idea into a spec", "what should we decide
  before building".
- Any platform: web, desktop, mobile, API/CLI/service/library, or hybrids such as web + mobile or a
  desktop app with a sync backend.
- Resuming a repo that already has the eight documents and gate tables ("where are we", "what gate
  are we at", "continue the build").
- Changing an approved spec mid-flight (see Change control).

**Don't use it for:**
- A one-off implementation plan for a feature in a repo without this document system. A plain task
  plan is enough there.
- A throwaway spike to answer "does X even work?" Run the experiment instead.
- Adopting the method on an existing codebase is covered separately in `references/brownfield.md`.
  That path is adapted from the greenfield method and less proven.

## Roles and tools

This skill assumes two parties plus, optionally, a third:

- **The human** owns the decisions. They answer questions, approve gates, own the protected documents
  and merge code.
- **The orchestrating agent** (you, while this skill is loaded) runs the interviews, drafts documents,
  runs the checks and reports.
- **A coding agent** runs implementation in the repo from Gate 5 on. It can be the same agent, or a
  separate headless coding agent such as `claude -p`, `codex exec` or `opencode run`.

**The ask tool.** Interviews work best through a structured-question tool, meaning anything that
presents a question with selectable options. If your harness doesn't have one, ask numbered questions
in chat with lettered options, and accept free-text answers. The interview rules below apply either way.

## The pipeline

| Gate | Phase | Artifact(s) | Owner | Load |
|---|---|---|---|---|
| — | Intake: classify the platform, shape and location | intake decisions (become D1…) | human answers | `references/intake.md` + `references/platform-<x>.md` |
| 0 | Scaffold the eight files | all 8, AGENTS.md (a)(b)(f) filled | agent | `scripts/scaffold.py`, `references/method.md` |
| 1 | SPEC: users → facts → clarify → CLARITY GAPS → draft | `SPEC.md` | **human** owns, agent drafts | `references/spec.md` |
| 1.5 | Stack: every choice forced by a SPEC line | `AGENTS.md` (c)(d)(e) | human approves | `references/stack.md` |
| 2 | DESIGN (UI or interface only) | `DESIGN.md` | agent drafts, human reviews | `references/design.md` |
| 3 | TESTING, then the SECURITY proposal | `TESTING.md`, `SECURITY.md` | TESTING: agent drafts. SECURITY: **human** writes it from the agent's proposal | `references/testing.md`, `references/security.md` |
| 4 | PLAN: atomic, ordered, verifiable tasks | `PLAN.md` | **agent** owns | `references/plan.md` |
| 5 | Build loop, one task at a time | code + PLAN task log | agent; human reviews at the agreed cadence | `references/build-loop.md` |
| 6 | SECURITY verification pass | evidence report → human ticks boxes | agent runs, human ticks | `references/ship.md` |
| 7 | DEPLOY runbook | `DEPLOY.md` | agent drafts, human approves | `references/ship.md` |
| 8 | Deploy to dev/staging; production only on explicit approval | release record in PLAN | human approves production | `references/ship.md` |

**Gates are hard stops.** Nothing past a gate starts until the human says "approved" for that gate,
and that includes drafting the next document. Approval is given per gate, never as "approve the rest".

**Load references just in time.** Read only the reference for the phase you're in, plus the platform
file. The body of this file is enough to orient; the references hold the procedures.

## Operating model

- **Gates 0–4 are document work.** The orchestrating agent interviews, drafts the files directly in
  the project directory, runs the checker and presents the gate. This is conversation work, so keep it
  with the agent that is talking to the human.
- **Gate 5 onward is code.** The coding agent works in the repo, on the machine where the repo lives,
  with `AGENTS.md` as its entry point. Dispatch one task per invocation, then review the diff and the
  real test output yourself before reporting. Details are in `references/build-loop.md`.
- **Portable mode.** To run the whole pipeline inside a single coding agent with no orchestrator, fill
  in `templates/KICKOFF-PROMPT.md` and paste it as the first message in an empty project directory. It
  is the self-contained founding prompt and drives the same files and gates.

## Interview mechanics (how to ask the right questions)

1. **Keep batches small:** at most 5 questions per batch and at most 4 options each, with the
   recommended option first. Always allow a free-text answer. Put options in the options field, never
   in the question text.
2. **Batch only independent questions.** If answer A changes question B, ask A first.
3. **Never ask what the requirement already answers.** Quote it as a fact with its `Rn` cite instead.
   Interview fatigue is how humans start rubber-stamping.
4. **Make options concrete alternatives, not adjectives.** "Email + password / Magic link / Google
   sign-in" works; "Simple / Secure / Flexible" doesn't.
5. **Recommend from the facts gathered so far, never from habit.** When the reason isn't obvious, put
   one clause of it in the question.
6. **Every answer becomes a numbered decision `Dn`** in SPEC Appendix A.3, with its source (e.g.
   "intake Q3", "SPEC round 2 Q1"). Decisions carry the same weight as requirement facts.
7. **"You decide" is delegation, not licence.** Accept it only for *mechanics* (library choice, folder
   layout, naming), and only after the human confirms explicitly. Behaviour is never delegated
   silently.
8. **Run at most two clarification rounds per document.** A round is one pass over the open gaps, and
   it may take several batches. Anything still open after that becomes `[NEEDS CLARIFICATION: …]`,
   never a guess.
9. **Tell the human where they are between batches,** e.g. "SPEC round 1, batch 2 of ~3: auth and
   data." A long interview without a map feels endless.
10. **If an answer batch comes back partial,** record what was answered, add the rest to the gaps
    table and stop. Don't fill in the blanks.

The full question bank is in `references/intake.md`: the classification round, the per-SPEC-section
bank that the gaps table is built from, and a filter for choosing which questions to ask. The platform
files add their own rounds.

## Procedure

### Step 0: Intake (before any file exists)
1. Read the requirement and number its statements R1…Rn, keeping the text verbatim. It becomes SPEC
   Appendix A.1. A one-sentence requirement is fine, because the interview does the work.
2. Load `references/intake.md` and run the **classification round**: platform, who uses it and how
   many, ambition for v1, anything already fixed, and where the project lives.
3. Load the matching platform file: `references/platform-web.md`, `platform-desktop.md`,
   `platform-mobile.md`, or `platform-other.md` (API/CLI/service/library). For a hybrid, load one file
   per surface plus the hybrid section of `platform-other.md`. Ask only the platform questions the
   requirement left open.

### Step 1: Scaffold (Gate 0)
```bash
python3 <skill-dir>/scripts/scaffold.py <project-dir> "<Project Name>" <web|desktop|mobile|api|cli|hybrid[:web,mobile]> \
  [--requirement-file requirement.txt]
```
This creates the eight docs from `templates/`, a platform-specific `.gitignore` and an `.env.example`.
It runs `git init -b main` and checks out `feature/spec-docs`. It never commits, refuses to overwrite
existing docs, and warns if `git config user.name`/`user.email` is unset. Fix that before any commit.

Then finish AGENTS.md sections (a) index, (b) loading policy and (f) ownership; the template carries
most of them. Sections (c) stack, (d) commands and (e) directory map stay `[TBD until SPEC approval]`.
Write the numbered requirement into SPEC Appendix A.1 and the intake decisions into A.3.

### Step 2: SPEC (Gate 1)
Follow `references/spec.md` in order: users first → facts with cites → contradictions as decisions →
clarification rounds → **CLARITY GAPS table (mandatory, shown before any draft)** → draft →
self-check → gate.

### Step 3: Stack (Gate 1.5)
Follow `references/stack.md`. Every row of AGENTS.md (c) names the SPEC line that forces it. The
commands table starts with every row ⬜, and a row becomes ✅ only after the command has actually run.

### Step 4: DESIGN (Gate 2)
Use `references/design.md` plus the platform file's DESIGN section. For projects with no UI,
DESIGN.md becomes the interface contract (CLI UX or API ergonomics); see `platform-other.md`.

### Step 5: TESTING, then SECURITY (Gate 3)
Do `references/testing.md` first, because it maps every AC to a test. Then do
`references/security.md`: the agent produces a *proposal* and the human writes SECURITY.md. That
ownership rule is the point.

### Step 6: PLAN (Gate 4)
Follow `references/plan.md`. Agree the **review cadence** for Gate 5 here (per task, per phase, or at
named checkpoints) and record it in PLAN.md.

### Step 7: Build (Gate 5)
Follow `references/build-loop.md`: one task per coding-agent invocation, reviewed before reporting.

### Step 8: Ship (Gates 6–8)
Follow `references/ship.md`. A production deploy or store submission needs the human's explicit
approval naming the target.

### At every gate
1. **Run the checker.** It is mechanical, not a matter of judgment:
   ```bash
   python3 <skill-dir>/scripts/check_docs.py <project-dir> --gate N
   ```
   It always checks that all eight files exist and counts leftover template slots and open markers.
   From gate 1 it checks AC numbering and Given/When/Then shape. From gate 3 it checks that every SPEC
   AC is mapped in TESTING and every SECURITY control has a verification method. From gate 4 it checks
   that every AC is covered by a PLAN task. From gate 5 it flags unverified commands and reports the
   share of ACs proven, and from gate 6 it flags unticked security boxes. Show its real output. A FAIL
   blocks the gate presentation: fix it, or explain why it stands.
2. **Present a gate summary:** what the document decides, the counts (decisions, ACs, screens, tests,
   controls, tasks), the open items and the checker output. Don't paste the whole file; the human reads
   the file. Add a "what I'd challenge" list of 2–4 items naming the weakest decisions in the document.
3. **Wait for explicit approval.** Then flip the document's status line and the gate row in AGENTS.md
   (and in PLAN.md from Gate 4), and commit on the feature branch as the local git user.

## Resuming a project

1. Read only `AGENTS.md` and `RULES.md`, and find the gate-status table.
2. At Gate 4 or later, also read the gate progress in `PLAN.md` and the last task-log entry.
3. Run `check_docs.py --gate <current>`.
4. Report the current gate, the last verified task, the open `[NEEDS CLARIFICATION]` items and the
   next action. Never re-run an approved gate unless the human reopens it.

## Change control (mid-flight)

The spec is the contract, and code never gets ahead of it.
- A new fact or a changed mind becomes a new decision `Dn+1`, proposed as a SPEC diff. **The human
  applies it.**
- Run the ripple check every time: SPEC → TESTING AC map → SECURITY threat surface → PLAN tasks →
  DESIGN screens and states. List the documents that must re-gate, and re-gate only those.
- If a task turns out to imply a schema or data-structure change, stop and ask (hard rule), however
  small the change. In the reference build, the agent flagged an implied schema change while drafting
  security controls and got approval before touching anything. That is the method working as designed.
- If the agent disagrees with a human override, it records the objection in the task log and
  complies within the limit the human set (e.g. "drop it, add it back when I say").

## Pitfalls (each one happened, or nearly did, in the reference build)

- **Drafting before decomposing.** Jumping straight to the SPEC template silently reinterprets the ask.
  Always do users → facts → contradictions → questions first.
- **Treating "you'll figure it out" as licence.** The reference build recorded it as a decision: *not*
  licence. The agent decides mechanics only, and behaviour gaps get asked.
- **Mistaking throughput for proof.** Seven tasks green isn't the product proven; at that point the
  reference build was "only about seven percent proven". Report what is *proven* against ACs, not the
  number of tasks closed.
- **Running tasks back to back with no human pause.** Chaining several tasks without review builds up
  proof debt that a later review has to repay. Agree the cadence at Gate 4 and keep it.
- **Letting a mock stand in for the invariant.** The product's defining guarantee is proven against
  the real thing (real database, real concurrency, real device), with a guard test that *fails if the
  protection is removed*. In the reference build the database constraint was dropped deliberately, and
  the tests caught it.
- **Trusting one green concurrency run.** The reference build hit a deadlock that only showed up on
  repeated runs at 10-way contention. Run race tests repeatedly, and treat a flake as a finding, not
  noise.
- **Claiming commands before they ran.** The AGENTS.md commands table has a Verified column, and each
  row stays ⬜ until the command has run in a session.
- **The agent writing a human-owned file.** SECURITY.md and RULES.md get proposals only. The agent's own
  rules forbid the write, and that friction is deliberate.
- **Dependencies added unasked.** One coding agent installed about 50 packages (554 MB) without asking.
  Dependency changes are always ⚠️ Ask first.
- **Leaving distribution to the end (desktop/mobile).** Signing, notarization, store review and
  provisioning take calendar time, not code. Phase 0 of the PLAN pushes a signed "hello world" through
  the real pipeline.
- **Forgetting that mobile clients live forever.** Old app versions keep calling the API. Ship a
  versioned API and a minimum-supported-version check from the first release.
- **Silent failures in background work.** A scheduled job that dies leaves state wrong with nothing in
  the UI to show it. Every job gets an integration test and a visible failure signal.
- **Agent identity in git.** No co-author trailers, no agent as author, and no agent name in branch
  names. The human's git identity owns the history.
- **Options written into the question text.** They can't be selected; put them in the options.

## Files

- `references/method.md`: the constitution. The document system, ownership, precedence, markers,
  gates, hard rules, git rules and Definition of Done, including the verbatim blocks AGENTS.md carries.
  Read it at Gate 0 and whenever a rule is in question.
- `references/intake.md`: the classification round, the full question bank by SPEC section, and the
  rules for asking. Read it at intake and while building every gaps table.
- `references/platform-web.md`, `platform-desktop.md`, `platform-mobile.md`, `platform-other.md`
  (API/CLI/service/library, hybrids, local-first): per-phase additions covering intake questions, SPEC
  sections, stack options, DESIGN, TESTING tooling, SECURITY surface, PLAN Phase 0 and
  DEPLOY/distribution. Read the matching file at intake and again at each gate.
- `references/spec.md`, `stack.md`, `design.md`, `testing.md`, `security.md`, `plan.md`,
  `build-loop.md`, `ship.md`: one file per phase, each with its procedure. Read each at its gate.
- `references/brownfield.md`: adopting the method on an existing codebase.
- `templates/`: the eight document skeletons, plus `KICKOFF-PROMPT.md`, the portable founding prompt.
- `scripts/scaffold.py` creates the project and documents. `scripts/check_docs.py` runs the mechanical
  gate checks. Both use only the Python 3 standard library.

## Status of the method

Gates 0–5 have been run in practice on the reference build. Gates 6–8 (`references/ship.md`) and the
brownfield path are written from the same rules but haven't yet been run end to end, and both files
say so. Improvements from real use belong in these files.
