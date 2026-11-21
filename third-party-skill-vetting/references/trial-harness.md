# Trial harness — judging design and content skills on a real repo

Scope: running a group of third-party skills against a project so the reviewer can see the result in a browser,
with nothing installed and nothing pushed. Adopting one afterwards goes back to SKILL.md section 4 (pinned copy).
Two targets: a real repo (below), or an app built for the trial when the skill's subject is behavior rather
than appearance (*Capability trials*).

## Setup

```bash
mkdir -p <trial-dir> && cd <trial-dir>
git clone -q <repo> site && cd site
git remote set-url --push origin DISABLED     # fetch still works; no push can happen
npm ci --no-audit --no-fund
git branch trial/00-baseline && git checkout -q trial/00-baseline
(setsid nohup <dev-server-cmd> --host 0.0.0.0 --port <port> > ../dev.log 2>&1 &)   # e.g. npx astro dev
sleep 6 && curl -s -o /dev/null -w '%{http_code}\n' http://<lan-ip>:4321/
```

- Hand over the **LAN IP**, never `localhost`: the reviewer's browser is usually not on the host running the server.
- `setsid nohup … &` keeps the dev server alive past the tool call; a plain `&` dies with the shell.
- Pin the clone's push URL to `DISABLED` rather than removing `origin`: `git fetch`/`log origin/master` keep
  working for branch-cut comparisons, and the guarantee is absolute rather than a line in a brief.

## Fetching the skill files, not the skills

List the catalog's tree once (`catalog.json` or the repo tree API), then pull only the chosen skills' blobs,
reference files included, into `<scratch>/<trial>/skills/<skill>/`:

```bash
curl -sL https://raw.githubusercontent.com/<org>/<repo>/main/skills/<skill>/SKILL.md -o skills/<skill>/SKILL.md
grep -rEl 'curl |wget |npx |npm i|pip install|eval\(|base64' skills | head
```

The grep is the cheap pre-flight: a design or writing skill that shells out is doing something other than what
its description says. Anything that survives gets read properly (SKILL.md plus the references it points at)
before it is handed to a child agent.

## The brief

A constraints block **first**, then the task. What matters is what must NOT change:

| Constraint | Why it is in the brief |
|---|---|
| Palette hexes and font pairing, quoted | Without it a "colors" skill re-themes a site whose palette is an official decision |
| Copy, prices, the data file, the page outline | A layout or writing skill will otherwise rewrite the product |
| "Edit only under `<src>`" | Keeps the diff reviewable and the build output out of it |
| No installs, no push, no remote changes | The brief is the only thing standing between a skill and the network |
| Run the build; report per skill | Gives you a checkable claim per skill instead of one summary |

Require the report per skill: **what changed, why, which rule of the skill drove it, what it deliberately did
not change.** The not-changed list is the most useful part — it is where the skill's own judgement shows.

- **Give one group per run.** Three skills on the same surface compound into a diff nobody can attribute.
  A single run may still cover a cluster (typography + layout + color) as long as the report stays per skill.
- **Skills that contradict each other never share a run.** Anything whose premise is "choose a new direction"
  (theme generators, style philosophies) gets a written brief and no code while the fixed-design skills run.
- **Name the surfaces that should be refused before the run starts.** For a restraint-oriented skill the refusals
  are half the result: list the high-frequency, keyboard-initiated and non-visual surfaces in the brief as
  expected rejections, and require the quote of the rule that rejects them. Without that line, "the skill has
  taste" and "the skill changed nothing" produce the same report.

## Copy and writing groups

A copy group needs a **voice constraint**, not only a fact constraint. Writing and microcopy skills ship a default
tone — casual-polite, exclamation marks, "Please try again", "Saved!" — that is wrong for a plain
engineer-to-engineer surface. Put the voice in the brief (plain, no exclamation marks, no "please", no hype) and
require the run to name the skill whose tone it overrode and why. Without that line the writing skill is silently
dead weight: the run keeps the house voice, reports edits, and nothing distinguishes a skill that worked from one
that was ignored. Expect the same shape from UX-audit/UX-flow style skills, which assume a mobile design system
(bottom nav, toasts, skeletons) — on a marketing site only the transferable half survives: entry and exit paths,
recovery from errors, error prevention. Credit the fixes to the findings, not to the skill.

- **Check facts and bans on the diff's ADDED lines, never on the file.** File-level grep reports the pre-existing
  hits and hides the new one, and a copy pass rewrites a shared error string inside a component or a worker.
  `git diff -- src | grep '^+' | grep -nE '[0-9]|[৳$€]'` for numeric drift,
  `git diff | grep '^+' | grep -niE '<banned-term>|...|!'` for vocabulary and tone.
