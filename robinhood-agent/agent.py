"""Build the Agent SDK options and run one trading cycle."""

from __future__ import annotations

import os

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    SystemMessage,
    query,
)

from config import Config
from risk import RiskGuard


def _system_prompt(cfg: Config, live: bool) -> str:
    r = cfg.risk
    mode = "LIVE — approved orders will execute for real" if live else "DRY RUN — no orders will be placed"
    allowlist = ", ".join(r.symbol_allowlist) if r.symbol_allowlist else "(none configured — all orders will be denied)"
    account_line = (
        f"Account: {cfg.account_number} — operate ONLY on this account; pass this "
        f"account_number to every account-scoped tool.\n"
        if cfg.account_number
        else "Account: NOT configured — set ROBINHOOD_ACCOUNT_NUMBER; orders will be denied.\n"
    )
    return (
        f"{cfg.strategy}\n\n"
        "--- Operating context (enforced in code, not negotiable) ---\n"
        f"Mode: {mode}.\n"
        f"{account_line}"
        f"Tradable symbols: {allowlist}.\n"
        f"Per-order limit: ${r.max_order_notional_usd:,.2f}. "
        f"Max orders per run: {r.max_orders_per_run}. Max per day: {r.max_orders_per_day}.\n"
        f"Buys {'allowed' if r.allow_buy else 'disabled'}, "
        f"sells {'allowed' if r.allow_sell else 'disabled'}, "
        f"cancels {'allowed' if r.allow_cancel else 'disabled'}.\n"
        "A risk guard evaluates every tool call before it runs. If it denies a "
        "call, accept the denial, report it in your summary, and stop — do not "
        "attempt to circumvent it."
    )


def build_options(cfg: Config, guard: RiskGuard, live: bool) -> ClaudeAgentOptions:
    token = os.environ.get("ROBINHOOD_ACCESS_TOKEN", "").strip()
    if not token:
        raise RuntimeError(
            "ROBINHOOD_ACCESS_TOKEN is not set. Put it in .env (see .env.example)."
        )

    return ClaudeAgentOptions(
        model=cfg.model,
        system_prompt=_system_prompt(cfg, live),
        mcp_servers={
            cfg.mcp_server_name: {
                "type": "http",
                "url": cfg.mcp_url,
                "headers": {"Authorization": f"Bearer {token}"},
            }
        },
        # can_use_tool is the single authority for every tool call. We do NOT
        # wildcard-allow the Robinhood tools, so each call is routed through the
        # guard rather than auto-approved.
        can_use_tool=guard.can_use_tool,
        permission_mode="default",
        max_turns=30,
    )


async def run_cycle(cfg: Config, *, live: bool) -> None:
    guard = RiskGuard(cfg, live=live)
    options = build_options(cfg, guard, live)

    prompt = (
        "Run one trading cycle now following your strategy and the operating "
        "context. Finish with a short plain-language summary of what you "
        "observed, what you did or why you did nothing, and any risk-guard "
        "denials."
    )

    print(f"[cycle] mode={'LIVE' if live else 'DRY RUN'} model={cfg.model}")
    async for message in query(prompt=prompt, options=options):
        if isinstance(message, SystemMessage) and message.subtype == "init":
            for server in message.data.get("mcp_servers", []):
                status = server.get("status")
                if status in ("failed", "needs-auth"):
                    print(f"[warn] Robinhood MCP server status: {status} "
                          f"(check ROBINHOOD_ACCESS_TOKEN / authorization)")
        elif isinstance(message, AssistantMessage):
            for block in message.content:
                if getattr(block, "type", None) == "text":
                    print(block.text)
                elif getattr(block, "name", "").startswith("mcp__"):
                    print(f"[tool] {block.name} {getattr(block, 'input', {})}")
        elif isinstance(message, ResultMessage):
            print(f"[cycle] done. orders placed this run: {guard.orders_this_run}")
