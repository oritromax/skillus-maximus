#!/usr/bin/env python3
"""Scaffold a spec-driven project: the eight docs, a platform .gitignore, git on a feature branch.

Usage:
  scaffold.py <project-dir> "<Project Name>" <platform> [--requirement-file FILE] [--no-git]

platform: web | desktop | mobile | api | cli | hybrid   (hybrid: comma list allowed, e.g. hybrid:web,mobile)

Never overwrites an existing doc (prints SKIP). Never commits. Exits non-zero on bad input.
"""
import argparse
import datetime as dt
import pathlib
import subprocess
import sys

SKILL = pathlib.Path(__file__).resolve().parent.parent
TEMPLATES = SKILL / "templates"
DOCS = ["AGENTS.md", "RULES.md", "SPEC.md", "DESIGN.md", "TESTING.md", "SECURITY.md", "PLAN.md", "DEPLOY.md"]

GITIGNORE_BASE = """# secrets — never committed (RULES.md)
.env
.env.*
!.env.example
*.pem
*.key
*.p12
*.pfx
*.keystore
*.jks
*.mobileprovision
*.p8
secrets/

# OS / editor
.DS_Store
Thumbs.db
.idea/
.vscode/
*.swp

# logs / coverage
*.log
coverage/
.nyc_output/
"""

GITIGNORE_PLATFORM = {
    "web": "\n# web\nnode_modules/\ndist/\nbuild/\n.next/\n.svelte-kit/\n.astro/\n.turbo/\n.vercel/\nplaywright-report/\ntest-results/\n",
    "desktop": "\n# desktop\nnode_modules/\ndist/\nbuild/\nout/\nrelease/\ntarget/\nsrc-tauri/target/\n*.dmg\n*.msi\n*.exe\n*.AppImage\n*.deb\n",
    "mobile": "\n# mobile\nnode_modules/\n.expo/\nios/Pods/\nios/build/\nandroid/.gradle/\nandroid/app/build/\nbuild/\n*.ipa\n*.apk\n*.aab\nDerivedData/\n.dart_tool/\ngoogle-services.json\nGoogleService-Info.plist\n",
    "api": "\n# api\nnode_modules/\ndist/\nbuild/\n__pycache__/\n.venv/\nbin/\n",
    "cli": "\n# cli\nnode_modules/\ndist/\nbuild/\n__pycache__/\n.venv/\nbin/\ntarget/\n",
}


def run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project_dir")
    ap.add_argument("name")
    ap.add_argument("platform")
    ap.add_argument("--requirement-file")
    ap.add_argument("--no-git", action="store_true")
    a = ap.parse_args()

    plat = a.platform.lower()
    if plat.startswith("hybrid"):
        surfaces = plat.split(":", 1)[1].split(",") if ":" in plat else []
        kinds = [s for s in surfaces if s in GITIGNORE_PLATFORM] or ["web", "mobile"]
        plat_label = "hybrid (" + ", ".join(surfaces or ["surfaces TBD"]) + ")"
    elif plat in GITIGNORE_PLATFORM:
        kinds = [plat]
        plat_label = plat
    else:
        sys.exit(f"bad platform '{a.platform}': use web|desktop|mobile|api|cli|hybrid[:a,b]")

    root = pathlib.Path(a.project_dir).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)

    req = "[REQUIREMENT — paste verbatim, numbered R1…Rn]"
    if a.requirement_file:
        lines = [l.rstrip() for l in pathlib.Path(a.requirement_file).expanduser().read_text().splitlines() if l.strip()]
        req = "\n".join(f"- **R{i}** {l}" for i, l in enumerate(lines, 1))

    subs = {"{{PROJECT}}": a.name, "{{PLATFORM}}": plat_label,
            "{{DATE}}": dt.date.today().isoformat(), "{{REQUIREMENT}}": req}

    created, skipped = [], []
    for d in DOCS:
        dest = root / d
        if dest.exists():
            skipped.append(d)
            continue
        text = (TEMPLATES / d).read_text()
        for k, v in subs.items():
            text = text.replace(k, v)
        dest.write_text(text)
        created.append(d)

    gi = root / ".gitignore"
    if gi.exists():
        skipped.append(".gitignore")
    else:
        gi.write_text(GITIGNORE_BASE + "".join(GITIGNORE_PLATFORM[k] for k in dict.fromkeys(kinds)))
        created.append(".gitignore")

    env_ex = root / ".env.example"
    if not env_ex.exists():
        env_ex.write_text("# Names only — never values. Filled as tasks introduce configuration.\n")
        created.append(".env.example")

    print(f"project: {root}")
    print(f"platform: {plat_label}")
    for c in created:
        print(f"  CREATE {c}")
    for s in skipped:
        print(f"  SKIP   {s} (exists — not overwritten)")

    if not a.no_git:
        if not (root / ".git").exists():
            r = run(["git", "init", "-b", "main"], root)
            print("  git init -b main:", "ok" if r.returncode == 0 else r.stderr.strip())
        cur = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], root).stdout.strip()
        if cur in ("main", "master", "HEAD"):
            r = run(["git", "checkout", "-b", "feature/spec-docs"], root)
            print("  branch feature/spec-docs:", "ok" if r.returncode == 0 else r.stderr.strip())
        else:
            print(f"  on branch {cur} — left as is")
        name = run(["git", "config", "user.name"], root).stdout.strip()
        email = run(["git", "config", "user.email"], root).stdout.strip()
        if not name or not email:
            print("  WARN git user.name/user.email not set — set them before any commit (commits are authored as the local git user only)")
        else:
            print(f"  git author: {name} <{email}>")
    print("nothing committed. next: fill AGENTS.md (a)(b)(f), write SPEC Appendix A.1/A.3, then run the SPEC process.")


if __name__ == "__main__":
    main()
