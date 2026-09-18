"""Read-only option mispricing scanner (S7 catalyst screen).

Finds contracts that are cheap because the market has UNDERPRICED a coming
catalyst -- not merely cheap in dollars. See option_math.py for why those
are different things, and strategies.md S7 for the strategy.

This is a REPORT, not a trading input:
  - No order/cancel/exercise tool is offered to this session -- structurally
    absent, not merely denied, same as screener.py and momentum_scanner.py.
  - Selection is a pure function (option_math.apply_filters_and_rank) you
    can read and test independently; see test_option_math.py, which replays
    a real ENVX chain and asserts the screen rejects it.
  - Output goes to option_candidates.json, which nothing else in this repo
    reads. run.py only ever reads daily_allowlist.json. This scanner never
    writes that file and never will.

The catalyst itself is NOT verifiable by any connected tool -- the same
unsolved gap as S3's fifth pillar. The model records what it found in
`notes`; code never treats that as a pass/fail gate. A perfect mismatch
ratio on an imagined catalyst is still a losing trade.

    python option_scanner.py --config config.json
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

from config import Config, load_config
from option_math import OptionScanConfig, apply_filters_and_rank

_collected: list[dict[str, Any]] = []


def _make_recorder_server():
    @tool(
        "record_option_candidate",
        "Record ONE option contract you examined for the catalyst-mispricing "
        "screen. Call this once per contract, including ones that look "
        "unattractive -- selection is made afterward by fixed numeric rules "
        "in code, not by you.",
        {
            "symbol": str,
            "underlying_price": float,
            # The catalyst. catalyst_timing must be 'am' or 'pm' for earnings:
            # a pm report moves the stock the NEXT session, and an option
            # expiring before that is structurally worthless.
            "catalyst_date": str,
            "catalyst_timing": str,
            "catalyst_type": str,
            # The contract being evaluated.
            "expiration_date": str,
            "strike": float,
            "type": str,
            "bid": float,
            "ask": float,
            "iv": float,
            "delta": float,
            "open_interest": float,
            "volume": float,
            # The AT-THE-MONEY straddle for the SAME expiration -- this is
            # what prices the expected move. Not the contract above unless
            # that contract happens to be the ATM strike.
            "atm_call_mid": float,
            "atm_put_mid": float,
            # Past moves as percentages, e.g. [-8.4, 2.6, -20.1]. Signed is
            # fine; magnitude is what gets used. At least two are required.
            "historical_moves": list,
            "notes": str,
        },
    )
    async def record_option_candidate(args: dict[str, Any]) -> dict[str, Any]:
        _collected.append(dict(args))
        return {
            "content": [
                {"type": "text", "text": f"Recorded {args.get('symbol')} "
                 f"{args.get('strike')}{args.get('type')} "
                 f"{args.get('expiration_date')}."}
            ]
        }

    return create_sdk_mcp_server(
        name="option_scanning", version="1.0.0", tools=[record_option_candidate]
    )


def _scan_config(cfg: Config) -> OptionScanConfig:
    """Read the option_scan block off the loaded config, tolerating its
    absence so an older config.json still runs at documented defaults."""
    raw = getattr(cfg, "option_scan", None)
    if isinstance(raw, OptionScanConfig):
        return raw
    if isinstance(raw, dict):
        known = OptionScanConfig.__dataclass_fields__
        return OptionScanConfig(**{k: v for k, v in raw.items() if k in known})
    return OptionScanConfig()


def _write_report(
    selected: list[dict[str, Any]],
    rejected: list[dict[str, str]],
    examined: int,
    path: str | Path = "option_candidates.json",
) -> None:
    record = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "examined": examined,
        "candidates": selected,
        "rejected": rejected,
        "note": "Research report only. Nothing in this repo reads this file "
        "-- it is not an allowlist and does not feed run.py. A low mismatch "
        "ratio means the option is cheap relative to this name's own "
        "history; it says nothing about direction, and nothing about "
        "whether the catalyst is real.",
    }
    Path(path).write_text(json.dumps(record, indent=2))


SYSTEM_PROMPT = """\
You are a market data researcher, NOT a trader. You have READ-ONLY access --
there is no order-placing tool in this session, so do not attempt to trade.

Your job: find option contracts that may be UNDERPRICED relative to a coming
catalyst. A contract being cheap in dollars is NOT the signal -- most cheap
contracts are cheap because they are far out-of-the-money and implied
volatility is already elevated for a known event. The signal is the market
pricing a SMALLER move than the stock historically makes on similar events.

Process:
1. Call get_earnings_calendar for the next 2 weeks to find dated catalysts.
   Earnings are the only catalyst type any tool here can confirm. If the
   operator named other candidates, use those too and say in `notes` what
   the catalyst is and how you know -- never invent one.
2. For each candidate symbol:
   a. get_equity_quotes for the current underlying price. Skip anything
      outside roughly $2-$100.
   b. get_earnings_results to get PAST report dates AND their am/pm timing.
   c. get_equity_historicals (interval=day) covering those past reports.
      DISCARD any bar with interpolated=true or volume=0 BEFORE computing
      anything. Those bars are synthesized to fill gaps and carry no
      information -- a delisting, halt, or post-bankruptcy reorganization
      leaves long runs of them at a flat price, which produce a string of
      fake 0.0% moves and make the stock look far calmer than it is. This
      is not hypothetical: on 2026-08-12 WOLF returned 169 synthesized bars
      out of 331, flat at $1.54 with zero volume, which silently turned
      three of its six earnings moves into 0.0%.
      Then compute each past move as the close-to-close percent change from
      the report date's close to the NEXT session's close for a 'pm'
      report, or from the prior session's close to the report date's close
      for 'am'. Skip any report whose surrounding bars were discarded
      rather than reaching across the gap -- a move measured across a
      months-long hole is not a move.
      You need at least two such moves; if you cannot compute two, record
      the candidate anyway with what you have and the code will exclude it.
      Say in `notes` how many reports you had to skip and why.
   d. get_option_chains, then get_option_instruments for the first
      expiration that falls AFTER the catalyst moves the stock. For a 'pm'
      report on date D the move happens on D+1, so an expiry on D is
      worthless -- do not select it.
   e. get_option_quotes for: the AT-THE-MONEY call and put at that
      expiration (these price the expected move), plus the specific
      cheaper out-of-the-money contract(s) you are evaluating.
