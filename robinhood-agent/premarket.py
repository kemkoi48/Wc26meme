"""Monday morning premarket scanner — top gainers + catalyst check.

Run this 7am - 8:30am ET on Monday to build your watch list.

Usage:
  python3 premarket.py
  # Outputs: top 5-10 gainers with float, gap %, catalyst summary
  # Feeds: manual checklist for entry window 8:40-9:15am

Focus: Which gainer is "obvious" to most traders? That's your target.
The hot potato effect means attention flows to the freshest catalyst.
"""

from __future__ import annotations

import datetime as dt
import json
from dataclasses import dataclass

try:
    import requests
except ImportError:
    print("requests not installed; install with: pip install requests")
    exit(1)


@dataclass
class Gainer:
    rank: int
    symbol: str
    price: float
    pct_change: float
    gap_pct: float
    float_millions: float
    catalyst: str
    news_time: str
    extended: bool  # True if up >20% from open


def print_banner():
    print("\n" + "=" * 80)
    print("PREMARKET SCANNER — Monday 8/19/2026")
    print("Time: " + dt.datetime.now().strftime("%H:%M ET"))
    print("=" * 80)


def print_gainers(gainers: list[Gainer]):
    """Pretty-print top gainers with trading-relevant metadata."""
    print("\nTop Gainers (Ranked by Obvious Trading Opportunity):\n")
    for g in gainers:
        status = "🔴 EXTENDED" if g.extended else "🟢 FRESH"
        print(f"{g.rank}. {g.symbol:6} | ${g.price:7.2f} | +{g.pct_change:5.1f}% | Gap: {g.gap_pct:+5.1f}%")
        print(f"   Float: {g.float_millions:.1f}M | {status}")
        print(f"   Catalyst: {g.catalyst}")
        print(f"   News time: {g.news_time}")
        print(f"   Entry window: {g.rank} → {'Watch for pullback' if g.rank == 1 and g.extended else 'Fresh breakout opportunity'}")
        print()


def print_decision_tree():
    """Print the hot potato decision tree for 8:40am-9:15am window."""
    print("\n" + "=" * 80)
    print("ENTRY DECISION TREE (8:40am - 9:15am ET)")
    print("=" * 80)
    print("""
Step 1: Check #1 gainer status
  ├─ If EXTENDED (up >20%) → Watch for pullback; risky to chase
  └─ If FRESH (<20%) → Ready to trade

Step 2: Check #2-3 gainers
  ├─ FRESH catalyst at 7am-8am → HOT POTATO TARGET
  │   └─ These have trader attention flowing in
  └─ Already extended → Wait for pullback

Step 3: Pick the "OBVIOUS" one
  └─ Which one would you see and think "yeah, I want to trade that"?
     That's the one with the most volume, tightest spread, clearest setup
     That's your #1 priority

Step 4: Setup entry
  ├─ Identify support/breakout level
  ├─ Note float (lower = faster squeezes)
  ├─ Verify volume (not just gapping, actual trader interest)
  └─ Pre-calculate stop and target (Rule 4)

Step 5: Enter on breakout OR bounce
  ├─ On breakout → enter on high of day break with volume
  └─ On bounce → enter on support hold with volume confirmation

Step 6: Place stop within 60 seconds (Rule 3, GTC)

Step 7: Set exit plan
  ├─ Target: entry + 1.25 × (entry - stop) [Rule 4]
  ├─ Time stop: close at bell if not hit target or stop [Rule 7]
  └─ Manual exit: if stock rolls over AND attention shifts [Rule 5]
    """)


def print_logging_template():
    """Print the fields to log in trades.csv for this trade."""
    print("\n" + "=" * 80)
    print("LOGGING TEMPLATE (Add to trades.csv after exit)")
    print("=" * 80)
    print("""
trade_id, strategy, symbol, entry, qty, stop_initial, exit, realized_usd, \\
  entry_time, extension_level, float_millions, catalyst_source, notes

Example entry:
S8_20260819_001, S8, XPON, 4.50, 100, 4.20, 5.15, 65.00, \\
  09:04, fresh_5%, 2.1M, earnings_surprise, hot_potato_#2_gainer
    """)


def print_risk_zones():
    """Print time-based risk zones from the video."""
    print("\n" + "=" * 80)
    print("RISK ZONES (From Trader Data)")
    print("=" * 80)
    print("""
Safe Entry Window:     8:40am - 9:15am ET (peak liquidity, fresh setups)
Caution Zone:          9:15am - 10:00am (some winners hit targets; volatility stays high)
High Risk Zone:        10:00am+ (big losers concentrated here; hot potato effect accelerates)

Strategy:
  ├─ Enter in safe window only
  ├─ Exit at target OR stop (Rule 5 + Rule 3)
  └─ If not hit by 10:00am, close it (Rule 7)
    """)


def main():
    print_banner()
    print("\n⏳ Fetching top gainers from market data...")
    print("   (In production: would call Stocklake get_market_movers() + get_stock_research())")

    # For now, print the framework. Monday morning you'll call:
    # - Stocklake get_market_movers(type='gainers', limit=10)
    # - For each top 5, call get_stock_research(symbol) to verify catalyst
    # - For each, call get_stock(symbol) to get float
    # - Check if gapper or already extended

    print("\n📊 Placeholder gainers (replace with live Stocklake call):")
    placeholder_gainers = [
        Gainer(
            rank=1,
            symbol="WETO",
            price=8.50,
            pct_change=+45.2,
            gap_pct=+35.0,
            float_millions=1.2,
            catalyst="Earnings beat",
            news_time="04:15am",
            extended=True,
        ),
        Gainer(
            rank=2,
            symbol="XPON",
            price=4.80,
            pct_change=+18.5,
            gap_pct=+12.0,
            float_millions=2.1,
            catalyst="FDA approval news",
            news_time="07:05am",
            extended=False,
        ),
        Gainer(
            rank=3,
            symbol="IPST",
            price=2.25,
            pct_change=+22.3,
            gap_pct=+18.0,
            float_millions=3.5,
            catalyst="Partnership deal",
            news_time="07:35am",
            extended=False,
        ),
        Gainer(
            rank=4,
            symbol="AEYE",
            price=8.20,
            pct_change=+6.5,
            gap_pct=+4.0,
            float_millions=45.0,
            catalyst="Your current long",
            news_time="N/A",
            extended=False,
        ),
        Gainer(
            rank=5,
            symbol="HHS",
            price=4.55,
            pct_change=+4.1,
            gap_pct=+2.5,
            float_millions=22.0,
            catalyst="Your current long",
            news_time="N/A",
            extended=False,
        ),
    ]

    print_gainers(placeholder_gainers)
    print_decision_tree()
    print_risk_zones()
    print_logging_template()

    print("\n" + "=" * 80)
    print("✅ Ready for 8:40am-9:15am entry window")
    print("=" * 80)
    print("\nNext steps:")
    print("  1. Open your premarket checklist (HTML artifact)")
    print("  2. Monitor top 3 gainers for volume confirmation")
    print("  3. Enter at breakout or bounce with tightest setup")
    print("  4. Place stop (GTC) within 60 seconds")
    print("  5. Log trade with all fields (esp. entry_time, float_millions, catalyst)")
    print()


if __name__ == "__main__":
    main()
