"""Load and validate config.yaml into typed dataclasses."""

from __future__ import annotations

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


@dataclass
class Config:
    model: str
    mcp_server_name: str
    mcp_url: str
    strategy: str
    risk: RiskConfig
    tool_classification: ToolClassification


def load_config(path: str | Path = "config.yaml") -> Config:
    raw = yaml.safe_load(Path(path).read_text())
    if not isinstance(raw, dict):
        raise ValueError(f"{path} did not parse to a mapping")

    mcp = raw.get("mcp", {}) or {}
    risk = raw.get("risk", {}) or {}
    tc = raw.get("tool_classification", {}) or {}

    cfg = Config(
        model=raw.get("model", "claude-opus-4-8"),
        mcp_server_name=mcp.get("server_name", "robinhood"),
        mcp_url=mcp.get("url", "https://agent.robinhood.com/mcp/trading"),
        strategy=raw.get("strategy", "").strip(),
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
        ),
    )

    if not cfg.strategy:
        raise ValueError("config.yaml: `strategy` must not be empty")
    if cfg.risk.max_order_notional_usd <= 0:
        raise ValueError("config.yaml: risk.max_order_notional_usd must be > 0")
    return cfg
