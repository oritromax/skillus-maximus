#!/usr/bin/env python3
"""Mechanical gate checks for a spec-driven project.

Usage: check_docs.py <project-dir> --gate N [--allow-open]

Checks accumulate by gate:
  all   eight docs present; leftover {{template}} slots; [NEEDS CLARIFICATION] / [AGENT-PROPOSED] counts
  >=1   SPEC: ACs present, unique, Given/When/Then shaped; no open [NEEDS CLARIFICATION] (unless --allow-open);
        decision register counted; AGENTS (c)/(d) no longer TBD
  >=2   DESIGN filled (not placeholder); contrast table present
  >=3   every live SPEC AC mapped in TESTING; every SECURITY control line has "verified by"
  >=4   every live SPEC AC covered by a PLAN task; task count
  >=5   unverified commands in AGENTS (d); PLAN task status counts
  >=6   unticked SECURITY boxes
Exit code 1 if any FAIL.
"""
import argparse
import pathlib
import re
import sys

DOCS = ["AGENTS.md", "RULES.md", "SPEC.md", "DESIGN.md", "TESTING.md", "SECURITY.md", "PLAN.md", "DEPLOY.md"]
results = []
NC_RE = r"\[NEEDS CLARIFICATION:"  # a marker carries its question; bare mentions in prose are not open items


def out(level, msg):
    results.append((level, msg))


def ac_ids(text):
    """All AC ids referenced in text ('12', '12b'), expanding ranges (AC31–AC37, AC5-7) and slash lists (AC5/6/7)."""
    ids = set()
    for m in re.finditer(r"\bAC(\d+)\s*[–—]\s*(?:AC)?(\d+)\b|\bAC(\d+)-(?:AC)?(\d+)\b", text):
        a, b = (int(m.group(1)), int(m.group(2))) if m.group(1) else (int(m.group(3)), int(m.group(4)))
        if a < b <= a + 200:
            ids.update(str(i) for i in range(a, b + 1))
    for m in re.finditer(r"\bAC(\d+[a-z]?)((?:\s*/\s*\d+[a-z]?)+)", text):
        ids.add(m.group(1))
        ids.update(re.findall(r"\d+[a-z]?", m.group(2)))
    ids.update(re.findall(r"\bAC(\d+[a-z]?)\b", text))
    return ids


def ac_key(x):
    m = re.match(r"(\d+)([a-z]?)", x)
    return (int(m.group(1)), m.group(2))


def spec_acs(spec):
    """AC definitions: table rows '| ACn |' or list items '- **ACn**' / 'ACn:' at line start."""
    defs, withdrawn = {}, set()
    for line in spec.splitlines():
        m = re.match(r"\s*(?:\|\s*|[-*]\s*)\**AC(\d+[a-z]?)\**\s*(?:\||:|—|-|\.)\s*(.*)", line)
        if m:
            n = m.group(1)
            body = m.group(2)
            if re.search(r"withdrawn", body, re.I):
                withdrawn.add(n)
            defs.setdefault(n, []).append(body)
    return defs, withdrawn


