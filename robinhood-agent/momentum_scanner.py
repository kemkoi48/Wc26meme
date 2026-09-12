"""Read-only momentum scanner (Warrior-Trading-style stock selection).

Surfaces market-wide candidates matching the "5 pillars" of momentum stock
selection described in sources.md (relative volume, % gain, price range,
float, plus a notes field since no connected tool can verify news/catalyst).
See sources.md's "Warrior Trading" entry for the strategy this mirrors and
why it is NOT wired into trading.

This is a REPORT, not a trading input:
  - No order/cancel/exercise tool is offered to this session -- structurally
    absent, not just denied, same as screener.py.
  - Selection against the 4 numerically-verifiable pillars is a pure function
    (apply_filters_and_rank) you can read and test independently.
  - Output goes to momentum_candidates.json, a file nothing else in this repo
    reads. run.py only ever reads daily_allowlist.json (written by
    screener.py). This scanner never writes that file and never will: the
    strategy it surfaces requires same-day round trips that trip good-faith
    violations on this account's cash-account settlement, and its exit logic
    depends on continuous real-time tape/Level-2 reading that a polling bot
    structurally cannot do. Use this to look at candidates yourself, not to
    feed an automated buy.

    python momentum_scanner.py --config config.json
"""

from __future__ import annotations

import argparse
import asyncio
import datetime as dt
import json
import os
from pathlib import Path
from typing import Any

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    PermissionResultAllow,
    PermissionResultDeny,
    ResultMessage,
    SystemMessage,
    create_sdk_mcp_server,
    query,
    tool,
)
from dotenv import load_dotenv

from config import Config, MomentumScanConfig, load_config

_collected: list[dict[str, Any]] = []


def _make_recorder_server():
    @tool(
        "record_momentum_candidate",
        "Record research findings for ONE symbol found while scanning for "
        "today's strongest movers. Call this once per symbol you examine, "
        "even ones that look unattractive -- the actual selection is made by "
        "code afterward against fixed numeric thresholds, not by you.",
        {
            "symbol": str,
            "price": float,
            "pct_change": float,
            "volume": float,
            "avg_volume": float,
            "float_shares": float,
            # Live quote from get_equity_quotes. Report both, even when the
            # spread looks bad -- the exclusion is code's job, not yours.
            # Report 0 for either only if the quote genuinely has no bid or
            # ask; that is treated as unusable data and excluded.
            "bid": float,
            "ask": float,
            "notes": str,
        },
    )
    async def record_momentum_candidate(args: dict[str, Any]) -> dict[str, Any]:
        _collected.append(dict(args))
        return {"content": [{"type": "text", "text": f"Recorded {args.get('symbol')}."}]}

    return create_sdk_mcp_server(
        name="momentum_scanning", version="1.0.0", tools=[record_momentum_candidate]
    )


def apply_filters_and_rank(
    candidates: list[dict[str, Any]], cfg: MomentumScanConfig
) -> list[dict[str, Any]]:
    """THE safety-critical function. Claude's reported numbers are untrusted
    input: anything malformed, or outside the configured thresholds, is
    excluded. Only the numerically-verifiable pillars are enforced here --
    relative volume, % change, price range, float, and quoted spread --
    because no connected tool can verify a news catalyst; that stays in
    `notes` for a human to read, never a pass/fail gate. Survivors are ranked
    by relative volume (the strongest demand/supply imbalance) and capped at
    top_n.

    On spread: enforced as (ask - bid) / midpoint, the standard quoted-spread
    percentage. A missing, zero, or crossed (bid > ask) quote is treated as
    unusable and excluded -- same fail-closed posture as every other field.
    A candidate sitting exactly on max_spread_pct may fall either side of the
    line depending on float representation; that is acceptable for a research
    filter and not worth an epsilon, but don't read the boundary as exact.
    This is the one filter that measures tradability rather than momentum: a
    name can pass all four momentum pillars and still be untradable, which is
    exactly what price-floor filtering fails to catch."""
    passed: list[dict[str, Any]] = []
    for c in candidates:
        try:
            symbol = str(c["symbol"]).upper().strip()
            price = float(c["price"])
            pct_change = float(c["pct_change"])
            volume = float(c["volume"])
            avg_volume = float(c["avg_volume"])
            float_shares = float(c["float_shares"])
            bid = float(c["bid"])
            ask = float(c["ask"])
        except (KeyError, TypeError, ValueError):
            continue  # malformed report -> exclude, fail closed
        if not symbol or avg_volume <= 0 or float_shares <= 0:
            continue
        if bid <= 0 or ask <= 0 or ask < bid:
            continue  # no/crossed quote -> not tradable, fail closed
        spread_pct = (ask - bid) / ((ask + bid) / 2.0) * 100.0
        if spread_pct > cfg.max_spread_pct:
            continue
        relative_volume = volume / avg_volume
        if relative_volume < cfg.min_relative_volume:
            continue
        if pct_change < cfg.min_pct_change:
            continue
        if not (cfg.min_price <= price <= cfg.max_price):
            continue
        if float_shares > cfg.max_float:
            continue
        passed.append({
            "symbol": symbol,
            "price": price,
            "pct_change": pct_change,
            "relative_volume": relative_volume,
            "float_shares": float_shares,
            "spread_pct": spread_pct,
            "notes": str(c.get("notes", ""))[:300],
        })
    passed.sort(key=lambda c: c["relative_volume"], reverse=True)
    return passed[: max(0, cfg.top_n)]


def _write_report(
    selected: list[dict[str, Any]],
    all_examined: int,
    path: str | Path = "momentum_candidates.json",
) -> None:
    record = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "examined": all_examined,
        "candidates": selected,
        "note": "Research report only. Nothing in this repo reads this file "
        "-- it is not an allowlist and does not feed run.py.",
    }
    Path(path).write_text(json.dumps(record, indent=2))


