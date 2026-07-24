"""RiskGuard: the deterministic gate every tool call passes through.

The guard is intentionally simple and fail-closed. It does not trust the model
to respect limits — it enforces them in code, and denies anything it cannot
confidently validate.
"""

from __future__ import annotations

import datetime as dt
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from claude_agent_sdk import PermissionResultAllow, PermissionResultDeny

from config import Config

# Field names commonly used across order APIs. We match defensively rather than
# assume Robinhood's exact schema.
_SYMBOL_KEYS = ("symbol", "ticker", "instrument", "asset", "stock")
_SIDE_KEYS = ("side", "action", "direction", "order_side", "type")
_QTY_KEYS = ("quantity", "qty", "shares", "units", "amount_shares")
_NOTIONAL_KEYS = (
    "notional",
    "amount",
    "amount_usd",
    "amount_in_dollars",
    "dollar_amount",
    "dollars",
    "cash_amount",
    "value",
)
_PRICE_KEYS = ("price", "limit_price", "estimated_price", "last_price", "quote")
_ACCOUNT_KEYS = ("account_number", "account", "account_id", "rhs_account_number")


@dataclass
class Decision:
    allow: bool
    reason: str


def _first(d: dict[str, Any], keys: tuple[str, ...]) -> Any:
    for k in keys:
        if k in d and d[k] not in (None, ""):
            return d[k]
    return None


def _to_float(v: Any) -> float | None:
    try:
        return float(str(v).replace("$", "").replace(",", "").strip())
    except (TypeError, ValueError):
        return None


