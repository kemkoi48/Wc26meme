"""Stocklake Pro insider activity screener for catalyst verification.

This tool pulls insider trading data and research summaries to verify catalysts
and detect signals that often precede halts or reversals. It runs independently
of the main screener and is controlled by a manual on/off toggle.

Usage:
  # Check a single symbol for insider activity
  python3 stocklake_screener.py --symbol AEYE --enable

  # Batch check multiple symbols
  python3 stocklake_screener.py --symbols AEYE,HHS,SMWB --enable

  # Disable refresh (read from cache only, useful on quota-restricted days)
  python3 stocklake_screener.py --symbols AEYE,HHS --disable

Safety properties:
  - Read-only tool; cannot place, cancel, or exercise any order.
  - Manual on/off toggle prevents accidental quota burn (ChatGPT screener burned
    5000/5000 daily calls by refreshing every 10 minutes).
  - Results are cached to disk (stocklake_cache.json) and reused unless --enable
    is explicitly passed.
  - If API key is missing or quota exhausted, tool falls back to cached data
    gracefully.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urljoin

import requests
from dotenv import load_dotenv

load_dotenv()

CACHE_FILE = Path(__file__).parent / "stocklake_cache.json"
API_BASE = "https://api.stocklake.com"


@dataclass
class InsiderFinding:
    """One insider activity finding for a symbol."""
    symbol: str
    date: str
    action: str  # "buy" | "sell" | "exercise"
    name: str  # insider name
    title: str  # role
    amount: float  # notional USD
    trend: str  # "accumulation" | "distribution" | "neutral"
    note: str


@dataclass
class StocklakeResult:
    """Screening result for one symbol."""
    symbol: str
    success: bool
    insider_activity: list[InsiderFinding]
    research_verdict: Optional[str]  # "BULLISH" | "BEARISH" | "NEUTRAL" | None
    news_catalyst: Optional[str]
    error: Optional[str]
    cached_at: str


def _load_cache() -> dict[str, StocklakeResult]:
    """Load cached results from disk."""
    if not CACHE_FILE.exists():
        return {}
    try:
        data = json.loads(CACHE_FILE.read_text())
        return {k: StocklakeResult(**v) for k, v in data.items()}
    except Exception as e:
        print(f"Warning: cache load failed ({e}), starting fresh")
        return {}


def _save_cache(results: dict[str, StocklakeResult]) -> None:
    """Save results to disk cache."""
    try:
        data = {k: asdict(v) for k, v in results.items()}
        CACHE_FILE.write_text(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Warning: cache save failed ({e})")


def get_insider_activity(
    symbol: str,
    api_key: Optional[str] = None,
    use_cache: bool = True,
) -> StocklakeResult:
    """Fetch insider activity for one symbol from Stocklake Pro.

    Args:
        symbol: stock ticker
        api_key: Stocklake API key (reads from STOCKLAKE_API_KEY env if None)
        use_cache: if True and data is cached, return cached result without API call

    Returns:
        StocklakeResult with findings or cache hit, or error details.
    """
    symbol = symbol.upper().strip()
    cache = _load_cache()

    # Check cache first if enabled
    if use_cache and symbol in cache:
        cached = cache[symbol]
        age_hours = (
            (dt.datetime.fromisoformat(cached.cached_at) - dt.datetime.now()).total_seconds()
            / 3600
        )
        if age_hours < 24:  # Cache valid for 24 hours
            return cached

    # If we have no API key, return cached or error
    api_key = api_key or os.getenv("STOCKLAKE_API_KEY", "").strip()
    if not api_key:
        if symbol in cache:
            return cache[symbol]
        return StocklakeResult(
            symbol=symbol,
            success=False,
            insider_activity=[],
            research_verdict=None,
            news_catalyst=None,
            error="STOCKLAKE_API_KEY not set in .env",
            cached_at=dt.datetime.now().isoformat(),
        )

    try:
        # Fetch insider activity
        insider_url = urljoin(API_BASE, f"/v1/stocks/{symbol}/insider_activity")
        insider_resp = requests.get(
            insider_url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10,
        )
        insider_resp.raise_for_status()
        insider_data = insider_resp.json()

        # Fetch research (sentiment, verdict, catalyst)
        research_url = urljoin(API_BASE, f"/v1/stocks/{symbol}/research")
        research_resp = requests.get(
            research_url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10,
        )
        research_resp.raise_for_status()
        research_data = research_resp.json()

        # Parse insider activity into findings
        findings: list[InsiderFinding] = []
        for item in insider_data.get("insider_transactions", [])[:10]:  # Top 10 recent
            finding = InsiderFinding(
                symbol=symbol,
                date=item.get("date", ""),
                action=item.get("transaction_type", "").lower(),
                name=item.get("insider_name", ""),
                title=item.get("position", ""),
                amount=float(item.get("notional_amount", 0)),
                trend=item.get("insider_trend", "neutral"),
                note=item.get("note", ""),
            )
            findings.append(finding)

        result = StocklakeResult(
            symbol=symbol,
            success=True,
            insider_activity=findings,
            research_verdict=research_data.get("verdict"),
            news_catalyst=research_data.get("recent_news_headline"),
            error=None,
            cached_at=dt.datetime.now().isoformat(),
        )

        # Update cache
        cache[symbol] = result
        _save_cache(cache)

        return result

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            error_msg = "Daily quota exhausted"
        elif e.response.status_code == 404:
            error_msg = "Symbol not found (small cap not in Stocklake universe)"
        else:
            error_msg = f"API error: {e.response.status_code}"

        result = StocklakeResult(
            symbol=symbol,
            success=False,
            insider_activity=[],
            research_verdict=None,
            news_catalyst=None,
            error=error_msg,
            cached_at=dt.datetime.now().isoformat(),
        )

        # Still cache errors so we know the status
        cache[symbol] = result
        _save_cache(cache)

        return result

    except Exception as e:
        error_msg = f"Request failed: {str(e)}"
        return StocklakeResult(
            symbol=symbol,
            success=False,
            insider_activity=[],
            research_verdict=None,
            news_catalyst=None,
            error=error_msg,
            cached_at=dt.datetime.now().isoformat(),
        )


def screen_batch(
    symbols: list[str],
    enable_refresh: bool = False,
) -> list[StocklakeResult]:
    """Fetch insider activity for multiple symbols.

    Args:
        symbols: list of tickers to screen
        enable_refresh: if False, use cache only; if True, fetch fresh data

    Returns:
        List of StocklakeResult, one per symbol.
    """
    results = []
    for symbol in symbols:
        result = get_insider_activity(symbol, use_cache=not enable_refresh)
        results.append(result)
        if result.error and "quota" in result.error.lower():
            print(f"\n⚠️  Quota exhausted after {symbol}. Stopping.")
            break
    return results


def print_findings(results: list[StocklakeResult]) -> None:
    """Pretty-print screening results."""
    for r in results:
        status = "✓" if r.success else "✗"
        print(f"\n{status} {r.symbol}")
        if r.error:
            print(f"  Error: {r.error}")
        else:
            if r.insider_activity:
                print(f"  Insider activity: {len(r.insider_activity)} recent transactions")
                for finding in r.insider_activity[:3]:  # Show top 3
                    print(
                        f"    • {finding.date}: {finding.name} ({finding.title}) "
                        f"{finding.action.upper()} ${finding.amount:,.0f} ({finding.trend})"
                    )
            if r.research_verdict:
                print(f"  Research: {r.research_verdict}")
            if r.news_catalyst:
                print(f"  Catalyst: {r.news_catalyst[:80]}...")
        print(f"  Cached: {r.cached_at}")


def main():
    parser = argparse.ArgumentParser(
        description="Stocklake Pro insider activity screener (manual toggle)"
    )
    parser.add_argument(
        "--symbol", type=str, help="Single symbol to screen"
    )
    parser.add_argument(
        "--symbols", type=str, help="Comma-separated symbols to screen"
    )
    parser.add_argument(
        "--enable",
        action="store_true",
        help="Enable API refresh (fetch fresh data). Omit to use cache only.",
    )
    parser.add_argument(
        "--disable",
        action="store_true",
        help="Disable API refresh (use cache only). This is the default.",
    )
    args = parser.parse_args()

    if not args.symbol and not args.symbols:
        parser.print_help()
        return

    symbols = []
    if args.symbol:
        symbols.append(args.symbol)
    if args.symbols:
        symbols.extend(args.symbols.split(","))

    symbols = [s.strip().upper() for s in symbols if s.strip()]

    enable_refresh = args.enable and not args.disable
    if not enable_refresh:
        print("📦 Cache mode (--disable is default; pass --enable to refresh from API)")

    results = screen_batch(symbols, enable_refresh=enable_refresh)
    print_findings(results)


if __name__ == "__main__":
    main()