async def run_scan(cfg: Config) -> None:
    token = os.environ.get("ROBINHOOD_ACCESS_TOKEN", "").strip()
    if not token:
        raise RuntimeError("ROBINHOOD_ACCESS_TOKEN is not set. Put it in .env.")

    mc = cfg.momentum_scan
    server = _make_recorder_server()

    # Built once, used for BOTH allowed_tools and the permission callback (see
    # screener.py's comment on why -- avoids the two drifting apart). Only
    # scanner/data-lookup tools; no order/cancel/exercise tool appears here at
    # all, so there's nothing for the model to even attempt to place.
    allowed = [
        f"mcp__{cfg.mcp_server_name}__get_scanner_filter_specs",
        f"mcp__{cfg.mcp_server_name}__get_scans",
        f"mcp__{cfg.mcp_server_name}__run_scan",
        f"mcp__{cfg.mcp_server_name}__create_scan",
        f"mcp__{cfg.mcp_server_name}__update_scan_filters",
        f"mcp__{cfg.mcp_server_name}__get_equity_fundamentals",
        f"mcp__{cfg.mcp_server_name}__get_equity_quotes",
        "mcp__momentum_scanning__record_momentum_candidate",
    ]
    allowed_set = set(allowed)

    async def _permission(tool_name: str, input_data: dict[str, Any], context: Any):
        if tool_name in allowed_set:
            return PermissionResultAllow(updated_input=input_data)
        return PermissionResultDeny(
            message="This scan only permits read-only scanner/data-lookup "
            "tools; it cannot place, cancel, or modify any order.",
            interrupt=False,
        )

    system_prompt = (
        "You are a market data researcher, NOT a trader. You have READ-ONLY "
        "access -- there is no order-placing tool available to you in this "
        "session, so do not attempt to trade anything.\n\n"
        "Find today's strongest momentum stocks using this process:\n"
        "1. Call get_scanner_filter_specs to see valid filter types.\n"
        "2. Call get_scans. If a saved scan already sorts by % change or "
        "relative volume (e.g. a 'gainers' or 'most active' scan), run it "
        "with run_scan. Otherwise use create_scan or update_scan_filters to "
        "build one sorted by percentage change descending, then run_scan it.\n"
        "3. Take up to the top 25 rows from the scan result.\n"
        "4. For each of those symbols, call get_equity_fundamentals to get: "
        "current price, % change on the day, today's volume, average daily "
        "volume, and float (shares available to trade). Then ALSO call "
        "get_equity_quotes for the same symbols to get the live bid and ask "
        "-- these are required, and a wide bid/ask spread is how an "
        "untradable stock is detected regardless of how good its momentum "
        "looks. Report bid and ask as quoted; do not skip a symbol because "
        "its spread looks bad, and do not substitute the last trade price "
        "for a missing bid or ask (report 0 instead).\n"
        "5. Call record_momentum_candidate exactly once per symbol you "
        "examined, even ones that look weak -- the actual selection is made "
        "afterward by fixed numeric rules in code, not by your judgment. Put "
        "anything you notice about a possible catalyst (or the absence of "
        "one) in the notes field -- no tool here can confirm real news, so "
        "this is informational only, not a criterion you should filter on "
        "yourself.\n\n"
        "Do not skip any symbol from the scan result you decided to examine."
    )

    options = ClaudeAgentOptions(
        model=cfg.model,
        system_prompt=system_prompt,
        mcp_servers={
            cfg.mcp_server_name: {
                "type": "http",
                "url": cfg.mcp_url,
                "headers": {"Authorization": f"Bearer {token}"},
            },
            "momentum_scanning": server,
        },
        allowed_tools=allowed,
        can_use_tool=_permission,
        permission_mode="default",
        max_turns=60,
    )

    _collected.clear()
    print("[momentum_scanner] scanning the market for today's strongest movers...")
    async for message in query(prompt="Begin the momentum scan now.", options=options):
        if isinstance(message, SystemMessage) and message.subtype == "init":
            for s in message.data.get("mcp_servers", []):
                if s.get("status") in ("failed", "needs-auth"):
                    print(f"[warn] MCP server '{s.get('name')}' status: {s.get('status')}")
        elif isinstance(message, AssistantMessage):
            for block in message.content:
                if getattr(block, "type", None) == "text":
                    print(block.text)
        elif isinstance(message, ResultMessage):
            pass

    print(f"[momentum_scanner] {len(_collected)} candidate report(s) received.")
    selected = apply_filters_and_rank(_collected, mc)
    _write_report(selected, len(_collected))
    if not selected:
        print("[momentum_scanner] No candidate passed the configured filters "
              "(relative volume / % change / price range / float / spread). "
              "Wrote an empty report to momentum_candidates.json.")
        return

    print(f"[momentum_scanner] Top candidates (research only, not tradable "
          f"via this repo):")
    for c in selected:
        print(f"    {c['symbol']}: ${c['price']:.2f}  +{c['pct_change']:.1f}%  "
              f"rel.vol {c['relative_volume']:.1f}x  float "
              f"{c['float_shares']:,.0f}  spread {c['spread_pct']:.2f}%"
              f"  -- {c['notes']}")
    print("[momentum_scanner] Wrote momentum_candidates.json")


def main() -> None:
    load_dotenv()
    p = argparse.ArgumentParser(
        description="Read-only market-wide momentum scanner (research report only)."
    )
    p.add_argument("--config", default="config.json", help="Path to config file.")
    args = p.parse_args()
    cfg = load_config(args.config)
    asyncio.run(run_scan(cfg))


if __name__ == "__main__":
    main()
