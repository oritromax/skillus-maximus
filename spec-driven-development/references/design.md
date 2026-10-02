# Gate 2: DESIGN.md (the UI contract)

DESIGN.md is drafted by the agent and reviewed by the human. **Scope is UI/visual only:** screens,
tokens, components, states, special cases. No architecture, data model, API or auth flow; those live in
SPEC and are already decided. If you find yourself designing a table or an endpoint, stop and put it
back in SPEC (as a proposed SPEC change).

No-UI projects (API, CLI, library) still have a DESIGN.md: the interface contract. See
`platform-other.md`.

Two principles:
- **The UI must match intent, not AI slop.** Exact tokens beat judgment. At build time the implementer
  never decides a colour, a radius, a duration, a state or a piece of behaviour-bearing copy; it's all
  written down.
- **Start from context, not vibes.** SPEC's user stories define which screens exist and what they do.
  Derive the UI from the contract; don't invent surfaces the product doesn't need.

Inputs: the approved SPEC, the platform file's DESIGN section, and any brand or visual references (read
them first). When visual references are given, derive the palette and type from them rather than from a generic
template.

## Procedure

### 1. Screen inventory
Every screen from SPEC's stories and roles. For each: name + ID (S1…), purpose (one line), entry point,
primary action (the one thing it's for), roles that see it (from SPEC; no new roles), surface (hybrid).
Add the system screens: auth, empty, error, offline, permission-denied (mobile/desktop), update-required
(mobile/desktop).

### 2. CLARITY GAPS: before questions, before design
Everything SPEC doesn't pin down for the UI:

| # | What's unclear | Why it matters | Options I see | Blocks (screens/tokens) |
|---|---|---|---|---|

The typical questions are in the design question bank below. An empty list says "No unresolved items".

### 3. Clarification rounds
Questions come **from the gaps table**, batched by gap group, 2–4 concrete options, max two rounds.
Unresolved items stay `[NEEDS CLARIFICATION]`.

**Design question bank** (filter as usual; ask only real gaps):
- Brand direction: existing brand/logo/colours · a reference product they like · neutral and functional
  · "you propose, I'll pick from 2–3".
- Light/dark: light only · dark only · both, following the OS · both with a toggle.
- Density: comfortable (consumer) · compact (data-heavy tool) · per-screen.
- Primary device/size per role (admins at a desk, field users on phones).
- Admin UI depth: full UI · minimal forms · CLI/DB scripts only for v1.
- Icon style; illustration (none recommended for tools); motion appetite.
- Accessibility floor: WCAG 2.2 AA (recommend) · AAA for text contrast · a stated custom floor.
- Copy voice: plain/neutral · friendly · formal. Who writes the exact copy for errors and warnings?
- Platform conventions (desktop/mobile): native per OS · one custom system everywhere.

If the human says "you propose", produce **two or three named directions** (e.g. *Quiet utility*,
*Warm editorial*) with a token sketch each and ask them to pick. If they want to see them, render a
throwaway single-file HTML preview of each. Don't pick for them.

### 4. Tokens
A small, named system. Every value is a named token with a one-line rationale.
- **Colour:** neutrals, surfaces, ink/text, muted text, borders (decorative vs control). One accent
  unless SPEC says otherwise. **Status colours for every domain state in SPEC's state model**, plus
  danger/success/warning/info. One accent, not a rainbow.
- **Typography:** one family plus mono accents only; a named type scale; weights. Hierarchy comes from
  type before boxes and icons.
- **Spacing/layout:** a 4- or 8-based scale, grid tokens, breakpoints with real values (web), size
  classes (mobile), window sizes (desktop).
- **Radius, elevation, borders:** a few named values.
- **Motion:** durations and easings named; state clarification, never theatre; reduced-motion respected.
- **Light/dark:** only if decided; both sets are complete.
- **Contrast:** compute the ratio for every text/surface pair and every control border, and write it
  next to the pair. WCAG AA minimum (4.5:1 text, 3:1 large text and UI components). No unverified
  claims; compute it with a script, don't eyeball it.
- Format per platform: CSS custom properties in a fenced block (web/desktop webview), or a token table
  plus the platform theme file shape (Swift/Kotlin/Dart/RN theme object) to be copied verbatim.

### 5. Components
The recurring atoms built from §1, not from a generic kit: buttons (primary/secondary/danger/ghost),
form controls, and the domain components the screens demand (a booking grid cell, a status pill, the
check-in control). Each one has anatomy, sizes, the tokens used, and its states. Icons are minimal and
only where they aid scanning.

### 6. States
- **Universal states** for every interactive component: default, hover (pointer platforms), focus,
  active/pressed, disabled, loading, empty, error.
- **Domain state → UI:** every state in SPEC's state model maps to a visible answer: colour token,
  label, available actions, and transitions the user can see (what shows when something is about to
  expire, when it expires, when the slot reopens). No state is left to improvisation.
- **Platform states:** offline, pending sync, sync failed, permission denied, update required (per the
  platform file).

### 7. Special cases (the anti-slop section)
- **What is exact:** token values, state definitions, and **any copy that affects behaviour or trust**
  (warnings, permission prompts, destructive confirmations, error messages), written verbatim.
- **What is judgment:** spacing tweaks within the scale and minor alignment, only within the written
  system.
- Truncation and overflow rules (long names, long lists, very long text).
- Responsive/adaptive behaviour per breakpoint or size class; touch targets (44pt/48dp/44px).
- Accessibility floor: focus order, screen-reader labels for icon-only controls, font scaling.
- Anything the implementer would otherwise improvise at build time goes here.

### 8. Draft DESIGN.md
Fixed structure (`templates/DESIGN.md`): Preamble (the decisions: direction, token rationale, state
model at a glance) → 1 Screens → 2 Tokens (fenced block + verified contrast table) → 3 Components →
4 States → 5 Special cases. Hybrids: shared tokens, then a screens/components section per surface.

Additions not derivable from SPEC or the discussion are marked `[AGENT-PROPOSED: … — reason]`. You may
propose; you never silently add.

**Self-check:** would an implementer have to make any visual decision not written here? Then write it
down. Does every SPEC state have a UI answer? Does every screen have its empty and error states?

### 9. Gate
Present: screen count, token count, the contrast table result (all pass?), the state mapping, open
items, and the challenge list. Wait for approval. Next is TESTING, then SECURITY. Don't generate PLAN
yet.

## Reference point (the reference build)
533 lines; 19 screens with "the one screen that matters" called out (the day view); a full light + dark
token set as CSS custom properties with a verified contrast table for both; components; universal +
domain states; exact copy for every behaviour-bearing message; truncation, responsive and an a11y floor.
