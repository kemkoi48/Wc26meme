#!/usr/bin/env bash
# Run the daily symbol screener (read-only research; picks today's
# symbol_allowlist via hard numeric filters, see screener.py). Run this once
# each morning BEFORE start.sh / your trading schedule -- see
# deploy/crontab.example for a ready-made cron line.
#
#   bash screen.sh

set -euo pipefail
cd "$(dirname "$0")"

if [ ! -d .venv ]; then
  echo "Not set up yet - run:  bash setup.sh"
  exit 1
fi
if [ ! -f .env ]; then
  echo "Missing .env - run:  bash setup.sh   then edit .env (QUICKSTART.md step 3)."
  exit 1
fi

# Same bin/ vs Scripts/ detection as start.sh (Mac/Linux vs Windows venv layout).
if [ -f .venv/bin/python ]; then
  VENV_PY=.venv/bin/python
elif [ -f .venv/Scripts/python.exe ]; then
  VENV_PY=.venv/Scripts/python.exe
else
  echo "The virtual environment looks broken - run:  bash setup.sh   again."
  exit 1
fi

exec "$VENV_PY" screener.py --config "${1:-config.json}"
