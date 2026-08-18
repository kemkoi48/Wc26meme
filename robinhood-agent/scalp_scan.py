"""Scan minute bars for momentum-scalp entries, and manage an open one.

Reads bars from a JSON file in the shape `get_equity_historicals` returns,
so the same file can be produced by the agent during market hours or saved
by hand. No network here on purpose -- the detection logic stays a pure
function (scalp_signal.py) and this is only I/O and formatting.

    # scan every symbol in a bar dump for a fresh entry
    python3 scalp_scan.py --bars bars.json

    # ...and check an open position's exit at the same time
    python3 scalp_scan.py --bars bars.json --holding IPST:7.7174

`--holding SYMBOL:ENTRY_PRICE` replays every bar after the one whose close
equals ENTRY_PRICE, or simply the last N bars if no match, and reports the
exit decision.

READ scalp_signal.py's header before trusting any number this prints. The
short version: the entry DIRECTION is measurement-backed, the expected
RETURN is not -- most signals lose about 2%, and the profit in the sample
came from a handful of trades on one symbol on one day.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from scalp_signal import (
    DEFAULT_STOP_PCT,
    MAX_HOLD_BARS,
    MIN_BAR_RETURN_PCT,
    MIN_SURGE,
    decide_exit,
    detect_entry,
    to_bars,
)


def load_dump(path: Path) -> dict[str, list[dict]]:
    """Accepts the raw get_equity_historicals envelope, or a bare
    {symbol: [bars]} mapping."""
    data = json.loads(path.read_text())
    if isinstance(data, dict) and "data" in data:
        results = data["data"].get("results", [])
        return {r["symbol"]: r.get("bars", []) for r in results}
    if isinstance(data, dict):
        return data
    raise SystemExit("unrecognized bar file shape")


def main() -> None:
    ap = argparse.ArgumentParser(description="Momentum-scalp scanner")
    ap.add_argument("--bars", required=True, help="JSON file of minute bars")
    ap.add_argument("--holding", default=None, metavar="SYM:ENTRY",
                    help="check exit for an open position")
    ap.add_argument("--min-surge", type=float, default=MIN_SURGE)
    ap.add_argument("--min-return", type=float, default=MIN_BAR_RETURN_PCT)
    ap.add_argument("--stop-pct", type=float, default=DEFAULT_STOP_PCT)
    ap.add_argument("--show-all", action="store_true",
                    help="print non-signals too, with the reason they failed")
    args = ap.parse_args()

    dump = load_dump(Path(args.bars))

    if args.holding:
        try:
            sym, entry_s = args.holding.split(":")
            entry = float(entry_s)
        except ValueError:
            raise SystemExit("--holding needs SYMBOL:ENTRY_PRICE, e.g. IPST:7.7174")
        sym = sym.upper()
        if sym not in dump:
            raise SystemExit(f"{sym} not in {args.bars}")
        bars = to_bars(dump[sym])
        # find the bar we entered on, else assume we are near the end
        idx = next((i for i, b in enumerate(bars) if abs(b.c - entry) < 0.005), None)
        since = bars[idx + 1:] if idx is not None else bars[-MAX_HOLD_BARS:]
        d = decide_exit(entry, since, stop_pct=args.stop_pct)
        flag = "*** EXIT NOW ***" if d.exit_now else "hold"
        print(f"\n{sym}  entry ${entry:.4f}  {len(since)} bars held")
        print(f"  {flag}  ({d.kind or 'no trigger'})")
        print(f"  {d.reason}\n")
        return

    print(f"\nscanning {len(dump)} symbol(s) "
          f"[surge >= {args.min_surge}x AND bar return >= {args.min_return}%]\n")
    fired = 0
    for sym, raw in sorted(dump.items()):
        bars = to_bars(raw)
        sig = detect_entry(bars, min_surge=args.min_surge,
                           min_bar_return=args.min_return, stop_pct=args.stop_pct)
        if sig.fired:
            fired += 1
            print(f"  *** {sym} ***  {sig.reason}")
            print(f"      entry ~${sig.entry_hint:.4f}   stop ${sig.stop_price:.4f} "
                  f"({args.stop_pct:+.1f}%)   no profit target -- trail out")
            print(f"      exit when: a close below the PRIOR bar's low, "
                  f"or {MAX_HOLD_BARS} bars with no progress")
            print(f"      {sig.confidence}\n")
        elif args.show_all:
            print(f"      {sym:<8} no: {sig.reason}")

    if not fired:
        print("  no entries. That is the normal outcome -- on 2026-08-17 this")
        print("  condition fired 41 times across 5 symbols in a whole session,")
        print("  and 28 of those still lost money.\n")


if __name__ == "__main__":
    main()
