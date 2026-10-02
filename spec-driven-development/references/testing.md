# Gate 3a: TESTING.md (how "done" gets proven)

The agent drafts TESTING.md and the human reviews it. It's approved **before** SECURITY, because
SECURITY's "verified by" lines must fit TESTING's rules.

TESTING.md is not a style guide. It is **the proof plan for SPEC**: every AC mapped to a named test at
a chosen level, with special handling for the invariant, time, external effects and the platform.
After approval it governs every implementation iteration.

## Philosophy (carried into the doc, adapted to the project)
1. **"Done" means verifiable, not describable.** Every claim is backed by output from a command run in
   the session that claims it. No paraphrased results, no "should pass".
2. **The suite proves the acceptance criteria, not the implementation.** Every SPEC AC maps to at
   least one named test. An AC with no test is an unmet AC, however complete the code looks.
3. **The invariant gets the strictest proof,** against the real thing, never a mock that can't
   exhibit the failure.
4. **A failing test stops the work.** It's reported, never deleted, skipped, weakened, or worked around.

## Procedure

### 1. Inventory what needs proving
From SPEC: every AC; the state model (every legal transition + every illegal one refused); every
background job; every external effect (email, push, webhook, file write); every boundary value; the
invariant; non-functional numbers that are testable (§11); edge cases E1… that have decided behaviour.

### 2. Choose levels
| Level | Runs against | Proves |
|---|---|---|
| Unit | Pure functions, no I/O | Rules, arithmetic, boundaries, state transitions, validation, copy selection |
| Integration | The real app layer + **real dependencies** (DB, mail capture, local store, filesystem) | Endpoints/IPC/commands, flows end to end, persistence, authorization, effects |
| E2E | The built app through its real UI (browser / app on a device / desktop window) | Only what exists once the UI is involved: rendering of domain state, focus, navigation, real device behaviour |
| Platform-specific | See the platform file | Packaging, update, migration from old versions, permission denial, offline sync |

**Choosing rule:** if it can be proven at a lower level, prove it there. **Name the E2E journeys
explicitly and cap them** (the reference build had five, "and only these"); everything else is cheaper and
more reliable at integration level.

### 3. The AC → test map (the heart of the doc)
A table per AC group, every AC in SPEC exactly once:

| AC | Level | Test proves |
|---|---|---|
| AC1 | integration | Overlapping booking on a held room is refused with a conflict response |
| AC8 | unit + integration | Each of the six violations is refused **with its own message** (six assertions, not one) |

Rules:
- "Test proves" states the observable outcome, not the mechanism.
- Compound ACs get **separate assertions per clause**.
- Boundaries are tested **on both sides** (exactly 60 accepted / 61 needs approval).
- Hybrid projects add a "Surface" column; a `[web, mobile]` AC needs proof on both or a stated reason
  one level covers both (e.g. a server-enforced rule proven once at API level).
- Manual checks are allowed only when automation is impossible or absurd (a store review, a physical
  device-only behaviour). Mark them `manual:` with the exact steps; they're re-run before each release.

`check_docs.py --gate 3` fails if any SPEC AC is missing from TESTING.md.

### 4. Special sections (include each one that applies)
- **The invariant test.** Against the real dependency under genuine concurrency (N ≥ 10 parallel
  identical requests → exactly one succeeds, N−1 get clean conflicts, and no raw DB errors reach the
  client). **A guard property: if the protection is removed, this test must fail.** A test that still
  passes without the constraint tests the wrong thing and is itself a defect. Run it repeatedly (e.g.
  20×) at least once per phase; intermittent failures are findings. (The reference build's deadlock only
  surfaced on repeated 10-way runs.)
- **Time.** Time is injected, never read from the system clock in domain code; one `now()` provider.
  Clocked tests set an instant, act, advance, and assert again. **No test sleeps.** Boundaries are
  tested on both sides. Include a DST-crossing case if times are stored UTC and rendered local.
- **State machine.** 100% of legal transitions, plus a test that each illegal one is refused.
- **External effects.** Email: captured by Mailpit/MailHog and asserted via its API; recipients are
  compared as a *set* (exactly these, no extras), the subject/product name, content rules (e.g. no
  links), no secrets. Push/webhooks: a capture endpoint or provider sandbox, same four assertions.
  Capture is reset between tests.
- **Background jobs.** Every job has an integration test, because a job that silently fails leaves
  state wrong with nothing visible.
- **Authorization.** An exhaustive table test: every route/command × every role → expected
  allow/deny. A new route without a row fails the test (it enumerates the router, not a hand list).
- **Data migration.** Every migration runs on a clean DB and on a DB seeded at the previous schema
  version. Desktop/mobile: open fixture files/stores from every released version.
- **Platform must-tests** from the platform file (kill-and-restore, offline sync, permission denied,
  update path, packaging smoke, the OS/device matrix).
- **Security tests** are listed in SECURITY.md's "verified by" lines and live in the same suite.
  TESTING.md says where (e.g. `tests/security/`).

### 5. Coverage expectations
- **100% of SPEC ACs** is the real coverage metric and the only one that gates a task.
- **100% of state-machine transitions** (legal + illegal refused).
- **Line coverage is reported, not targeted.** No test is written to move a percentage.

### 6. Structure, naming, data
- Where tests live (unit beside source; `tests/integration`, `tests/e2e`, `tests/security`).
- **Test names state the criterion and carry the AC number:** `refuses a booking that overlaps a held
  slot (AC1)`. A failure names its own contract.
- Factories/fixtures with defaults + per-test overrides; each test creates and cleans its own data;
  no order dependence.
- **No real credentials, personal data or real email addresses in fixtures, ever** (`example.com`).

### 7. Running tests
The exact commands from AGENTS (d), with a note that they're **unverified until PLAN T1 runs them**.
Local services that must be up first.

### 8. The per-iteration loop (copied into every build task)
After **every** task, before it is ticked in PLAN:
1. Full unit + integration suite.
2. Typecheck + lint.
3. E2E when the task touched a screen; platform checks when it touched packaging/update/permissions.
4. **Paste the real output.** Not a summary.
5. Tick the task in PLAN, naming the ACs it satisfied.

### 9. When a test fails
Report it and stop. Never permitted: deleting, skipping or `.only`-ing around a failing test; loosening
an assertion to match wrong behaviour; changing an AC to fit the implementation (SPEC is human-owned; a
criterion that seems wrong is raised, not edited); reporting done with a known failure outstanding. A
test that contradicts SPEC is a finding. Either the test or the contract is wrong, and only the human
decides which.

### 10. Clarify with the human (one batch, only real gaps)
- E2E budget: which journeys are worth a browser/device?
- CI: run on every PR? Which runner (GitHub Actions / self-hosted / none for now)?
- Physical-device or clean-VM checks before release (mobile/desktop): who and on what hardware?
- Performance tests: are §11 numbers enforced in CI or checked before release?
- Any test data the human can supply (real-shaped, anonymised)?

### 11. Gate
Run `check_docs.py --gate 3` (with SECURITY still unwritten, expect only the SECURITY checks to be
pending). Present: AC count mapped, level split, E2E journey list, special sections included, open
items. Wait for approval, then do SECURITY.

## Reference point (the reference build)
217 lines: philosophy (3 rules), levels table + "what belongs where", five E2E journeys "and only
these", coverage rules, the 44-AC map, the concurrency test section, clocked time, MailHog (four
assertions per email), structure/naming, commands, the per-iteration loop, the failure policy.