3. Call record_option_candidate once per contract examined. Report bid/ask
   exactly as quoted -- report 0 if a side genuinely has no quote; never
   substitute a last-trade price, and never skip a contract because its
   numbers look bad. Code decides, not you.

Put anything you notice about the catalyst -- news, sentiment, insider
activity, an approaching technical breakout, or the ABSENCE of a clear
reason -- in `notes`. No tool here can confirm a catalyst is real, so this
is informational for a human reader and is never filtered on.

Do not skip a symbol you decided to examine."""


async def run_scan(cfg: Config) -> None:
    token = os.environ.get("ROBINHOOD_ACCESS_TOKEN", "").strip()
    if not token:
        raise RuntimeError("ROBINHOOD_ACCESS_TOKEN is not set. Put it in .env.")

    oc = _scan_config(cfg)
    server = _make_recorder_server()

    # Built once, used for BOTH allowed_tools and the permission callback, so
    # the two cannot drift apart (see screener.py). No order/cancel/exercise
    # tool appears at all -- there is nothing for the model to attempt.
    allowed = [
        f"mcp__{cfg.mcp_server_name}__get_earnings_calendar",
        f"mcp__{cfg.mcp_server_name}__get_earnings_results",
        f"mcp__{cfg.mcp_server_name}__get_equity_quotes",
        f"mcp__{cfg.mcp_server_name}__get_equity_historicals",
        f"mcp__{cfg.mcp_server_name}__get_equity_fundamentals",
        f"mcp__{cfg.mcp_server_name}__get_option_chains",
        f"mcp__{cfg.mcp_server_name}__get_option_instruments",
        f"mcp__{cfg.mcp_server_name}__get_option_quotes",
        "mcp__option_scanning__record_option_candidate",
    ]
    allowed_set = set(allowed)

    async def _permission(tool_name: str, input_data: dict[str, Any], context: Any):
        if tool_name in allowed_set:
            return PermissionResultAllow(updated_input=input_data)
        return PermissionResultDeny(
            message="This scan only permits read-only market-data tools; it "
            "cannot place, cancel, or modify any order.",
            interrupt=False,
        )

    options = ClaudeAgentOptions(
        model=cfg.model,
        system_prompt=SYSTEM_PROMPT,
        mcp_servers={
            cfg.mcp_server_name: {
                "type": "http",
                "url": cfg.mcp_url,
                "headers": {"Authorization": f"Bearer {token}"},
            },
            "option_scanning": server,
        },
        allowed_tools=allowed,
        can_use_tool=_permission,
        permission_mode="default",
        max_turns=120,
    )

    _collected.clear()
    print("[option_scanner] scanning for catalyst-mispriced contracts...")
    async for message in query(prompt="Begin the option scan now.", options=options):
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

    print(f"[option_scanner] {len(_collected)} contract report(s) received.")
    selected, rejected = apply_filters_and_rank(_collected, oc)
    _write_report(selected, rejected, len(_collected))

    if rejected:
        print(f"[option_scanner] {len(rejected)} excluded:")
        for r in rejected[:20]:
            print(f"    {r['symbol']}: {r['reason']}")

    if not selected:
        print("[option_scanner] No contract passed. That is the expected "
              "result most days -- a genuine volatility mismatch is rare, "
              "and the screen is built to say no. Wrote an empty report.")
        return

    print("[option_scanner] Candidates (research only, NOT tradable via this repo):")
    for c in selected:
        strike = c["strike"] if c["strike"] is not None else float("nan")
        print(
            f"    {c['symbol']} ${strike:g}{c['type'][:1]} {c['expiration_date']}"
            f"  ${c['ask']:.2f} (${c['premium_usd']:.0f}/contract)"
            f"  delta {c['delta']:+.2f}  spread {c['spread_pct']:.1f}%"
        )
        print(
            f"        market prices {c['expected_move_pct']:.1f}% vs "
            f"{c['historical_move_pct']:.1f}% historical  -> ratio "
            f"{c['mismatch_ratio']:.2f}  ({c['catalyst_type']} "
            f"{c['catalyst_date']})"
        )
        if c.get("iv_disagreement_pct") is not None and c["iv_disagreement_pct"] > 35:
            print(
                f"        [check] straddle and IV expected-move disagree by "
                f"{c['iv_disagreement_pct']:.0f}% -- one input may be stale"
            )
        if c["notes"]:
            print(f"        notes: {c['notes']}")
    print("[option_scanner] Wrote option_candidates.json")
    print("[option_scanner] Reminder: a low ratio means cheap versus this "
          "name's own history. It is not a direction call, and it does not "
          "verify the catalyst is real.")


def main() -> None:
    load_dotenv()
    p = argparse.ArgumentParser(
        description="Read-only option catalyst-mispricing scanner (report only)."
    )
    p.add_argument("--config", default="config.json", help="Path to config file.")
    args = p.parse_args()
    cfg = load_config(args.config)
    asyncio.run(run_scan(cfg))


if __name__ == "__main__":
    main()
