# Intake and the question bank

This file is the "ask the right questions" engine. Three layers:

1. **Classification round:** always asked first; it picks the platform file and sizes the method.
2. **Platform round:** from `platform-<x>.md`; only the questions the requirement left open.
3. **SPEC question bank:** by SPEC section. These are not asked wholesale. They are the checklist the
   CLARITY GAPS table is built from; only the gaps that remain become questions.

## How to pick questions (applies to every round)

For every candidate question, in order:
1. **Does the requirement answer it?** Then it's a fact. Cite it (`R3`) and don't ask.
2. **Does an earlier decision answer it?** Then it's derived. Mark it `[DERIVED: from Dn]` and confirm
   it at the gate rather than asking now.
3. **Would a wrong guess be cheap to change later?** (copy text, colour, a folder name.) Then it's a
   mechanic. Decide it, mark it `[AGENT-PROPOSED]`, and surface it at the gate.
4. **Otherwise it's a question.** Put it in the batch.

Order batches so **upstream answers come first**: users → core flow → data → auth → integrations →
non-functionals → edge cases. Never ask about edge cases of a flow whose shape isn't decided.

Batch size: 3–5 questions per batch. A round is typically 2–4 batches. Tell the human the map before
round 1 starts: "~12 questions in 3 batches, about 5 minutes."

## Layer 1: classification round (one batch)

Ask only the ones the requirement doesn't answer.

| # | Question | Choices (recommended first; choose from the facts) |
|---|---|---|
| C1 | What kind of app is this? | Web app (browser) · Mobile app · Desktop app · Several surfaces (e.g. web + mobile) |
| C2 | Who uses it and roughly how many? | Just me / my household · A small known group (team, client staff, <100) · Public sign-up (hundreds+) · Other systems only (API/service, no humans) |
| C3 | What's the ambition for v1? | Real use by real users, built to last · Internal tool, good enough to rely on · Prototype to validate an idea · Learning project |
| C4 | Is anything already fixed? | Nothing; choose from the spec · Stack/language is fixed · Hosting/target is fixed · Must integrate with an existing system |
| C5 | Where should the project live? | A new directory here · On another machine/server · Existing repo (brownfield) · Somewhere else |

Follow-ups only when needed:
- C1 = several surfaces → which is primary? Does one surface do everything, or is there a split?
- C1 = mobile → see `platform-mobile.md` M1 (iOS / Android / both).
- C1 = "not sure" → ask about usage *context* instead: "at a desk / on the move / offline in the
  field / needs local files or hardware". Then recommend a platform with the reason in one line.
- C3 = prototype → offer the compressed method (one round, shorter docs; gates kept) and record the
  choice as a decision.
- C4 = fixed stack → record it as D-n now. Stack.md then works *within* that constraint and flags any
  SPEC line the fixed stack can't honour.

**Platform-picking help** (when the human asks "which should it be?"):

| Signal in the requirement | Leans |
|---|---|
| Used at a desk, many users, zero-install, frequent updates | Web |
| Camera, push, GPS, offline in the field, used on the move | Mobile |
| Local files, heavy local compute, hardware/USB, works offline, one machine | Desktop |
| "Anywhere, any device" with modest device needs | Web, responsive (PWA if install/offline matters) |
| No human UI | API/service/CLI (`platform-other.md`) |

## Layer 3: the SPEC question bank (by SPEC section)

Use it as a checklist when building the gaps table. ★ marks a question that is almost always a real
gap in a raw requirement.

