"""Entrypoint and scheduler for robinhood-agent.

    python run.py                 # dry run, once (safe default)
    python run.py --interval 900  # dry run every 15 minutes
    python run.py --live          # LIVE, once — approved orders execute
    python run.py --live --interval 3600
"""

from __future__ import annotations

import argparse
import asyncio
import datetime as dt
import time

from dotenv import load_dotenv

from agent import run_cycle
from config import load_config


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Autonomous Robinhood trading agent.")
    p.add_argument(
        "--live",
        action="store_true",
        help="Place real orders that pass the risk limits. Without this flag, "
        "all orders are denied (dry run).",
    )
    p.add_argument(
        "--interval",
        type=int,
        default=None,
        metavar="SECONDS",
        help="Run repeatedly every SECONDS. Omit to run a single cycle.",
    )
    p.add_argument("--config", default="config.yaml", help="Path to config file.")
    return p.parse_args()


async def main() -> None:
    load_dotenv()
    args = parse_args()
    cfg = load_config(args.config)

    if args.live:
        print("!! LIVE MODE: orders passing the configured risk limits WILL execute.")
    else:
        print("Dry run: no orders will be placed. Use --live to trade for real.")

    if args.interval is None:
        await run_cycle(cfg, live=args.live)
        return

    if args.interval < 1:
        raise SystemExit("--interval must be >= 1 second")

    print(f"Looping every {args.interval}s. Ctrl-C to stop.")
    while True:
        started = time.monotonic()
        try:
            await run_cycle(cfg, live=args.live)
        except Exception as exc:  # keep the loop alive across transient failures
            print(f"[error] cycle failed at {dt.datetime.now().isoformat()}: {exc}")
        elapsed = time.monotonic() - started
        sleep_for = max(0.0, args.interval - elapsed)
        print(f"[sleep] next cycle in {sleep_for:.0f}s")
        await asyncio.sleep(sleep_for)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped.")
