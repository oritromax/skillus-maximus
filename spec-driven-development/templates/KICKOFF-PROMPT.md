# Kickoff prompt: portable founding prompt (any agentic harness)

Use this to run the whole pipeline inside a single coding agent with no orchestrator (Claude Code,
Codex, OpenCode, Cursor, Kiro…). Fill the three `{{…}}` slots and paste everything inside the fence as
the first message in an empty project directory. The harness scaffolds the eight files, copies the
gates and rules into AGENTS.md, and runs the SPEC process. Every later session starts from AGENTS.md.

```markdown
You are setting up a new project using the Spec-Driven Agentic Development method. Before writing any
application code, establish the document system and follow the gated workflow below.

Project: {{PROJECT NAME}}
Platform: {{web | desktop (which OSes) | mobile (iOS/Android) | API/CLI | hybrid: list surfaces}}
Requirement (verbatim, messy is fine):
{{REQUIREMENT}}

## The document system: eight root-level markdown files

- SPEC.md: what the system is + system-level how (data, interfaces, auth, flows). The source of truth. I own it.
- DESIGN.md: UI/visual contract only (screens, tokens, components, states, special cases). You draft, I review.
- RULES.md: immutable principles + ✅ Always / ⚠️ Ask first / 🚫 Never. I own it; you may suggest, never edit.
- AGENTS.md: your operating manual + the index to every other file. I own it.
- TESTING.md: the proof plan; every SPEC acceptance criterion mapped to a named test. You draft, I review.
- SECURITY.md: pre-ship checklist, every control with how it is verified. I own it; you propose, never edit.
- PLAN.md: the task board. You own it: create and maintain it, ticking tasks only when proven. I don't hand-edit it.
- DEPLOY.md: deployment/release runbook. You draft against my guardrails, I approve.

Precedence: RULES.md > SECURITY.md > SPEC.md > AGENTS.md. Any other conflict: stop and flag it.
Never guess anything unspecified: ask me, or mark it [NEEDS CLARIFICATION: …].

## Do this now

1. Scaffold the eight files (placeholders for those that fill at later gates). Populate AGENTS.md
   with: (a) the document index (what each file is and when to read it); (b) the context-loading
   policy (aware of every file, read each only when needed; always-on = AGENTS.md + RULES.md, kept
   short); (c) tech stack, (d) exact commands with a Verified column, (e) directory map, all marked
   [TBD until SPEC approval]; (f) file ownership. Copy the workflow gates, hard rules and git rules
   below into AGENTS.md verbatim. Future sessions start from AGENTS.md, not this prompt.
2. Write RULES.md: the precedence line; five principles (never guess; done = verifiable, not
   describable; gates are gates; a failed check stops the work; the spec is the contract); and the
   Always / Ask first / Never tiers derived from the hard rules and git rules below.
3. SPEC process, in this order:
   a. **Users first.** Identify the roles the requirement implies and confirm them with me. Never
      assume roles from generic words like "users".
   b. **Facts.** Number the requirement R1…Rn. List every concrete statement, quoted and cited, with
      no interpretation. Separate facts from desires and from delegation ("you'll figure it out" is a
      question for me, not licence; you decide mechanics only, after I confirm). Flag every
      contradiction as a decision for me. Name the invariant: the one guarantee the product exists for.
   c. **Clarification:** batched rounds of pointed questions, 2–4 concrete options each with your
      recommendation first, or let me write my own. At most two rounds. Ask nothing the requirement
      already answers. Cover, as gaps require: scope out, roles and account creation, every limit as a
      number, entities and their states, deletion and retention, time zones, concurrency, background
      jobs, auth, integrations and their failure modes, scale, a11y, privacy, and the
      platform-specific questions (web: rendering, devices, offline, realtime, hosting · desktop: OSes,
      where data lives, system access, distribution and updates, signing · mobile: platforms,
      distribution, backend, offline, device features, store rules, minimum app version).
   d. **CLARITY GAPS report**, mandatory before any draft: | # | What's unclear | Why it matters |
      Options | Blocks (SPEC sections) |. If it's empty, say "No unresolved items".
   e. **Draft SPEC.md:** brief, goals (GO1 = the invariant), scope in/out, roles, user stories,
      acceptance criteria (numbered AC1…, each Given/When/Then with concrete values, each testable),
      data structure with state model and retention, logical flow, interfaces with an access rule per
      route/command, auth flow, testable non-functional requirements, edge cases with decided
      behaviour, integrations with failure behaviour, constraints, glossary, open questions, and an
      appendix with the numbered requirement, the cited facts, and the decision register (D1…, each
      with its source).
   f. **Self-check:** if an implementer would have to guess anything, it becomes [NEEDS CLARIFICATION].
4. Stop and wait for my review of SPEC.md. Don't choose a stack, design, or write code.

## Workflow gates: don't skip any; wait for my approval at each

0. The eight documents are scaffolded and AGENTS.md is populated.
1. SPEC.md → I approve. Then the stack is chosen from the SPEC (AGENTS.md (c)–(e)), every choice citing the SPEC line that forces it → I approve.
2. DESIGN.md (UI only): screen inventory → clarity gaps → questions → named tokens with computed WCAG contrast → components → every interaction and domain state → exact behaviour-bearing copy → I approve.
3. TESTING.md (every AC mapped to a named test at the lowest level that proves it; the invariant tested against the real dependency under real concurrency, with a test that fails if the protection is removed; time injected, no sleeps; effects captured and asserted) → I approve. Then a SECURITY.md proposal (threat surface → cited out-of-scope declines → controls as "control — what it stops — verified by", per heading → open questions) → I write SECURITY.md and approve, before implementation begins.
4. PLAN.md (you generate it from SPEC + DESIGN + TESTING + SECURITY as atomic, ordered tasks, each one verifiable the moment it lands, every AC covered; ordering principle stated; review cadence agreed with me) → I approve before implementation.
5. Implement one task at a time; update PLAN.md as you go; run tests per TESTING.md every iteration. "Done" means verifiable, not describable: prove it (tests, builds, migrations, deploys) before you claim anything is done. Stop for my review at the agreed cadence.
6. Verify against SECURITY.md before anything ships: every control evidenced by a real run; I tick the boxes.
7. DEPLOY.md → I approve before the first deploy, release or store submission; the runbook is proven against staging first.
8. Deploy only per DEPLOY.md, to dev/staging only. Production, a public release or a store submission requires my explicit approval naming the target.

If a gate check fails, report the failure and stop. Don't retry silently.

## Hard rules: obey them at all times

- RULES.md and SECURITY.md are immutable. You may suggest additions when a new requirement surfaces something we hadn't anticipated, but only I add them.
- Never expose secrets or commit the .env file (or any signing key, keystore or credential file).
- Always ask before changing the data structure, creating a migration, or changing a persisted on-disk/on-device format.
- Always ask before adding, removing or upgrading a dependency.
- Never guess anything unspecified: ask, or mark [NEEDS CLARIFICATION].
- Load files just-in-time to keep context and API cost down.

## Git is human-owned. The local git user is the only author, never you

- Never commit on main/master. For each piece of work create a feature branch (feature/<name>), and once it is complete and verified, open a PR to the default branch.
- You commit freely on feature branches, authored solely as the local git user (user.name / user.email). Never use an agent identity: no custom author/committer, no signing as yourself, no Co-Authored-By trailers, no AI attribution, no agent name in branch names.
- Committing to main and merging are mine. You create the PR; I approve and merge it.
- Never create git worktrees.
```
