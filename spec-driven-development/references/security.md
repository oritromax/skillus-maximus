# Gate 3b: SECURITY.md (proposal → human-written checklist)

SECURITY.md is **human-owned and immutable to the agent.** RULES.md's 🚫 Never forbids the agent from
editing it, so the agent produces a **proposal**: it never writes, stages or commits SECURITY.md, and
implements nothing after presenting. The human reviews and writes the file from the proposal. (An
orchestrating agent may write the file *after* the human explicitly says "write it as proposed" or
"write it with these edits". That instruction is the human's authorship act. The coding agent never
writes it.)

Scope: the security of **this** system as SPEC defines it. No generic enterprise checklist and no OWASP
dump. Anything SPEC excluded gets a cited N/A, never a recommendation to add it back.

Inputs: SPEC (all of it, with roles §4, data §7, flows §8, interfaces §9, auth §10, NFRs §11, edge
cases §12, integrations §13, scope §3, decisions A.3, and the access/security ACs), AGENTS + RULES,
the approved TESTING.md (verification methods must fit it), and the platform file's SECURITY section.

## Procedure

### Step 1: Threat surface (before any checklist)
Enumerate every entry point an attacker can touch, from SPEC flows, interfaces, emails/push, jobs,
IPC/deep links (desktop/mobile), and update channels. Classify each: unauthenticated / role-X /
admin / system / local-user. For each: the top risks **this system** actually has and the worst
realistic outcome (impersonation, data disclosure, privilege escalation, resource hijack, inbox abuse,
RCE via update). Each later control points back to a risk it kills.

| # | Entry point | Who can reach it | Top risks here | Worst realistic outcome |
|---|---|---|---|---|

### Step 2: Scope honesty (the declines register)
From SPEC §3 (out of scope) and the decisions, list what this system consciously does **not** have,
each with its cite, and one line on how the exclusion shrinks the attack surface (no SSO → no IdP trust
boundary; no links in email → no phishing-lookalike vector; no uploads → no file-handling class). Where
a heading ends up with nothing applicable, say so with the cite; don't pad it.

### Step 3: Controls, under fixed headings
Every control is a checkbox line with three parts:

`- [ ] <control, concrete and specific to this system> — <what it stops (risk # from Step 1, SPEC AC/D)> — verified by <how, per TESTING.md>`

Headings, in this order (skip none; an empty heading says N/A with a cite):
1. **Authentication & session handling**: hashing algorithm and parameters, password policy, reset
   flow, lockout, session token storage, cookie/token flags, rotation, expiry, revocation.
2. **Authorization / access control per role**: the role table as server-side enforcement on every
   route/command; object ownership (IDOR/BOLA); admin actions logged.
3. **Input validation & output encoding**: every input class; every place user content renders
   (UI, email, PDF, logs); disclosure rules (what one user must never see about another's data).
4. **Rate limiting & abuse protection**: auth, reset, expensive endpoints, notification volume; only
   what the flows imply.
5. **Logging & PII policy**: audited events, what is deliberately **not** logged, retention and hard
   delete, where PII lives.
6. **Data at rest / in transit**: hashing, encryption where needed, TLS stance, secrets handling
   (`.env` discipline is baseline; don't restate it as new), backups.
7. **Third-party integration trust boundaries**: per integration, what crosses the boundary and
   what the prod swap changes.
8. **Dependency & supply chain**: pinned versions, lockfile, review-before-add (RULES ⚠️), audit
   command and threshold. Right-sized; no vendor audit theatre.
9. **Platform surface** (from the platform file, when applicable): web headers/CSRF/CORS; desktop
   IPC allow-list, signing, update integrity, keychain; mobile token storage, deep links, bundle
   secrets, store privacy disclosures.

"Verified by" must name a real mechanism from TESTING (an integration test, a clocked test, a header
assertion, an audit command, a manual pre-release check with steps). "Reviewed" or "best practice"
is not verification. `check_docs.py` fails any control line without "verified by".

### Step 4: NEEDS CLARIFICATION batch
Anything security can't wait on that SPEC leaves open (hashing parameters, session storage, prod email
provider, TLS termination, extra rate limits, at-rest encryption, crash-report consent): batch them as
questions, 2–4 concrete options each, recommended first with a one-clause reason. Label them NC-1…, and
record each answer as "Decisions taken at Gate 3" inside the proposal.

### Step 5: Output contract
Deliver, in this order:
1. The threat-surface table.
2. The declines register (cited N/As).
3. The proposal in SECURITY.md's exact shape (`templates/SECURITY.md`): baseline, threat surface,
   declines, headings 1–9 with three-part checkbox lines, Decisions taken at Gate 3, verification rule.
4. The NC batch (or "none").

Then **stop**. Don't edit SECURITY.md, don't implement anything, and propose no next steps beyond
waiting for the human's review.

### Step 6: Gate
Once the human writes (or explicitly instructs the write of) SECURITY.md: run `check_docs.py --gate 3`.
Present: control count per heading, declines count, NC resolved, and every control traced to a risk.
Gate 3 closes when **both** TESTING and SECURITY are approved.

## Reference point (the reference build)
173 lines, 63 controls, NC-1…NC-8 resolved, a baseline section in force from day one, a threat surface
table, a "consciously out of scope" register, eight headings, and a closing verification rule:
*"Nothing ships until every applicable box is checked **and the check was actually performed**, not
assumed."* The class's best moment: the agent flagged an implied schema change while proposing
controls, asked first, and got live approval.
