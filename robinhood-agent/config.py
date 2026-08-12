"""Load and validate config (YAML or JSON) into typed dataclasses."""

from __future__ import annotations

import datetime as dt
import json
import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class RiskConfig:
    symbol_allowlist: list[str] = field(default_factory=list)
    max_order_notional_usd: float = 100.0
    max_orders_per_run: int = 3
    max_orders_per_day: int = 10
    allow_buy: bool = True
    allow_sell: bool = True
    allow_cancel: bool = False
    # If true, and a same-day daily_allowlist.json (written by screener.py)
    # exists, its symbols REPLACE symbol_allowlist for this run. If no valid
    # same-day file exists, symbol_allowlist above is used unchanged (fails
    # closed -- an empty symbol_allowlist still denies all orders).
    auto_screen: bool = False


@dataclass
class ScreeningConfig:
    """Controls screener.py, the deterministic daily symbol screener.

    Claude only GATHERS data (read-only tools). Whether a symbol is actually
    selected is decided by these numeric thresholds in code -- see
    apply_filters_and_rank() in screener.py.
    """
    candidate_universe: list[str] = field(default_factory=list)
    min_avg_dollar_volume: float = 10_000_000.0
    min_atr_pct: float = 1.0
    max_atr_pct: float = 8.0
    min_price: float = 1.0
    max_price: float = 2000.0
    top_n: int = 3


@dataclass
class MomentumScanConfig:
    """Controls momentum_scanner.py, the read-only Warrior-Trading-style
    momentum scanner (see sources.md for the strategy this mirrors).

    This is a RESEARCH report only -- momentum_scanner.py never writes
    daily_allowlist.json and is never read by run.py. That's deliberate: the
    strategy this scans for requires same-day round trips that trip
    good-faith violations on this account's cash-account settlement, so it
    is not wired into anything that can place an order.
    """
    min_relative_volume: float = 5.0
    min_pct_change: float = 10.0
    min_price: float = 2.0
    max_price: float = 20.0
    max_float: float = 20_000_000.0
    # Max quoted bid/ask spread as a percent of the midpoint. This is a
    # DIRECT liquidity measure -- unlike min_price, which only proxies
    # liquidity by assuming cheap == illiquid (an assumption that both misses
    # wide-spread expensive stocks and excludes tight-spread cheap ones; see
    # sources.md, Sincere entry). Live example: TISI quoted 21.55 x 22.55 on
    # 2026-08-11 == 4.54% spread, a bigger round-trip cost than most
    # realistic intraday edges on a small account.
    max_spread_pct: float = 1.0
    top_n: int = 10


@dataclass
class ToolClassification:
    order_patterns: list[str] = field(default_factory=list)
    cancel_patterns: list[str] = field(default_factory=list)
    read_patterns: list[str] = field(default_factory=list)


@dataclass
class Config:
    model: str
    mcp_server_name: str
    mcp_url: str
    strategy: str
    risk: RiskConfig
    tool_classification: ToolClassification
    screening: ScreeningConfig
    momentum_scan: MomentumScanConfig
    # The brokerage account the bot is allowed to act on. Resolved from the
    # ROBINHOOD_ACCOUNT_NUMBER env var (preferred) or the config file. When set,
    # the risk guard denies any order/cancel aimed at a different account.
    account_number: str | None = None


def load_daily_allowlist(path: str | Path = "daily_allowlist.json") -> list[str] | None:
    """Read screener.py's output. Returns None (fail closed) if the file is
    missing, unreadable, malformed, empty, or not from today (UTC) -- a stale
    file is never trusted, so a screener that stops running does not leave
    yesterday's picks silently active forever."""
    p = Path(path)
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text())
    except (json.JSONDecodeError, OSError):
        return None
    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    if data.get("date") != today:
        return None
    symbols = data.get("symbols")
    if not isinstance(symbols, list) or not symbols:
        return None
    return [str(s).upper() for s in symbols]


