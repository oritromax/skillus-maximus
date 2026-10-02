# Gate 1.5: Stack, commands, directory map (AGENTS.md (c)–(e))

The stack is chosen **after** SPEC approval, from the SPEC. Choosing it earlier makes the spec bend to
the tool. Stack is *mechanics*: the agent proposes and the human approves or overrides any row.

## Procedure
1. **List the forcing lines.** Walk SPEC for anything that constrains tech: the invariant (GO1), data
   constraints (§7), concurrency, offline/sync, realtime, platform targets, integrations, hosting
   constraints (§14), intake decisions (fixed stack, C4).
2. **For each layer, propose one choice and name the SPEC line that forces it.** If nothing forces it,
   say "preference: <reason>" and offer the alternative. Use the platform file's stack table as the
   option space.
   - Good: "PostgreSQL. §7 requires overlap prevention enforced by the database (GO1, AC2); that needs
     `EXCLUDE USING gist`. MySQL and SQLite can't express it."
   - Bad: "PostgreSQL. Robust and popular."
3. **Flag what is NOT interchangeable.** The reference build's stack table led with "PostgreSQL is not
   interchangeable", because swapping it would turn the product's guarantee into a race condition.
4. **Verify current versions** (package registry, release pages) and write the *target major* only.
   Pinned versions are recorded as tasks install them. **No version is claimed before it's installed.**
5. **Ask the human** in one question batch: approve the stack table as proposed / change specific
   rows / discuss. If the human has preferences (Biome over ESLint, Drizzle over Prisma), they're overrides,
   recorded as "human override" in the table.
6. **Write the commands table (d)**, every row ⬜ with a Verified column. Include: start local
   services, install, dev run, build, test all, test single file, E2E, lint, format, typecheck,
   security audit, DB generate/migrate/seed, run a job by hand, package/sign (desktop/mobile).
7. **Write the directory map (e)**, marked "Planned", plus the two-files-are-copies rule if it applies
   (e.g. `tokens.css` is DESIGN §2 verbatim; the invariant migration implements SPEC §7 literally).
8. Run `check_docs.py --gate 1`, present, wait for approval.

## Sensible defaults (offer them, don't impose them)
- TypeScript strict, Biome for lint+format, Vitest, Playwright for web E2E.
- PostgreSQL in docker compose for anything multi-user; real services in tests (no DB mocks).
- Mailpit/MailHog for email capture locally.
- Drizzle (raw SQL migrations keep constraints reviewable).
- Containers deployed behind a reverse proxy on whatever host the human already runs.
- Self-hostable over SaaS where reasonable.

## Smells
- A choice justified by popularity alone.
- Two tools for one job (ESLint + Prettier + Biome; Tailwind + CSS-in-JS + tokens).
- A framework whose schema language can't express the SPEC's constraints, which pushes the most
  important line in the system out of sight.
- In-process timers for scheduled work the SPEC depends on (they die with the process).
- A dependency for something the platform already does.
