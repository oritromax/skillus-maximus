# Gate 1: SPEC.md (raw requirement → contract)

SPEC.md is human-owned: the agent drafts, the human approves and edits. It is the source of truth that
every later document derives from.

Two principles:
- **"A good plan makes implementation obvious. If someone has to guess, the plan is incomplete."** The
  same goes for a spec. A spec that leaves the implementer guessing is a wish. Every guess you'd have to
  make is a `[NEEDS CLARIFICATION]` owed to the human.
- **Understand before you execute.** No decomposition, no spec. Jumping to the template is how scope
  creeps and requirements get silently reinterpreted.

Inputs: the requirement as it arrived, numbered R1…Rn (verbatim, in Appendix A.1), the intake decisions
(A.3), and the platform file(s).

## Procedure

### 1. Start with the users
Identify who uses the system from what the requirement implies, then confirm with the human before going
further. Strategy follows from who you're building for. Defining roles is your job; never assume them
from generic words like "people", "users" or "teams". One question listing the candidate roles
(multi-select) plus "who creates accounts" usually settles it.

### 2. Decompose. Facts, not interpretation
1. **Pass 1, facts only.** List every concrete statement: numbers, entities, the current process,
   stated pains. Quote each and cite its `Rn`. No uncited facts and no interpretation yet. (Appendix A.2.)
2. **Separate facts from desires and delegation.** "You'll figure it out" hands you a decision. Accept
   it only after the human confirms explicitly, and only for mechanics. Until then it is a discussion
   question.
3. **Flag contradictions** (fast + cheap + perfect; self-service + zero effort; "simple" + a list of 20
   features). Each one is a decision for the human, never a compromise you pick silently.
4. **Find the invariant.** The one guarantee the product exists for. Name it as goal GO1. It drives the
   stack (Gate 1.5) and gets the strictest test (Gate 3).
5. **Derive scope from facts only.** A fact is stated in the requirement or resolved in discussion.
   Everything else goes to "out" or open questions, never to "in".

### 3. Clarification rounds
Build the candidate gap list from `intake.md` Layer 3 (the per-section bank) plus the platform file's
SPEC additions. Apply the four-step filter (answered? derived? cheap mechanic? → question). Then:
- Batched question rounds, 2–4 concrete options per question or open-ended for numbers/names.
- At most **two rounds**. Whatever is unresolved after that becomes `[NEEDS CLARIFICATION]`.
- When a question is really "which approach", frame the options as alternative answers to the same
  question so the choice is a decision, not a blank.
- Frame each accepted requirement as Given / When / Then where possible. Acceptance criteria fall out
  of that framing almost for free.
- Each answer → `Dn` in A.3 with its source.

### 4. CLARITY GAPS: mandatory before any draft
After the rounds and **before** drafting, show the report. It is the first thing the human reviews;
unknowns surfaced loudly beat guesses dressed as facts.

| # | What's unclear | Why it matters | Options I see | Blocks (SPEC sections) |
|---|---|---|---|---|

Rules:
- Every unresolved item goes here, including small ones.
- Items resolved in discussion do **not** appear (they're facts now).
- An empty list says so explicitly: "No unresolved items." Never skip the report.
- Anything on it becomes a `[NEEDS CLARIFICATION: …]` marker in the SPEC. Nothing on it is guessed.
- Offer a third round *only* for gaps that block the SPEC's core flow, and say that's what it is.

### 5. Draft SPEC.md
Use `templates/SPEC.md`. Section outline:

1. Brief · 2. Goals (GO1 = the invariant, each goal checkable) · 3. Scope (in/out) · 4. Roles (table:
role, can, cannot, created by) · 5. User stories (per role) · 6. Acceptance criteria · 7. Data structure
(entities, fields, constraints, state model + transition table, retention) · 8. Logical flow (per flow,
numbered steps; background jobs; notifications table) · 9. Interfaces (API endpoints / IPC commands /
CLI commands, with an access rule per route) · 10. Auth flow · 11. Non-functional requirements (each
testable) · 12. Edge cases (E1…, each with its decided behaviour) · 13. Integrations (each with
failure behaviour) · 14. Constraints · 15. Glossary · 16. Open questions · Appendix A: provenance
(A.1 requirement numbered, A.2 facts, A.3 decision register).

Plus the platform sections from the platform file (desktop: persisted format, process model, update
policy; mobile: lifecycle, permissions, push, versioned API + minimum version; hybrid: surface tags on
ACs).

**Acceptance criteria rules** (TESTING and the checker depend on these):
- Numbered `AC1`, `AC2`… in tables or a list. Numbers are never reused, and a removed AC stays as
  `ACn (withdrawn — Dm)`.
- Each is **Given / When / Then** with concrete values: "**Given** a booking of 61 minutes, **when**
  submitted without justification, **then** it is refused".
- Each is testable by a machine or a named manual check. If you can't say how it would be proven, it
  isn't an AC yet.
- Boundaries get their own ACs or explicit both-sides values (60 accepted / 61 needs approval).
- Hybrids: tag each AC with its surfaces `[web]`, `[mobile]`, `[web, mobile]`.

**Decision register rules:** `Dn | decision | source`. Human-made decisions only; agent mechanics go
in AGENTS (c) with a "forced by" line, not in the register.

**Preamble:** while in draft, open SPEC with the decomposition (users / facts summary / contradictions
and how each was decided / open questions). That's what the human reviews first. After approval, fold
it into the sections and keep Appendix A.

### 6. Self-check (before presenting)
- Would an implementer have to guess anything? Then it's a `[NEEDS CLARIFICATION]`, not a smooth
  sentence.
- Does every user story have at least one AC? Does every AC trace to a fact or decision?
- Does every state in the state model have entry triggers, exit triggers and a UI consequence named
  (DESIGN will need it)?
- Does every background job have a failure behaviour?
- Does every integration have a "when it's down" behaviour?
- Are scope-out items explicit enough that SECURITY can cite them as declines?
- Run `check_docs.py --gate 1`.

A spec with honest gaps beats a smooth one with silent assumptions.

### 7. Gate
Present the gate summary: counts (roles, stories, ACs, decisions, edge cases), the invariant, open
items, and the "what I'd challenge" list. Wait for approval. Don't start the stack, design or code.
After approval, set SPEC's status line to `✅ APPROVED (Gate 1)` with the date.

## What a finished SPEC looked like (the reference build)
472 lines; 28 decisions; 44 ACs in seven groups; 8 entities; a state machine; 8 email types; 30 edge
cases; Open questions reads "No unresolved items", with a table showing how each late gap was closed
by a decision. Its last line is the right posture: *"If anything here is wrong, it is wrong because a
decision was wrong, not because a gap was filled quietly."*
