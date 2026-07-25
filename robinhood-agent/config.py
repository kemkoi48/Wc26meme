"""Load and validate config (YAML or JSON) into typed dataclasses."""

from __future__ import annotations

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
    # The brokerage account the bot is allowed to act on. Resolved from the
    # ROBINHOOD_ACCOUNT_NUMBER env var (preferred) or the config file. When set,
    # the risk guard denies any order/cancel aimed at a different account.
    account_number: str | None = None


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
        ),
        tool_classification=ToolClassification(
            order_patterns=[str(p).lower() for p in (tc.get("order_patterns") or [])],
            cancel_patterns=[str(p).lower() for p in (tc.get("cancel_patterns") or [])],
            read_patterns=[str(p).lower() for p in (tc.get("read_patterns") or [])],
        ),
    )

    if not cfg.strategy:
        raise ValueError(f"{path}: `strategy` must not be empty")
    if cfg.risk.max_order_notional_usd <= 0:
        raise ValueError(f"{path}: risk.max_order_notional_usd must be > 0")
    return cfg
