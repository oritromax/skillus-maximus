# Platform: API / service / CLI / library, and hybrids

## API or backend service (no UI of its own)

**Intake:** who consumes it (our clients only / third parties / public)? Sync request-response or
event-driven (queues, webhooks)? Auth for machines (API keys, OAuth client credentials, mTLS)? Rate
limits per consumer? Versioning policy and deprecation window? An SLA?

**SPEC:** §9 is the product. Write it as an OpenAPI (or AsyncAPI for events) sketch inside SPEC, or as
`openapi.yaml` referenced from SPEC and gated with it. Error model (one shape, stable codes),
idempotency keys on unsafe retries, pagination, webhooks (signing, retries, ordering, replay).

**DESIGN.md = API ergonomics contract:** naming conventions, resource shapes, error catalogue,
pagination style, examples per endpoint, SDK/CLI surface if any. There are no visual tokens. The point
is the same: nothing left to judgment at build time.

**TESTING:** contract tests against the spec (schemathesis / dredd-style or generated); integration
against real dependencies; load tests if §11 has numbers; consumer-driven contracts if there are
known consumers.

**SECURITY:** OWASP API Top 10 against this API's routes (BOLA/IDOR first: every object access is
checked for ownership); key rotation; per-key scopes; request size limits; webhook signature
verification; SSRF on any URL input.

**Phase 0:** health endpoint, the OpenAPI doc served/validated, auth middleware with one protected
route + its test, real DB in compose.

**DEPLOY:** as web. Add the API versioning/deprecation runbook.

## CLI tool

**Intake:** who runs it (one person / devs / ops / CI)? Which OSes? Install method (brew, go install, npm -g,
pipx, single binary download)? Does it hold credentials? Is the output read by humans, scripts, or
both?

**SPEC:** the command tree (commands, subcommands, flags, args, defaults), exit codes, config file
location and precedence (flag > env > config > default), stdin/stdout/stderr contract, `--json`
output schema if scripts consume it, idempotency of destructive commands, a `--dry-run` policy.

**DESIGN.md = CLI UX contract:** help text format, error message style (what went wrong + what to do),
colour/TTY detection (`NO_COLOR`), progress output, prompts versus non-interactive mode (`--yes`,
CI detection), output tables/JSON examples for every command.

**TESTING:** golden-file tests of output (help, errors, `--json`); exit-code tests; a real filesystem
in a temp dir; cross-OS CI if multi-OS; path handling (spaces, unicode, Windows separators).

**SECURITY:** credential storage (OS keychain, not plaintext); never echo secrets; shell injection if it
shells out; safe temp files; update/self-update integrity; supply chain (signed release artefacts,
checksums).

**Phase 0:** skeleton command tree + `--help`/`--version` golden tests, the release pipeline producing
an installable artefact for each target.

## Library / SDK

**SPEC:** public API surface (every exported symbol is a contract), semver policy, supported runtime
versions, error/exception model, threading/async model, zero/minimal dependency stance.
**DESIGN.md:** API ergonomics plus docs structure. **TESTING:** unit + property-based tests, examples
in docs executed as tests, a compatibility matrix. **SECURITY:** dependency surface, safe defaults,
input validation at the boundary. **DEPLOY:** registry publish, provenance/signing, changelog.

## Hybrids (several surfaces)

Most real products are hybrids: web app + mobile app over one API, desktop app + sync server, mobile
app + admin web panel.

**Rules:**
1. **One SPEC, one decision register, one AC list.** ACs are tagged with the surface(s) they apply to:
   `AC12 [web, mobile]`. Behaviour is decided once.
2. **The API is the shared contract.** It is specified in SPEC §9 once, versioned from day one, and
   every surface consumes the same API. No surface-specific backdoors.
3. **DESIGN.md has a shared token layer plus a section per surface** (web screens, mobile screens),
   with the same domain-state → UI mapping on every surface. A state that looks different on mobile
   is a decision, not drift.
4. **TESTING has one AC map with a level per surface,** plus a cross-surface E2E for the journeys that
   span them (create on web → push on mobile → act on mobile → visible on web).
5. **SECURITY has one threat surface listing every client.** Mobile and desktop clients are untrusted
   by definition; all rules are server-enforced.
6. **PLAN orders server first, then the primary surface, then the secondary surface.** Each surface
   gets its own Phase 0 (signed pipeline for mobile/desktop) early. Don't leave the mobile signing
   pipeline to the last phase.
7. **DEPLOY has a section per surface plus the ordering rule:** backend deploys first and stays
   backward compatible with every live client version.

Intake for hybrids: ask C1 follow-up "which surface is primary?" and "does every surface do
everything, or is there a split (e.g. admin on web only)?". Then run each surface's platform round,
skipping questions already answered.

## Local-first apps (desktop or mobile with sync)

Treat sync as its own subsystem with its own SPEC section: the source of truth per entity, the conflict
policy per entity, the identity model, the offline queue, the schema-migration story when clients on
different versions sync, and the "two devices edit the same thing offline" ACs. This is the invariant
for these apps; it gets the strictest proof (a deterministic multi-client sync test harness).
