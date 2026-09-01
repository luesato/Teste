#!/usr/bin/env bash
# One-shot setup. Creates the venv, installs deps, and reports what it found.
# Safe to re-run. Touches nothing outside this folder.
set -euo pipefail

cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found. Install it with:  brew install python" >&2
  exit 1
fi

echo "==> Creating virtual environment"
[ -d .venv ] || python3 -m venv .venv

echo "==> Installing dependencies (this takes a minute)"
./.venv/bin/pip install --quiet --upgrade pip
./.venv/bin/pip install --quiet -r requirements.txt

echo "==> Checking your Chrome setup"
echo
# Don't abort on a failed check - the report itself is the useful part.
set +e
./.venv/bin/python check_setup.py
check_status=$?
set -e

if [ "$check_status" -ne 0 ]; then
  cat <<'EOF'

------------------------------------------------------------
Setup finished, but the check above found a problem.
Send those lines to Claude and it will tell you the fix.
------------------------------------------------------------
EOF
  exit 0
fi

cat <<'EOF'

------------------------------------------------------------
Next: copy the profile folder name above and send it to Claude,
along with the apps you want captured. Nothing has been captured
yet and no browser has been opened.
------------------------------------------------------------
EOF
