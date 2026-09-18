#!/usr/bin/env bash
# Run the read-only momentum scanner (Warrior-Trading-style stock selection;
# see sources.md and momentum_scanner.py). Writes momentum_candidates.json --
# a research report only. Nothing in this repo reads that file; it does NOT
# feed run.py or any trade.
#
#   bash scan_momentum.sh

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

exec "$VENV_PY" momentum_scanner.py --config "${1:-config.json}"
