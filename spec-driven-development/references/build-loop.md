# Gate 5: The build loop (one task at a time)

**Who:** the coding agent runs in the repo, on the machine where the repo lives. The orchestrating
agent (if there is one) dispatches each task, reviews the result and reports to the human. When a
single agent does both jobs, it still follows the same loop and the same verification step.

## The micro-loop (per task)
1. **Pick:** the next ⬜ task in PLAN whose dependencies are ✅.
2. **Load:** AGENTS + RULES (always), then only what the task needs (SPEC sections it cites, DESIGN
   for UI, TESTING always, SECURITY if it touches a control).
3. **Write the tests first where the AC is clear.** Red, for the right reason.
4. **Implement** the smallest change that makes them green. Stay inside the task; anything else is a
   follow-up, not a "while I'm here".
5. **Run the per-iteration loop** (TESTING §8): full suite + typecheck + lint (+ E2E/platform checks
   when touched). Real output.
6. **Update PLAN:** tick the task naming its ACs, add the task-log entry, mark any AGENTS (d) commands
   that ran for the first time as ✅, and record installed versions in AGENTS (c).
7. **Commit** on the feature branch as the local git user. The message names the task and ACs (e.g.
   `T15: POST /api/bookings (AC5/6/7/27/38/40)`), with no AI attribution.
8. **Stop** at the review cadence boundary.

**Stop conditions inside a task** (report and wait, per RULES): a failing check it can't fix within
the task; an implied schema/data-structure/persisted-format change; a new dependency; a conflict
between docs; anything unspecified; scope beyond the task.

## Dispatching a task to a headless coding agent

The task prompt is the same whichever agent runs it:

```text
Read AGENTS.md and RULES.md first. You are at Gate 5 of this project's spec-driven workflow.

Do PLAN.md task <Tn> only. Follow AGENTS.md's Definition of Done and TESTING.md's per-iteration loop.
Stop conditions are in RULES.md: if you hit one (schema/migration change, a new dependency, a doc
conflict, anything unspecified, a failing check you can't fix inside this task), stop and report;
do not work around it.

When done: update PLAN.md (tick <Tn> with the ACs proven + a task-log entry), commit on the current
feature branch as the local git user with no AI attribution, and end with a report containing:
1. what changed (files), 2. the exact verification commands you ran and their real output (tail),
3. ACs proven, 4. decisions you made (mechanics only), 5. anything you need from the human.
```

Pipe it to the agent's non-interactive mode from the repo directory, for example:

```bash
cd <repo> && claude -p --permission-mode acceptEdits \
  --allowedTools "Bash,Read,Edit,Write,Glob,Grep" < task-prompt.txt     # Claude Code
cd <repo> && codex exec "$(cat task-prompt.txt)"                         # Codex CLI
cd <repo> && opencode run "$(cat task-prompt.txt)"                       # OpenCode
```

Check your agent's current flags. The agent needs file edits **and** a shell, because it must run the
tests. Grant no more than that. Run it on the machine where the repo lives (over SSH if it's remote).
One task per invocation keeps each review small and the context clean.

**After each dispatch, verify; don't trust the report:**
- `git log -1 --format='%an <%ae>%n%s%n%b'`: author is the local git user, no trailers.
- `git diff HEAD~1 --stat` and a skim of the diff for scope creep and unasked dependencies
  (`package.json`/lockfile changes not in the task = flag them).
- Re-run the test command and compare it with the claimed output.
- `check_docs.py --gate 5`.
- Report to the human: task, ACs proven, real test summary, decisions, flags. Keep it short.

## Reporting progress honestly
Report **proof, not throughput**: "T1–T7 done; ACs proven: 6 of 44 (14%); the invariant proven under
20× repeated 10-way contention." Task counts alone mislead (the demo's "only about seven percent
proven so far").

## When things go sideways
- **A test the agent wants to weaken or skip:** forbidden. It reports, and the human decides whether
  the test or the contract is wrong.
- **The agent objects to a human instruction** (e.g. drop the constraint for a demo): it states the
  objection once, complies within the stated bound, and logs it.
- **Flaky test:** a finding. Reproduce it with repetition, root-cause it, and fix it as a follow-up
  task (the demo's deadlock fix came from exactly this).
- **Mid-build SPEC change:** run change control (SKILL.md). New decision, SPEC diff applied by the
  human, ripple check, affected docs re-gated, PLAN updated.
- **Context getting heavy:** new session; the harness re-anchors from AGENTS → PLAN gate progress →
  last task-log entry. That is what the docs are for.