### §1–2 Brief, goals, success
- ★ What problem does this solve, and for whom? What do people do today instead (the current process)?
- ★ What does success look like, measurably? (Pick 2–4 goals, each with a check: "no double bookings,
  ever" is a goal; "users like it" is not.)
- What is the **invariant**, the one guarantee the product exists for? (Double-booking never happens;
  money never moves twice; a note is never lost offline.) It gets the strictest proof in TESTING and
  usually drives the stack choice.
- Is there a deadline or budget? ("None" is a valid answer and gets recorded as a decision.)

### §3 Scope
- ★ What is explicitly *out* for v1? Offer the likely creep candidates as choices: SSO, payments,
  notifications, admin panel, multi-tenant, i18n, mobile app, import/export, analytics.
- Anything planned for v2 that v1 must not paint into a corner?

### §4 Roles
- ★ Which distinct roles exist, and what can each do that the others can't? Derive candidates from the
  requirement and confirm; never assume from generic words like "users" or "teams".
- Can one person hold several roles? Who creates accounts: self-sign-up, invite, admin-provisioned?
- Any role that acts *on behalf* of another (an admin booking for an employee)?

### §5–6 User stories and acceptance criteria
- For each core flow: what is the happy path, step by step?
- ★ Each limit, as a number: max sizes, durations, counts, windows. "Long meetings need approval" →
  how long, exactly?
- What happens at each boundary (exactly at the limit / one over)?

### §7 Data structure
- ★ What are the core entities and their lifecycles? Which have **states**? (Draft → submitted →
  approved…) The state model gets its own section and a transition table.
- ★ What is deleted versus kept? Soft delete? Retention period? Hard purge?
- History and audit: does anyone need to see who changed what?
- Time: which timezone(s)? Stored as UTC? Recurring items? DST?
- Money: currency, rounding, refunds? (Only if money exists.)
- Ownership: who owns each record, and who can see it?

### §8 Logical flow
- ★ For every state transition: who triggers it (user, admin, time, system), and what happens to
  related records and notifications?
- What runs on a schedule or in the background (expiries, reminders, cleanups, sync)?
- What happens when two people act on the same thing at once?

### §9 Interfaces (API / IPC / commands)
- Who consumes the API: only our own UI, or third parties too? (That decides versioning and docs.)
- Pagination, filtering, sorting needs on lists?
- Realtime? (Live updates, presence, collaborative edit.) Or is refresh fine?

### §10 Auth
- ★ How do people sign in? Email + password · Magic link/OTP · OAuth/SSO (which provider) · No auth
  (local-only app).
- Password policy, reset flow, MFA, session length, "remember me", sign-out everywhere?
- Account lifecycle: deactivation, deletion, what happens to their data?

### §11 Non-functional
- ★ Expected scale (users, records, requests) at launch and in a year? Order of magnitude only.
- Availability: does downtime matter? Backups and restore objective?
- Performance expectations that are *testable* (e.g. "day view renders in <1 s with 50 rooms").
- Accessibility floor (WCAG AA is the default recommendation), localisation/i18n, RTL?
- Privacy and regulation: personal data, health, finance, children, location → GDPR, HIPAA-like,
  PCI scope?
- Observability: what does the team need to see when it breaks (logs, errors, metrics, alerts)?

### §12 Edge cases
Generated, not asked: the agent lists them from the flows and asks only about those with no obvious
answer. Typical ones: concurrent edits, clock/DST, partial failure mid-flow, deleted owner, expired
session mid-action, offline then reconnect, duplicate submission, very large input, empty states.

### §13 Integrations
- ★ What external systems are involved? Email provider, payments, maps, calendar, SMS, storage, LLM
  APIs, existing company systems.
- For each one: what crosses the boundary, what happens when it's down, sandbox available?

### §14 Constraints
- Fixed stack, hosting, budget for running costs, licences, compliance, team skills, devices to
  support (OS versions, browsers).

### §15 Glossary
- Any domain word used in two senses? ("Booking" vs "reservation", "release" meaning two things.)
  Every overloaded word gets one meaning.

## Question batch patterns

**Good:** one decision per question, concrete choices, recommended first.
```json
{"questions": [
  {"question": "How should people sign in? (Recommended: email + password — R4 says staff use company email and there's no SSO mentioned.)",
   "choices": ["Email + password", "Magic link by email", "Google Workspace sign-in", "No sign-in — single-user local app"]},
  {"question": "Who creates accounts?",
   "choices": ["An admin invites/provisions them", "Anyone can sign up", "Sign-up limited to one email domain"]},
  {"question": "What's the longest booking allowed without approval, in minutes?"}
]}
```
The last question is open-ended because the answer is a number. Don't invent choices for numbers
unless there are natural tiers.

**Bad:** options in the text ("Should it be A, B or C?"); compound questions ("auth and roles?");
questions the requirement answers; adjectives as options; asking about edge cases before the flow is
decided.

## After each round

1. Fold every answer into the facts as `Dn` with its source.
2. Re-derive: answers often close other gaps. Remove those before the next round.
3. Show a one-line summary of the round's decisions before starting the next one, so the human can catch
   a misheard answer cheaply.