- **Count a product-banned word on the RENDERED page, base branch against trial branch.** Build both and compare
  `sed 's/<[^>]*>/ /g' dist/<route>/index.html | grep -oiE '\b<term>s?\b' | wc -l`. An unchanged count is the
  proof that a wording change did not smuggle the term in — stripping the old occurrence is exactly how a copy
  pass can reintroduce one elsewhere.

## Capability trials: build the baseline, do not clone one

A behavior skill — motion, gesture feel, interaction polish — is judged on what it decides, and no existing repo is
sitting in the failure state. Trialing it on a surface that already animates gives it nothing to convert. Build
the target for the trial and make the baseline the control.

- **Build the baseline with the craft deliberately absent, then verify the absence mechanically.** Brief it as
  "no `transition`, `animation`, `@keyframes`, `.animate(`, `scroll-behavior`, no motion or drag library", and
  grep `src/` yourself afterwards — a baseline that smuggles one transition in makes every later comparison
  meaningless. Cap the dependencies at the framework (`react`, `react-dom`) so the trial's library choice is
  visible evidence rather than an inherited one.
- **Cover every surface the skill has an opinion about, and let them conflict.** A board carries drag in
  progress, the gap closing behind a moved card, a detail modal, stacked undo toasts, an undo re-entry, a
  collapsible column, a popover, live search filtering, keyboard moves, hover and first load. Each is a separate
  decision, and a couple of them must land on the wrong side of the skill's own gate.
- **Publish the baseline before the trial run starts.** serve the static build from its own folder and
  hand over the plain URL; the reviewer should form an impression of
  the "before" while the "after" is still building. Publish the trial build **beside** it, never over it —
  two URLs to flip between is the deliverable.
- Branch the baseline `trial/00-baseline` in an empty-history repo and run the pass on `trial/01-…`, so the diff
  is the skill's work and nothing else.

Two rules decide whether the result is attributable to the skill at all:

- **Copy the whole sibling cluster, at the repo's own `skills/<name>/` layout.** A behavior skill delegates — the
  motion skill hands off to `../gestures/SKILL.md`, `../choreograph/SKILL.md`, `../pick-ui-library/SKILL.md`, and
  ships its recipes as `RECIPES.md` inside its own directory. Fetch one SKILL.md and the child hits a dangling
  relative path and improvises: you have tested model instinct and reported it as the skill. Record the repo sha
  once in `skills/.pinned-upstream`.
- **Never let the subject skill read the grading skill.** The review is a separate run, against the diff and the
  branch, not the report. Say so in the brief; a skill that has read its own grader grades itself.

The report is a **table, one row per surface**: frequency tier · purpose word · animate / rejected / unchanged ·
tool · properties · curve or spring · `file:line`. A prose summary cannot be checked against the diff; a row can,
and a rejection row with no quoted rule is the finding.

Run it with `claude -p < brief` and deny what a trial must never do: `Bash(git push*)`, `Bash(git remote*)`,
`Bash(ssh *)`, `Bash(sudo *)`, global installs, and `Bash(claude *)` plus `Bash(*/claude *)` — a skill whose text
says "spawn a subagent" would otherwise recurse into the CLI you are driving it with. `--add-dir` the vendored
`skills/` dir and the `runs/` dir so the child can read its skill and write its report while the app directory
stays the only writable tree.

Fake-completion check, before you publish the trial: the tree is uncommitted or committed by the child, `tsc` and
`build` are re-run by you, and the motion grep is repeated on the new branch. The claim "it added motion" is only
worth the grep that shows the properties it added.

- **A restraint-oriented skill's own "never ship" table is your linter.** Turn each prohibition into a grep over
  the diff's ADDED lines (`transition: all`, `scale(0)`, `ease-in`, `@keyframes`, animated
  `width|height|margin|top|left`) — a skill with an explicit rule table is mechanically checkable, so check it
  instead of trusting the report's claim of obedience. Run the same greps on the base branch: a hit on the
  baseline means the control was contaminated and every comparison built on it is void, while a hit only on the
  trial branch is the skill's own rule broken.
- **Browser and feel claims the child makes stay self-reports until you re-run them.** A headless CDP/Playwright
  smoke test ("keyboard moves start 0 animations", "reduced motion keeps only the fade") is checkable only if the
  script is on disk or quoted in the report; if it is not, hand it over as "its own browser check, not
  re-verified" rather than repeating it as fact. Forward its human feel-check list intact — the values a run says
  it cannot judge from code are the part a human actually has to do.

## Reviewing the group

1. `npm run build` yourself, and `git status --short` — expect an uncommitted tree (a headless run in an edit-only permission mode typically holds `git add`/`commit`/`diff` and package scripts for approval).
2. Commit as **one batch** when the skills' edits overlap in the same files; asking for per-skill commits
   produces either a fake split or three commits that do not build alone.
3. Recompute every number the report quotes. Contrast ratios and spacing sums arrive as "hand-computed, not
   machine-checked"; a ten-line script over the source hexes turns that into an auditable claim.