def _read_raw(path: Path) -> dict:
    text = path.read_text()
    if path.suffix.lower() == ".json":
        raw = json.loads(text)
    else:
        raw = yaml.safe_load(text)
    if not isinstance(raw, dict):
        raise ValueError(f"{path} did not parse to a mapping")
    return raw


def load_config(path: str | Path = "config.yaml") -> Config:
    path = Path(path)
    raw = _read_raw(path)

    mcp = raw.get("mcp", {}) or {}
    risk = raw.get("risk", {}) or {}
    tc = raw.get("tool_classification", {}) or {}
    sc = raw.get("screening", {}) or {}
    ms = raw.get("momentum_scan", {}) or {}

    # Account number: env var wins so the real value never has to live in a
    # committed config file.
    account_number = os.environ.get("ROBINHOOD_ACCOUNT_NUMBER") or raw.get("account_number")
    account_number = str(account_number).strip() if account_number else None

    cfg = Config(
        model=raw.get("model", "claude-opus-4-8"),
        mcp_server_name=mcp.get("server_name", "robinhood"),
        mcp_url=mcp.get("url", "https://agent.robinhood.com/mcp/trading"),
        strategy=str(raw.get("strategy", "")).strip(),
        account_number=account_number,
        risk=RiskConfig(
            symbol_allowlist=[str(s).upper() for s in (risk.get("symbol_allowlist") or [])],
            max_order_notional_usd=float(risk.get("max_order_notional_usd", 100.0)),
            max_orders_per_run=int(risk.get("max_orders_per_run", 3)),
            max_orders_per_day=int(risk.get("max_orders_per_day", 10)),
            allow_buy=bool(risk.get("allow_buy", True)),
            allow_sell=bool(risk.get("allow_sell", True)),
            allow_cancel=bool(risk.get("allow_cancel", False)),
            auto_screen=bool(risk.get("auto_screen", False)),
        ),
        tool_classification=ToolClassification(
            order_patterns=[str(p).lower() for p in (tc.get("order_patterns") or [])],
            cancel_patterns=[str(p).lower() for p in (tc.get("cancel_patterns") or [])],
            read_patterns=[str(p).lower() for p in (tc.get("read_patterns") or [])],
        ),
        screening=ScreeningConfig(
            candidate_universe=[str(s).upper() for s in (sc.get("candidate_universe") or [])],
            min_avg_dollar_volume=float(sc.get("min_avg_dollar_volume", 10_000_000.0)),
            min_atr_pct=float(sc.get("min_atr_pct", 1.0)),
            max_atr_pct=float(sc.get("max_atr_pct", 8.0)),
            min_price=float(sc.get("min_price", 1.0)),
            max_price=float(sc.get("max_price", 2000.0)),
            top_n=int(sc.get("top_n", 3)),
        ),
        momentum_scan=MomentumScanConfig(
            min_relative_volume=float(ms.get("min_relative_volume", 5.0)),
            min_pct_change=float(ms.get("min_pct_change", 10.0)),
            min_price=float(ms.get("min_price", 2.0)),
            max_price=float(ms.get("max_price", 20.0)),
            max_float=float(ms.get("max_float", 20_000_000.0)),
            max_spread_pct=float(ms.get("max_spread_pct", 1.0)),
            top_n=int(ms.get("top_n", 10)),
        ),
    )

    if not cfg.strategy:
        raise ValueError(f"{path}: `strategy` must not be empty")
    if cfg.risk.max_order_notional_usd <= 0:
        raise ValueError(f"{path}: risk.max_order_notional_usd must be > 0")

    # Auto-screen: a valid same-day screener output REPLACES the static
    # allowlist. No valid file -> keep the static list as-is (fail closed;
    # an empty static list still means "deny all orders").
    if cfg.risk.auto_screen:
        daily = load_daily_allowlist()
        if daily:
            cfg.risk.symbol_allowlist = daily

    return cfg
