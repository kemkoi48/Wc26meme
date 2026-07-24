# robinhood-agent

An **autonomous agentic trading bot** that connects Claude (via the
[Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk)) to Robinhood's
official Agentic Trading MCP endpoint (`https://agent.robinhood.com/mcp/trading`),
runs on a schedule, and executes a strategy **behind a deterministic risk
guard** that enforces hard limits in code before any order reaches Robinhood.

> ⚠️ **This bot can place real trades with real money.** Robinhood's own warning
> for agentic trading: strategies "may perform poorly under certain market
> conditions and may be difficult to monitor or stop in real time," and you can
> lose your entire investment. Start in `dry_run` mode. Read the whole of this
> file before going live.

## How it works

```
 run.py (scheduler)
    │
    ▼
 agent.py  ──►  Claude Agent SDK  ──►  Robinhood MCP (agent.robinhood.com/mcp/trading)
    │                  │
    │                  └── every tool call routes through ▼
    │
 risk.py  (RiskGuard.can_use_tool)   ◄── the deterministic safety layer
    │        • read-only tools .......... allowed
    │        • order/cancel tools ....... validated against hard limits, else DENIED
    │        • dry_run ................... all order/cancel tools DENIED
    │        • anything it can't parse ... DENIED (fail-closed)
    ▼
 audit.jsonl  (every decision logged)
```

The LLM never gets to place an order the guard hasn't approved. The guard is
plain Python — it does not depend on the model "being careful."

## Prerequisites

1. **Python 3.10+**
2. **Node.js 18+** — the Claude Agent SDK drives the Claude Code runtime, which
   is a Node process.
3. **Anthropic credentials** — either `ANTHROPIC_API_KEY` in your environment, or
   an `ant auth login` / Claude Code login profile the SDK can pick up.
4. **A Robinhood Agentic Account + OAuth access token.** The SDK does *not* run
   an interactive OAuth flow. You complete Robinhood's authorization yourself and
   provide the resulting bearer token. See "Getting a Robinhood token" below.

## Setup

```bash
cd robinhood-agent
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# edit .env and set ROBINHOOD_ACCESS_TOKEN (and ANTHROPIC_API_KEY if not already set)

# review and edit the strategy + risk limits
$EDITOR config.yaml
```

### Getting a Robinhood token

Follow Robinhood's Agentic Trading setup to authorize an agent and obtain an
OAuth access token for `https://agent.robinhood.com/mcp/trading`. Put it in
`.env` as `ROBINHOOD_ACCESS_TOKEN`. **Never commit this token** — `.env` is
gitignored. Tokens expire; refresh yours per Robinhood's docs when the agent
starts reporting auth failures (the MCP server will show `needs-auth`).

## Running

```bash
# Dry run, once (default). The agent reviews the market and PROPOSES trades;
# the guard blocks all real orders. This is your "paper" mode — start here.
python run.py

# Dry run on a loop, every 15 minutes
python run.py --interval 900

# LIVE — orders that pass the risk limits in config.yaml will actually execute.
# You must pass BOTH the flag and set dry_run: false is NOT required — the flag
# is the explicit opt-in. Read config.yaml risk limits first.
python run.py --live
python run.py --live --interval 3600
```

`--live` is the only way to place real orders. Without it, the guard denies every
order regardless of `config.yaml`. This is deliberate: going live is an explicit,
per-invocation decision, not a config file you might forget you edited.

## The risk guard (`config.yaml` → `risk:`)

Every limit below is enforced in `risk.py`, in code, before an order is allowed:

| Limit | Meaning |
|---|---|
| `symbol_allowlist` | Only these symbols may be traded. **Empty list = deny all orders** (fail-closed). Set it explicitly. |
| `max_order_notional_usd` | Max dollar size of a single order. Orders the guard can't price are denied. |
| `max_orders_per_run` | Max orders the agent may place in one run. |
| `max_orders_per_day` | Max orders per calendar day (persisted in `state.json`, UTC). |
| `allow_buy` / `allow_sell` | Enable/disable each side independently. |
| `allow_cancel` | Whether the agent may cancel existing orders. |

**Fail-closed by design:** if the guard sees an order-shaped tool call it cannot
confidently parse and price (unknown fields, missing quantity/notional), it
**denies** it. A denied call is not an error — the model receives the denial
reason and is instructed to report it and stop, not to retry around it.

### How tools are classified

The guard doesn't hardcode Robinhood's tool names (they may change). It matches
substrings from `tool_classification:` in `config.yaml`:

- a tool name matching `order_patterns` → treated as **order placement** (gated)
- a tool name matching `cancel_patterns` → treated as **cancel** (gated)
- anything else on the Robinhood server → treated as **read-only** (allowed)

Any tool **not** from the Robinhood MCP server (built-in Read/Write/Bash, etc.)
is denied — this bot only talks to Robinhood.

Inspect `audit.jsonl` after any run to see exactly what was proposed, allowed,
and denied, with reasons.

## Safety checklist before going live

- [ ] You ran in dry-run and reviewed `audit.jsonl` — the proposed trades look sane.
- [ ] `symbol_allowlist` is a short, explicit list you actually want traded.
- [ ] `max_order_notional_usd` and the per-run/per-day caps are amounts you're
      comfortable losing.
- [ ] You understand you may not be able to stop it mid-order once live.
- [ ] The account holds only capital you can afford to lose.

## Layout

```
robinhood-agent/
├── run.py          # entrypoint + scheduler (--once / --interval / --live)
├── agent.py        # builds the Agent SDK options and runs one cycle
├── risk.py         # RiskGuard: the deterministic can_use_tool gate + audit log
├── config.py       # loads and validates config.yaml
├── config.yaml     # strategy prompt + risk limits (edit this)
├── requirements.txt
├── .env.example
└── .gitignore
```