4. Treat the layout claims as estimates and name them for the reviewer: "the header overflows at 320px", "the sticky
   header is ~96px" are the two things a headless run cannot see and a person can in five seconds.
5. Tell the reviewer to refresh, state the branch and commit, and go back to `trial/00-baseline` before the next group.
6. **Record the reviewer's verdict in that group's report before deleting the branch.** When the reviewer rules mid-trial ("keep that
   one, cut the rest"), append the verdict to the report file — the exact change named, keep or drop, plus any
   caveat it carries — then delete the branch. Branches are throwaway by design and the report is the only record
   the final pick can read. A verdict that implies a constraint for later groups ("no new motion") goes into
   every following brief, not just the report.

## Archiving and reviewing the accumulated trial

Between the last group and the combined branch there is an archive step and an independent review. Skipping either
leaves one model grading its own homework and a set of diffs nobody has read line by line.

```bash
cd <trial-dir>/site
git format-patch -1 <group-sha> --stdout > ../patches/<group>.patch   # one per group, BEFORE the branch is deleted
git worktree add -q ../baseline trial/00-baseline                    # review root: read-only, never the live checkout
for g in g1 g2 g3; do (                       # one review per group, in parallel
  claude --model <stronger-seat> --permission-mode default --add-dir <trial-dir> --add-dir <skills-dir> \
    < ../reviews/$g.prompt > ../reviews/$g-review.md 2>../reviews/$g.err; echo "$g exit $?"
) & done; wait
```

- **Review from the baseline worktree, not the trial checkout.** The live one is on a branch that still exists and
  is serving the dev server; a reviewer with edit access there can silently become the author.
- **The brief's first paragraph is the contract**: identity (palette, fonts, fixed facts), "the current directory
  is a read-only checkout of the untouched baseline, edit nothing", per-change verdict format, and "the agent's
  report is a self-report written without seeing a diff — treat its claims as unverified".
- **One prompt per group, not one prompt over everything.** A single sweep reviews the summary of the group and
  runs out of budget before it reaches the sixth patch; six parallel seats each read their own diff in full.
- **Same group twice with two models is a legitimate comparison.** Cut both branches from the same baseline, pipe
  the identical brief, and compare on two axes: which found more real problems, and which introduced regressions.
  The stronger seat reliably finds more *and* adds unrequested churn — keep the union of its fixes, drop the churn,
  and do not let its extra edits make it "the better run" by volume.
- **Follow up the one or two findings that would change a decision.** A reviewer's biggest claim (an import that
  makes a whole font axis live, a specificity tie that decides a colour) is cheap to confirm against the actual
  package or selector, and it is the finding most likely to be half-right.

### Claim checks against the patch

A group report is useful as a map of what to look at and worthless as evidence. These five claims come back wrong
repeatedly; each is a grep or a two-line calculation:

| Report claim | How it fails | Check |
|---|---|---|
| "handles reduced motion" | The global reduce rule zeroes `animation-duration` but leaves `animation-delay` and stagger offsets, so children sit blank then pop in | Read the reduce block in the diff; every delay/offset in the added CSS needs a matching override |
| "fixed the overflow" | It moved the overflow to another width (a control row, a tag tier, a header CTA) | Recompute the row's total width at 320, 360 and 375px from the added CSS |
| "did not touch copy / left X alone" | An unrequested edit rides along, often on the page's main pitch | `git diff | grep '^-'` against the content and data files, not just the components |
| "improved contrast" | The pair moved but the *state* it is meant to signal stopped being visible (a focus border shifting to a near-identical grey) | Compute both ratios; a focus indicator needs a change a person can see, not a passing number |
| "one radius / one edge system per area" | Counting the diff shows 20 / 12 / 4 nested, or a shadow swap beside untouched hairline borders | Grep the added rules for `border-radius` and `box-shadow` and count the systems |

### Combining the carry-lists

- **Grep the union of patches for removed declarations first** (SKILL.md pitfalls): a rename in one group is invisible
  to the build of every other group.
- **A wrapper added by one group absorbs the children another group animates.** `>`-child stagger and `nth-child`
  delays break the moment a patch introduces an intermediate element; check the stagger's child count against the
  combined markup, not the original.
- **Two overrides that tie on specificity are decided by bundle order, which no review can see.** Any `:global`
  override aimed at a component's nested selector needs one extra class, not an assumed order.
- **Build the combined branch from the carry-lists, group by group, in order** — not from "keep group N" — so the
  conflicts surface where they happen and each step is still attributable to the group it came from.

## What the outcomes look like

A conservative model on `better-*`-style skills produces correctness fixes, not visible design: type sizes
lifted to a 12px floor, `minmax(0, 1fr)` tracks, opacity-faded text made solid, tokens renamed. Report that
shape honestly — "subtle, compare side by side" — instead of letting the reviewer hunt for a redesign that never came,
and offer a stronger seat for a group that should show something.
