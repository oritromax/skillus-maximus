# Platform: Web app

Load this when C1 = web, or for the web surface of a hybrid. Each section lists what this platform
**adds** to the phase reference. It doesn't repeat the phase reference.

Tool names are current as of this skill's writing. **Verify current versions at Gate 1.5** (registry or
release page). Never pin a version from memory.

## Intake questions (platform round)

| # | Question | Choices (recommended first, from facts) |
|---|---|---|
| W1 | How is it rendered? | Server-rendered app with interactive islands (SSR) · Single-page app + separate API · Static site + light API · Not sure, choose from the spec |
| W2 | Which devices must it work well on? | Desktop and mobile browsers (responsive) · Desktop browsers mainly · Mobile browsers mainly · Installable on phones too (PWA) |
| W3 | Does it need to work offline or be installable? | No, online only · Installable, online only · Yes, offline reading · Yes, offline editing with sync |
| W4 | Does anything update live without a refresh? | No, refresh is fine · Yes, a few live views (status, notifications) · Yes, real-time collaboration |
| W5 | Where will it run? | A VPS or self-hosted server with Docker · Managed platform (Vercel/Fly/Render/Cloudflare) · Company infra (fixed) · Decide at DEPLOY |
| W6 | Does it send email or other notifications? | Transactional email only · Email + in-app · Email + push/SMS · None |
| W7 | Is SEO or public, shareable pages important? | No, everything is behind login · Some public pages (landing, shared links) · Yes, public content is the product |

Browser support defaults to the last 2 versions of evergreen browsers. Ask only if the audience
suggests otherwise (enterprise lock-down, old Android).

## SPEC additions
- §9 becomes the HTTP API: method, path, auth requirement, request/response shape, error codes. Add a
  **route → access rule table**; TESTING proves it exhaustively.
- §10 session mechanics: cookie vs token, cookie flags, expiry, rotation, CSRF stance.
- §11: performance budgets that can be tested (TTFB, LCP on a named page, API p95 on named endpoints),
  supported browsers, a11y level.
- §12 web edge cases: double submit, back button after a mutation, two tabs open, session expiry
  mid-form, deep links to deleted things, very long strings in layouts.
- If W3 = offline editing: a sync section is mandatory (conflict policy, what is authoritative, queue
  limits). Treat it as a hybrid with a local-first core; see `platform-other.md`.

## Stack options (choose at Gate 1.5; every choice cites a SPEC line)

| Need | Options | Forced by |
|---|---|---|
| Full-stack TS, SSR | Next.js · SvelteKit · Remix/React Router · Astro (content-heavy) | W1, W7 |
| SPA + API | React/Vue/Svelte + Vite, API in Fastify/Hono/Go/FastAPI | W1, a separate API consumer (§9) |
| DB | PostgreSQL by default · SQLite (single node, low write concurrency) · MySQL if fixed | §7 invariants: Postgres exclusion constraints, range types, row locks |
| ORM / migrations | Drizzle · Prisma · Kysely · sqlc (Go) · Alembic (Py) | Migrations must be able to express §7's constraints in raw SQL |
| Auth | Built-in sessions + argon2id · Better Auth/Lucia-style libs · OAuth provider | §10 |
| Email (dev) | Mailpit / MailHog captured locally; provider over SMTP in prod | §8 notifications, testable capture |
| Jobs / schedule | cron + CLI entrypoint · a queue (BullMQ, pg-boss, River) | §8 background work; in-process timers die with the process |
| Realtime | SSE · WebSockets · a hosted realtime service | W4 |
| Styling | Plain CSS with DESIGN tokens · Tailwind with tokens mapped to theme | DESIGN tokens must stay the single source |

## DESIGN additions
- Breakpoints with real values, and the layout at each one for every screen that changes.
- Keyboard: every action is reachable; focus order and visible focus ring; dialogs trap focus and Esc
  closes them.
- Loading strategy per screen: skeleton, spinner or optimistic update, written down.
- URL design: which states are linkable (filters, selected item, date).
- Tokens as CSS custom properties in a fenced block, copied verbatim into `tokens.css`.

## TESTING tooling
| Level | Default tools |
|---|---|
| Unit | Vitest / Jest · Go test · pytest |
| Integration | API against **real DB** in docker compose; email captured by Mailpit/MailHog via its HTTP API |
| E2E | Playwright: only the journeys where the browser is what's being proven |
| A11y | axe-core inside Playwright on every E2E screen; zero serious/critical violations |
| Visual (optional) | Playwright screenshots on the key screens, at each breakpoint |
| Perf (if §11 budgets exist) | Lighthouse CI on named pages; k6/autocannon on named endpoints |

Web-specific must-tests: an exhaustive route-authorization table test (every route × every role);
CSRF on every mutating route if cookie sessions are used; session expiry and revocation.

## SECURITY surface (web additions)
- OWASP Top 10 mapped onto *this* system's entry points. No generic dump: each item cites a route or
  flow.
- Cookies: `HttpOnly`, `Secure`, `SameSite`; session rotation on login and privilege change.
- CSRF protection for cookie auth; CORS allow-list (never `*` with credentials).
- Security headers: CSP (no `unsafe-inline` scripts if achievable), HSTS, `X-Content-Type-Options`,
  `Referrer-Policy`, frame-ancestors.
- Output encoding (XSS) in every place user content renders, including emails.
- Rate limits on auth, reset and any expensive endpoint; account enumeration via identical responses.
- File uploads, if any: type sniffing, size cap, storage outside webroot, no execution, signed URLs.
- SSRF if the server fetches user-supplied URLs.

## PLAN Phase 0 (web)
1. Toolchain: package manager, language, lint/format, typecheck, test runner. Every AGENTS (d)
   command is run once.
2. Local services via docker compose (DB, mail capture, cache if needed); `.env.example` with names
   only.
3. Schema + first migration, **plus the invariant constraint and its guard test** if §7 has one.
4. A health endpoint + the app shell rendering one page in a browser (Playwright smoke).
5. CI running lint + typecheck + tests on every PR (if the human wants CI; ask at Gate 4).

## DEPLOY specifics
- Environments: local → staging → prod. Each has its own env vars and DB.
- Build artefact (container image or platform build), migration step **before** the new code serves,
  smoke checks after the deploy, rollback (previous image + down-migration policy, or
  forward-fix-only, decided explicitly).
- TLS, domain, reverse proxy; backups with a tested restore; scheduled jobs (cron on host or platform
  scheduler).
- Self-hosted default: Docker compose on a VPS behind an existing reverse proxy. Confirm the exact
  target host at Gate 7.
