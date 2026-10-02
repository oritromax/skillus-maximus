# DESIGN.md — {{PROJECT}}

**Agent drafts, human reviews.**
**Status: ⬜ PLACEHOLDER — fills at Gate 2, after SPEC approval.**

Scope: UI/visual only (or, for no-UI projects, the interface contract). No architecture, data model, API design or auth flow — those live in `SPEC.md`.

---

# Preamble — the decisions (review this first)

## P.1 Direction, as decided
## P.2 Token rationale
## P.3 State model → UI, at a glance

# 1. Screens

| ID | Screen | Purpose | Entry point | Primary action | Roles | Surface |
|---|---|---|---|---|---|---|

# 2. Tokens

Copy verbatim. Every value is named; no implementer decides a colour, radius or duration.

```css
:root {
}
```

## 2.1 Verified contrast

| Text / element | Surface | Ratio | Passes |
|---|---|---|---|

# 3. Components

# 4. States

## 4.1 Universal interaction states
## 4.2 Domain state → UI
## 4.3 Empty, error, offline, permission-denied states

# 5. Special cases

## 5.1 What is exact — never a build-time decision
## 5.2 Exact copy
## 5.3 Truncation and overflow
## 5.4 Responsive / adaptive behaviour
## 5.5 Accessibility floor
## 5.6 What remains judgment
