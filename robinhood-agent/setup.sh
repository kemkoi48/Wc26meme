#!/usr/bin/env bash
# One-shot setup for robinhood-agent. Run it from this folder:
#   bash setup.sh
# Safe to re-run; it only creates what's missing.

set -euo pipefail
cd "$(dirname "$0")"

say() { printf '\n==> %s\n' "$*"; }

say "Checking Python..."
if command -v python3 >/dev/null 2>&1; then PY=python3
elif command -v python >/dev/null 2>&1; then PY=python
else
  echo "Python is not installed."
  echo "  - Mac:     install from https://www.python.org/downloads/ (big yellow button)"
  echo "  - Windows: same site; during install TICK the box 'Add python.exe to PATH'"
  echo "Then run:  bash setup.sh   again."
  exit 1
fi
"$PY" -c 'import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)' || {
  echo "Your Python is too old (need 3.10+). Install the latest from python.org and re-run."
  exit 1
}
echo "    found: $("$PY" --version)"

say "Checking Node.js (the agent needs it)..."
if ! command -v node >/dev/null 2>&1; then
  echo "Node.js is not installed. Install the LTS version from https://nodejs.org"
  echo "Then run:  bash setup.sh   again."
  exit 1
fi
echo "    found: node $(node --version)"

say "Creating an isolated Python environment (.venv)..."
[ -d .venv ] || "$PY" -m venv .venv

say "Installing the required packages..."
./.venv/bin/pip install --quiet --upgrade pip
./.venv/bin/pip install --quiet -r requirements.txt

say "Creating your .env settings file..."
if [ -f .env ]; then
  echo "    .env already exists - leaving it alone."
else
  cp .env.example .env
  echo "    created .env - YOU MUST EDIT IT (see QUICKSTART.md step 3)."
fi

say "Setup complete."
echo
echo "Next steps (QUICKSTART.md has details):"
echo "  1. Open .env in a text editor and fill in your token + account number."
echo "  2. Open config.json and put symbols in \"symbol_allowlist\"."
echo "  3. Test it (safe, no real orders):   bash start.sh"