class RiskGuard:
    def __init__(
        self,
        config: Config,
        *,
        live: bool,
        state_path: str | Path = "state.json",
        audit_path: str | Path = "audit.jsonl",
    ) -> None:
        self.cfg = config
        self.live = live
        self.state_path = Path(state_path)
        self.audit_path = Path(audit_path)
        self.orders_this_run = 0
        self._server_prefix = f"mcp__{config.mcp_server_name}__"

    # ---- classification -------------------------------------------------

    def classify(self, tool_name: str) -> str:
        """Return 'order', 'cancel', 'read', or 'foreign'."""
        if not tool_name.startswith(self._server_prefix):
            return "foreign"
        bare = tool_name[len(self._server_prefix) :].lower()
        tc = self.cfg.tool_classification
        if any(p in bare for p in tc.cancel_patterns):
            return "cancel"
        if any(p in bare for p in tc.order_patterns):
            return "order"
        return "read"

    # ---- daily counter persistence -------------------------------------

    def _today(self) -> str:
        return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")

    def _load_state(self) -> dict[str, Any]:
        if self.state_path.exists():
            try:
                return json.loads(self.state_path.read_text())
            except (json.JSONDecodeError, OSError):
                pass
        return {}

    def _orders_today(self) -> int:
        state = self._load_state()
        if state.get("date") != self._today():
            return 0
        return int(state.get("orders", 0))

    def _record_order(self) -> None:
        self.orders_this_run += 1
        state = self._load_state()
        if state.get("date") != self._today():
            state = {"date": self._today(), "orders": 0}
        state["orders"] = int(state.get("orders", 0)) + 1
        self.state_path.write_text(json.dumps(state))

    # ---- audit ----------------------------------------------------------

    def _audit(self, tool_name: str, kind: str, decision: Decision, input_data: Any) -> None:
        record = {
            "ts": dt.datetime.now(dt.timezone.utc).isoformat(),
            "tool": tool_name,
            "kind": kind,
            "live": self.live,
            "allow": decision.allow,
            "reason": decision.reason,
            "input": input_data,
        }
        with self.audit_path.open("a") as f:
            f.write(json.dumps(record, default=str) + "\n")

    # ---- the gate -------------------------------------------------------

    def evaluate(self, tool_name: str, input_data: dict[str, Any]) -> Decision:
        kind = self.classify(tool_name)

        if kind == "foreign":
            return Decision(False, "This bot may only call Robinhood MCP tools.")

        if kind == "read":
            return Decision(True, "read-only")

        # From here down: order or cancel — the risky operations.
        if kind == "cancel":
            if not self.cfg.risk.allow_cancel:
                return Decision(False, "Cancels are disabled (risk.allow_cancel=false).")
            if not self.live:
                return Decision(False, "Dry run: cancels are not executed.")
            acct_ok = self._account_ok(input_data)
            if acct_ok is not None:
                return acct_ok
            return Decision(True, "cancel allowed")

        # kind == "order"
        if not self.live:
            return Decision(
                False,
                "Dry run: order placement is blocked. Report the order you WOULD "
                "place and continue without placing it.",
            )

        acct_ok = self._account_ok(input_data)
        if acct_ok is not None:
            return acct_ok
        return self._check_order(input_data)

    def _account_ok(self, input_data: dict[str, Any]) -> Decision | None:
        """Enforce the configured account. Returns a Deny decision on a problem,
        or None if the account check passes / is not configured."""
        if not self.cfg.account_number:
            return None  # not configured -> rely on symbol/notional limits
        supplied = _first(input_data, _ACCOUNT_KEYS)
        if supplied is None:
            return Decision(False, "Order specifies no account; denied (fail-closed).")
        if str(supplied).strip() != self.cfg.account_number:
            return Decision(
                False,
                f"Order targets account {supplied}, not the configured "
                f"agentic account; denied.",
            )
        return None

    def _check_order(self, input_data: dict[str, Any]) -> Decision:
        r = self.cfg.risk

        # Run-level and day-level caps.
        if self.orders_this_run >= r.max_orders_per_run:
            return Decision(False, f"Per-run order cap reached ({r.max_orders_per_run}).")
        if self._orders_today() >= r.max_orders_per_day:
            return Decision(False, f"Per-day order cap reached ({r.max_orders_per_day}).")

        # Symbol allowlist. Empty allowlist = deny all (fail-closed).
        raw_symbol = _first(input_data, _SYMBOL_KEYS)
        if raw_symbol is None:
            return Decision(False, "Order has no recognizable symbol field; denied (fail-closed).")
        symbol = str(raw_symbol).upper()
        if not r.symbol_allowlist:
            return Decision(False, "Symbol allowlist is empty; all orders denied (fail-closed).")
        if symbol not in r.symbol_allowlist:
            return Decision(False, f"Symbol {symbol} is not on the allowlist.")

        # Side.
        side = _first(input_data, _SIDE_KEYS)
        side_str = str(side).lower() if side is not None else ""
        is_buy = "buy" in side_str
        is_sell = "sell" in side_str
        if not (is_buy or is_sell):
            return Decision(False, "Order side is not recognizably buy/sell; denied (fail-closed).")
        if is_buy and not r.allow_buy:
            return Decision(False, "Buys are disabled (risk.allow_buy=false).")
        if is_sell and not r.allow_sell:
            return Decision(False, "Sells are disabled (risk.allow_sell=false).")

        # Notional. Prefer an explicit dollar amount; otherwise quantity*price.
        notional = _to_float(_first(input_data, _NOTIONAL_KEYS))
        if notional is None:
            qty = _to_float(_first(input_data, _QTY_KEYS))
            price = _to_float(_first(input_data, _PRICE_KEYS))
            if qty is not None and price is not None:
                notional = qty * price
        if notional is None:
            return Decision(
                False,
                "Cannot determine order dollar size (no notional, and no "
                "quantity*price to compute it); denied (fail-closed).",
            )
        if notional <= 0:
            return Decision(False, "Computed order notional is not positive; denied.")
        if notional > r.max_order_notional_usd:
            return Decision(
                False,
                f"Order notional ${notional:,.2f} exceeds the "
                f"${r.max_order_notional_usd:,.2f} per-order limit.",
            )

        return Decision(True, f"{side_str} {symbol} ~${notional:,.2f} within limits")

    # ---- Agent SDK callback --------------------------------------------

    async def can_use_tool(
        self,
        tool_name: str,
        input_data: dict[str, Any],
        context: Any,  # ToolPermissionContext; unused
    ) -> PermissionResultAllow | PermissionResultDeny:
        decision = self.evaluate(tool_name, input_data)
        self._audit(tool_name, self.classify(tool_name), decision, input_data)
        if decision.allow:
            if self.classify(tool_name) == "order":
                self._record_order()
            return PermissionResultAllow(updated_input=input_data)
        return PermissionResultDeny(message=decision.reason, interrupt=False)
