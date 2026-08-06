"""Deterministic daily symbol screener.

Run this once per day, BEFORE the trading agent (see deploy/crontab.example).
It uses Claude with READ-ONLY Robinhood tools to gather liquidity/volatility
data on a fixed candidate universe you configure -- but WHICH symbols actually
make the cut is decided by hard, code-enforced numeric thresholds in
config.json's `screening:` section, not by the model's judgment. This mirrors
risk.py's philosophy: the model can research and recommend; code decides.

Safety properties:
  - No order/cancel/exercise tool is even offered to this session -- not just
    denied, structurally absent from both `allowed_tools` and the permission
    callback. This process cannot place a trade no matter what it decides.
  - Selection is a pure function (apply_filters_and_rank) you can read and
    unit test independently of any live call.
  - If screening fails, times out, or nothing passes the filters, NO new file
    is written. The trading agent then falls back to its static
    symbol_allowlist (config.py: load_daily_allowlist returns None for a
    missing/stale file) -- it never silently reuses an old list past its date,
    and it never falls open into "trade whatever."

    python screener.py --config config.json
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

from config import Config, ScreeningConfig, load_config

_collected: list[dict[str, Any]] = []


def _make_recorder_server():
    @tool(
        "record_candidate",
        "Record research findings for ONE candidate symbol from today's "
        "screening universe. Call this once per symbol after checking its "
        "data. Call it for every symbol you were asked to research, even ones "
        "that look unattractive -- the actual selection is made by code "
        "afterward, not by you.",
        {
            "symbol": str,
            "avg_dollar_volume": float,
            "atr_pct": float,
            "last_price": float,
            "notes": str,
        },
    )
    async def record_candidate(args: dict[str, Any]) -> dict[str, Any]:
        _collected.append(dict(args))
        return {"content": [{"type": "text", "text": f"Recorded {args.get('symbol')}."}]}

    return create_sdk_mcp_server(name="screening", version="1.0.0", tools=[record_candidate])


def apply_filters_and_rank(
    candidates: list[dict[str, Any]], cfg: ScreeningConfig
) -> list[dict[str, Any]]:
    """THE safety-critical function. Claude's reported numbers are treated as
    untrusted input: anything malformed, or outside the configured liquidity /
    volatility / price bounds, is excluded. Survivors are ranked by volatility
    (ATR%) -- more movement means more chances for the trend/reversal rules in
    the strategy prompt to actually trigger -- and capped at top_n."""
    passed: list[dict[str, Any]] = []
    for c in candidates:
        try:
            symbol = str(c["symbol"]).upper().strip()
            vol = float(c["avg_dollar_volume"])
            atr_pct = float(c["atr_pct"])
            price = float(c["last_price"])
        except (KeyError, TypeError, ValueError):
            continue  # malformed report -> exclude, fail closed
        if not symbol:
            continue
        if vol < cfg.min_avg_dollar_volume:
            continue
        if not (cfg.min_atr_pct <= atr_pct <= cfg.max_atr_pct):
            continue
        if not (cfg.min_price <= price <= cfg.max_price):
            continue
        passed.append({
            "symbol": symbol,
            "avg_dollar_volume": vol,
            "atr_pct": atr_pct,
            "last_price": price,
            "notes": str(c.get("notes", ""))[:300],
        })
    passed.sort(key=lambda c: c["atr_pct"], reverse=True)
    return passed[: max(0, cfg.top_n)]


def _write_allowlist(selected: list[dict[str, Any]], path: str | Path = "daily_allowlist.json") -> None:
    record = {
        "date": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d"),
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "symbols": [c["symbol"] for c in selected],
        "candidates": selected,
    }
    Path(path).write_text(json.dumps(record, indent=2))


async def run_screen(cfg: Config) -> None:
    token = os.environ.get("ROBINHOOD_ACCESS_TOKEN", "").strip()
    if not token:
        raise RuntimeError("ROBINHOOD_ACCESS_TOKEN is not set. Put it in .env.")

    sc = cfg.screening
    if not sc.candidate_universe:
        print("[screener] No screening.candidate_universe configured in the "
              "config file; nothing to screen.")
        return

    server = _make_recorder_server()

    # Built once, used for BOTH allowed_tools and the permission callback, so
    # the two can never drift out of sync with each other (unlike the earlier
    # order_patterns bug where guessed tool names didn't match the real ones).
    allowed = [
        f"mcp__{cfg.mcp_server_name}__get_equity_historicals",
        f"mcp__{cfg.mcp_server_name}__get_equity_quotes",
        f"mcp__{cfg.mcp_server_name}__get_equity_fundamentals",
        f"mcp__{cfg.mcp_server_name}__get_equity_technical_indicators",
        "mcp__screening__record_candidate",
    ]
    allowed_set = set(allowed)

    async def _permission(tool_name: str, input_data: dict[str, Any], context: Any):
        if tool_name in allowed_set:
            return PermissionResultAllow(updated_input=input_data)
        return PermissionResultDeny(
            message="This screening run only permits read-only research "
            "tools; it cannot place, cancel, or modify anything.",
            interrupt=False,
        )

    universe_str = ", ".join(sc.candidate_universe)
    system_prompt = (
        "You are a market data researcher, NOT a trader. You have READ-ONLY "
        "access -- there is no order-placing tool available to you in this "
        "session, so do not attempt to trade anything; focus only on "
        "gathering data.\n\n"
        f"Research each of these symbols: {universe_str}\n\n"
        "For each symbol, use the available read-only tools (historicals, "
        "quotes, fundamentals, technical indicators) to determine:\n"
        "  - avg_dollar_volume: its typical daily dollar trading volume "
        "(roughly average daily share volume x price) over the recent period "
        "the data covers.\n"
        "  - atr_pct: its Average True Range as a percentage of price (a "
        "volatility measure). If a direct ATR indicator isn't available, "
        "estimate it from recent daily high/low/close historicals.\n"
        "  - last_price: its most recent price.\n\n"
        "For EVERY symbol listed above, call record_candidate exactly once "
        "with these values plus a short notes string, even for symbols that "
        "look unattractive to you -- the actual selection is made afterward "
        "by fixed numeric rules in code, not by your judgment. Do not skip "
        "any symbol."
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
            "screening": server,
        },
        allowed_tools=allowed,
        can_use_tool=_permission,
        permission_mode="default",
        max_turns=60,
    )

    _collected.clear()
    print(f"[screener] researching {len(sc.candidate_universe)} candidates: {universe_str}")
    async for message in query(prompt="Begin the screening research now.", options=options):
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

    print(f"[screener] {len(_collected)} candidate report(s) received.")
    selected = apply_filters_and_rank(_collected, sc)
    if not selected:
        print("[screener] No candidate passed the configured filters "
              "(min_avg_dollar_volume / atr_pct range / price range). Not "
              "writing a new allowlist -- the bot falls back to its static "
              "symbol_allowlist (or denies all, if that's empty).")
        return

    _write_allowlist(selected)
    print(f"[screener] Selected: {', '.join(c['symbol'] for c in selected)}")
    for c in selected:
        print(f"    {c['symbol']}: ${c['last_price']:.2f}  ATR {c['atr_pct']:.2f}%  "
              f"avg $vol {c['avg_dollar_volume']:,.0f}  -- {c['notes']}")
    print("[screener] Wrote daily_allowlist.json")


def main() -> None:
    load_dotenv()
    p = argparse.ArgumentParser(description="Deterministic daily symbol screener.")
    p.add_argument("--config", default="config.json", help="Path to config file.")
    args = p.parse_args()
    cfg = load_config(args.config)
    asyncio.run(run_screen(cfg))


if __name__ == "__main__":
    main()