def section(text, heading_regex):
    m = re.search(heading_regex, text, re.M)
    if not m:
        return ""
    start = m.end()
    level = len(re.match(r"#+", m.group(0).lstrip()).group(0)) if m.group(0).lstrip().startswith("#") else 2
    nxt = re.search(r"^#{1,%d} " % level, text[start:], re.M)
    return text[start:start + nxt.start()] if nxt else text[start:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project_dir")
    ap.add_argument("--gate", type=int, required=True)
    ap.add_argument("--allow-open", action="store_true", help="accept open [NEEDS CLARIFICATION] in SPEC (human-accepted)")
    a = ap.parse_args()
    root = pathlib.Path(a.project_dir).expanduser()
    g = a.gate

    docs = {}
    for d in DOCS:
        p = root / d
        if p.exists():
            docs[d] = p.read_text(errors="replace")
        else:
            out("FAIL", f"{d} missing")
    if not docs:
        print("\n".join(f"{l:5} {m}" for l, m in results))
        sys.exit(1)

    for d, t in docs.items():
        slots = re.findall(r"\{\{[A-Z_]+\}\}", t)
        if slots:
            out("WARN", f"{d}: {len(slots)} unfilled template slot(s) {sorted(set(slots))}")
        nc = len(re.findall(NC_RE, t))
        ap_ = len(re.findall(r"\[AGENT-PROPOSED:", t))
        if nc or ap_:
            out("INFO", f"{d}: {nc} [NEEDS CLARIFICATION], {ap_} [AGENT-PROPOSED]")

    spec = docs.get("SPEC.md", "")
    defs, withdrawn = spec_acs(spec)
    live = set(defs) - withdrawn

    if g >= 1:
        if not defs:
            out("FAIL", "SPEC: no acceptance criteria found (expected rows like '| AC1 | Given … when … then … |')")
        else:
            dupes = [n for n, v in defs.items() if len(v) > 1]
            if dupes:
                out("FAIL", f"SPEC: duplicate AC numbers {sorted(dupes, key=ac_key)}")
            nums = {ac_key(n)[0] for n in defs}
            missing = sorted(set(range(1, max(nums) + 1)) - nums)
            if missing:
                out("WARN", f"SPEC: gaps in AC numbering {missing} (withdrawn ACs should stay listed as withdrawn)")
            nogwt = [n for n in sorted(live, key=ac_key) if not re.search(r"\bgiven\b.*\bwhen\b.*\bthen\b", defs[n][0], re.I)]
            if nogwt:
                out("WARN", f"SPEC: {len(nogwt)} AC(s) not in Given/When/Then shape: {nogwt[:15]}")
            out("PASS", f"SPEC: {len(live)} live ACs ({len(withdrawn)} withdrawn)")
        nc = len(re.findall(NC_RE, spec))
        if nc and not a.allow_open:
            out("FAIL", f"SPEC: {nc} open [NEEDS CLARIFICATION] — resolve, or pass --allow-open if the human accepted them at the gate")
        decisions = set(re.findall(r"^\|\s*\**D(\d+)\**\s*\|", spec, re.M))
        out("INFO" if decisions else "WARN", f"SPEC: {len(decisions)} decisions in register")
        if re.search(r"Status:\s*⬜", spec):
            out("INFO", "SPEC: status line still ⬜ (flip it on approval)")
        agents = docs.get("AGENTS.md", "")
        for sec in ("(c)", "(d)", "(e)"):
            body = section(agents, r"^## " + re.escape(sec) + r".*$")
            if "[TBD until SPEC approval]" in body:
                out("WARN" if g == 1 else "FAIL", f"AGENTS {sec}: still [TBD until SPEC approval] (fills at Gate 1.5)")

    if g >= 2:
        design = docs.get("DESIGN.md", "")
        if re.search(r"Status:\s*⬜\s*PLACEHOLDER", design):
            out("FAIL", "DESIGN: still the placeholder")
        if not re.search(r"contrast", design, re.I):
            out("WARN", "DESIGN: no contrast table found (skip if no-UI project)")

    if g >= 3:
        testing = docs.get("TESTING.md", "")
        if re.search(r"Status:\s*⬜\s*PLACEHOLDER", testing):
            out("FAIL", "TESTING: still the placeholder")
        mapped = ac_ids(testing)
        unmapped = sorted(live - mapped, key=ac_key)
        if unmapped:
            out("FAIL", f"TESTING: {len(unmapped)} SPEC AC(s) not mapped to a test: {unmapped}")
        elif live:
            out("PASS", f"TESTING: all {len(live)} live ACs mapped")
        stray = sorted(mapped - set(defs), key=ac_key)
        if stray:
            out("WARN", f"TESTING: references AC(s) not in SPEC: {stray}")

        sec = docs.get("SECURITY.md", "")
        controls = [l for l in sec.splitlines() if re.match(r"\s*[-*]\s*\[[ xX]\]", l)]
        if re.search(r"Status:\s*⬜\s*BASELINE ONLY", sec) or len(controls) <= 3:
            out("FAIL", f"SECURITY: checklist not written yet ({len(controls)} control lines) — human writes it from the proposal")
        base = section(sec, r"^## Baseline.*$")
        base_lines = {l for l in base.splitlines()}
        noverify = [l for l in controls if not re.search(r"\bverified\b", l, re.I)]
        nv_base = [l for l in noverify if l in base_lines]
        nv_main = [l.strip()[:90] for l in noverify if l not in base_lines]
        if nv_base:
            out("WARN", f"SECURITY: {len(nv_base)} baseline line(s) without a verification method (standing rules — add how each is checked before Gate 6)")
        if nv_main:
            out("FAIL", f"SECURITY: {len(nv_main)} control(s) without a verification method: " + " | ".join(nv_main[:5]))
        elif controls:
            out("PASS", f"SECURITY: {len(controls)} controls, all with 'verified by'")

    if g >= 4:
        plan = docs.get("PLAN.md", "")
        if re.search(r"Status:\s*⬜\s*PLACEHOLDER", plan):
            out("FAIL", "PLAN: still the placeholder")
        tasks = re.findall(r"^\|\s*\**T(\d+)\**\s*\|", plan, re.M)
        out("INFO" if tasks else "FAIL", f"PLAN: {len(set(tasks))} tasks")
        # coverage only from task tables (exclude the task log so history can't mask a gap)
        board = plan.split("## Task log")[0]
        covered = ac_ids(board)
        uncovered = sorted(live - covered, key=ac_key)
        if uncovered:
            out("FAIL", f"PLAN: {len(uncovered)} SPEC AC(s) not covered by any task: {uncovered}")
        elif live:
            out("PASS", f"PLAN: all {len(live)} live ACs covered by tasks")
        if not re.search(r"^## Review cadence\s*\n+\S", plan, re.M) and "cadence" not in plan.lower():
            out("WARN", "PLAN: no review cadence recorded")

    if g >= 5:
        agents = docs.get("AGENTS.md", "")
        cmd = section(agents, r"^## \(d\).*$")
        rows = [l for l in cmd.splitlines() if l.startswith("|") and "---" not in l]
        unver = [l.split("|")[1].strip() for l in rows if "⬜" in l]
        if unver:
            out("WARN", f"AGENTS (d): {len(unver)} unverified command(s): {unver}")
        plan = docs.get("PLAN.md", "")
        board = plan.split("## Task log")[0]
        trows = [l for l in board.splitlines() if re.match(r"^\|\s*\**T\d+", l)]
        done = sum(1 for l in trows if "✅" in l)
        prog = sum(1 for l in trows if "🟨" in l)
        blocked = sum(1 for l in trows if "🚫" in l)
        out("INFO", f"PLAN: {done}/{len(trows)} tasks ✅, {prog} in progress, {blocked} blocked")
        proven = ac_ids("\n".join(l for l in trows if "✅" in l)) & live
        if live:
            out("INFO", f"PROOF: {len(proven)}/{len(live)} ACs claimed by ✅ tasks ({100*len(proven)//len(live)}%) — report this, not task count")

    if g >= 6:
        sec = docs.get("SECURITY.md", "")
        unticked = [l.strip()[:80] for l in sec.splitlines() if re.match(r"\s*[-*]\s*\[ \]", l)]
        if unticked:
            out("FAIL", f"SECURITY: {len(unticked)} unticked control(s) — Gate 6 needs every applicable box ticked by the human from evidence")
        else:
            out("PASS", "SECURITY: all boxes ticked")

    order = {"FAIL": 0, "WARN": 1, "PASS": 2, "INFO": 3}
    print(f"check_docs gate {g} — {root}")
    for lvl, msg in sorted(results, key=lambda r: order[r[0]]):
        print(f"{lvl:5} {msg}")
    fails = sum(1 for l, _ in results if l == "FAIL")
    print(f"RESULT: {'FAIL' if fails else 'OK'} ({fails} fail, {sum(1 for l,_ in results if l=='WARN')} warn)")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
