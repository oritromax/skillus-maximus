#!/usr/bin/env bash
# Read-only audit battery for a third-party agent skill / CLI repo.
# Usage: audit-skill-repo.sh <repo-dir> [generated-html-or-output-dir]
# Prints one section per question; changes nothing.
set -uo pipefail
REPO=${1:?usage: audit-skill-repo.sh <repo-dir> [generated-output]}
OUT=${2:-}
cd "$REPO" || exit 1
export LC_ALL=C

hr() { printf '\n=== %s ===\n' "$1"; }

hr "tree"
git log -1 --format='sha=%h  subject=%s' 2>/dev/null
printf 'files=%s\n' "$(git ls-files | wc -l)"

hr "install hooks / package metadata"
if [ -f package.json ]; then
  node -e 'const p=require("./package.json");console.log("private="+!!p.private);console.log("scripts="+JSON.stringify(p.scripts||{}));console.log("deps="+JSON.stringify(Object.keys(p.dependencies||{}))+" devDeps="+JSON.stringify(Object.keys(p.devDependencies||{})));' 2>/dev/null \
    || grep -nE '"(pre|post)?install"|"dependencies"|"private"' package.json
fi
find . -maxdepth 2 -name 'setup.py' -o -maxdepth 2 -name 'hooks' -o -maxdepth 2 -name 'install.sh' -o -maxdepth 2 -name 'Makefile' | grep -v node_modules | head

hr "process spawning (non-runtime)"
grep -rnE "spawn(Sync)?\(|execFile\(|exec\(" --include=*.mjs --include=*.js --include=*.ts --include=*.py . 2>/dev/null \
  | grep -v node_modules | grep -vE 'vendor|locales' | head -40

hr "network + exec primitives in source"
grep -rnE "\bfetch\(|XMLHttpRequest|sendBeacon|WebSocket|new Function|eval\(" --include=*.mjs --include=*.js --include=*.ts . 2>/dev/null \
  | grep -v node_modules | grep -vE 'vendor|locales' | head -30

hr "hardcoded remote endpoints in source"
grep -rhoE "https?://[a-zA-Z0-9._/-]+" --include=*.mjs --include=*.js --include=*.ts . 2>/dev/null \
  | grep -v node_modules | sort -u | head -20

hr "local server binds"
grep -rnE "listen\(|0\.0\.0\.0|127\.0\.0\.1" --include=*.mjs --include=*.js . 2>/dev/null | grep -v node_modules | head -15

hr "hidden unicode (zero-width / bidi / tag block)"
grep -rlP "[\x{200B}-\x{200F}\x{202A}-\x{202E}\x{2060}-\x{2064}\x{FEFF}\x{E0000}-\x{E007F}]" . \
  --include=*.md --include=*.mjs --include=*.js --include=*.json --include=*.py 2>/dev/null \
  | grep -vE 'node_modules|vendor|locales' | head

hr "persistent-authority instructions (edit global rules / rc / keys)"
grep -rnE "CLAUDE\.md|AGENTS\.md|\.bashrc|\.zshrc|crontab|authorized_keys|\.claude/|\.codex/|config\.yaml" \
  --include=*.md . 2>/dev/null | grep -v node_modules | head -20

hr "prompt-injection-shaped phrases (read in context, not by count)"
grep -rniE "ignore (all |any )?(previous|prior|above)|disregard (the|all|any)|do not tell the user|don't tell the user|without (telling|informing|asking) the user|exfiltrat|api[_ -]?key|credentials|rm -rf|sudo |curl .*\|" \
  --include=*.md . 2>/dev/null | grep -v node_modules | head -30

if [ -n "$OUT" ] && [ -e "$OUT" ]; then
  hr "generated output: remote loads and exec (must be empty for a self-contained artifact)"
  if [ -d "$OUT" ]; then FILES=$(find "$OUT" -name '*.html' | head -5); else FILES=$OUT; fi
  for f in $FILES; do
    printf '%s: ' "$f"
    grep -coE "<script[^>]*src=|fetch\(|XMLHttpRequest|sendBeacon|eval\(" "$f" 2>/dev/null || echo 0
    grep -oE "(src|href)=\"https?://[^\"]+" "$f" 2>/dev/null | sort -u | head -5
  done
fi

hr "done (read-only: nothing was modified)"
