#!/usr/bin/env bash
# Start the trading agent.
#
#   bash start.sh              -> DRY RUN, one cycle (safe: no real orders)
#   bash start.sh loop         -> DRY RUN, one cycle per day, keeps running
#   bash start.sh live         -> LIVE, one cycle (REAL ORDERS within your limits)
#   bash start.sh live loop    -> LIVE, one cycle per day, keeps running
#
# Uses config.json. Press Ctrl-C to stop a loop.

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

# Same bin/ vs Scripts/ detection as setup.sh (Mac/Linux vs Windows venv layout).
if [ -f .venv/bin/python ]; then
  VENV_PY=.venv/bin/python
elif [ -f .venv/Scripts/python.exe ]; then
  VENV_PY=.venv/Scripts/python.exe
else
  echo "The virtual environment looks broken - run:  bash setup.sh   again."
  exit 1
fi

ARGS=(--config config.json)
MODE="DRY RUN (no real orders)"
for a in "$@"; do
  case "$a" in
    live) ARGS+=(--live); MODE="LIVE - real orders within your configured limits" ;;
    loop) ARGS+=(--interval 86400) ;;
    *) echo "Unknown option: $a  (valid: live, loop)"; exit 1 ;;
  esac
done

echo "Mode: $MODE"
if [[ "$MODE" == LIVE* ]]; then
  read -r -p "Type YES to confirm live trading: " ok
  [ "$ok" = "YES" ] || { echo "Cancelled."; exit 1; }
fi

exec "$VENV_PY" run.py "${ARGS[@]}"
