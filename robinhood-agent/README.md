# robinhood-agent

> **New to Python / the command line?** Read **[QUICKSTART.md](QUICKSTART.md)**
> instead — it walks through everything with copy-paste commands
> (`bash setup.sh`, then `bash start.sh`). This README is the full reference.

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
# edit .env and set ROBINHOOD_ACCESS_TOKEN, ROBINHOOD_ACCOUNT_NUMBER (your
# agentic account), and ANTHROPIC_API_KEY if not already set

# review and edit the strategy + risk limits. Two equivalent formats ship:
#   config.yaml  — commented, the documented default
#   config.json  — right-sized for a small (~$28) balance; pass --config config.json
$EDITOR config.yaml
```

The config loader accepts YAML or JSON (by file extension). `config.json` is a
ready-to-run JSON profile sized for a small cash balance (per-order cap $5, one
order per run). Run it with `python run.py --config config.json`.

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
| account pinning | If `ROBINHOOD_ACCOUNT_NUMBER` is set, every order/cancel must target that exact account or it is denied. Orders with no account are denied (fail-closed). Only an account with `agentic_allowed=true` can actually be traded. |

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

## Backtesting the rule (`backtest.py`)

The live agent is an LLM reasoning over Robinhood's tools — it can't be replayed
deterministically. But the **moving-average trend rule** the strategy is based on
can be validated offline before you trust it live:

```bash
python backtest.py --demo                 # synthetic data, zero setup
python backtest.py --csv AAPL.csv         # your own date,close history
python backtest.py --csv AAPL.csv --short 20 --long 50 --fee-bps 1
```

It simulates long/flat, one symbol, no leverage (matching the cautious live
posture) and reports total vs buy-and-hold return, annualized return, max
drawdown, trade count, win rate, and Sharpe. Use it to pick sane symbols and
SMA windows — then reflect that choice in `config.yaml`'s `strategy:` and
`symbol_allowlist`. Pure standard library; CSV is a header row plus `date,close`.

Past performance doesn't predict future results, and a good backtest is not a
guarantee — treat it as a filter for obviously-bad ideas, not a green light.

## Pattern Scalp strategy (opening-range reversal)

`config.pattern-scalp.json` encodes the "Pattern Scalp" opening-range reversal:
after the first 15-minute candle, if its range exceeds 20% of the daily ATR (a
"manipulation" candle), fade the move back toward the opening range on a
5-minute reversal trigger. `backtest_pattern_scalp.py` tests the rule on
intraday data.

```bash
python backtest_pattern_scalp.py --demo                 # synthetic intraday
python backtest_pattern_scalp.py --csv SPY_5min.csv     # your own 5-min bars
```

CSV format: `timestamp,open,high,low,close` with ISO timestamps, regular-session
5-minute bars across many days.

**Read this before using it live — it is shipped as research / dry-run:**
- It is a **same-day day-trade**. The Agentic account is a **cash account**,
  where repeated same-day round-trips cause good-faith settlement violations and
  can get the account restricted. Don't run this `--live` on a cash account.
- It is **long-only** here: the strategy's short setups (upside manipulation) are
  skipped because you can't short in a cash account.
- The backtester's 5-minute entry ("John Wick" / engulfing) is **approximated**
  by an opening-range-low reclaim — indicative, not a candle-exact reproduction.
- A profitable backtest is a reason to test further, not to trade real money.

## Safety checklist before going live

- [ ] You ran in dry-run and reviewed `audit.jsonl` — the proposed trades look sane.
- [ ] `symbol_allowlist` is a short, explicit list you actually want traded.
- [ ] `max_order_notional_usd` and the per-run/per-day caps are amounts you're
      comfortable losing.
- [ ] You understand you may not be able to stop it mid-order once live.
- [ ] The account holds only capital you can afford to lose.

## Deploying (Mode B — unattended)

The bot is a plain Python process; something must keep it running. Two supported
shapes, both shipped in `deploy/`:

- **systemd** (`deploy/robinhood-agent.service`) — for the daily trend strategy
  as an always-on `--interval` loop. Copy to `/etc/systemd/system/`, edit paths
  and user, `systemctl enable --now robinhood-agent`. Ships in dry-run;
  add `--live` to `ExecStart` only after reviewing `audit.jsonl`.
- **cron** (`deploy/crontab.example`) — one-shot cycles on a market-hours
  schedule. This is the right shape for the Pattern Scalp (fires every 5 min
  during the opening window only). Mind the UTC/DST notes in the file.

Host checklist: Python 3.10+, Node 18+ (the Agent SDK drives a Node runtime),
the repo at a stable path (e.g. `/opt/robinhood-agent`) with a venv, and `.env`
populated (`ROBINHOOD_ACCESS_TOKEN`, `ROBINHOOD_ACCOUNT_NUMBER`,
`ANTHROPIC_API_KEY`). Tokens expire — when runs start failing with `needs-auth`
in the logs, re-authorize with Robinhood and update `.env`.

Operate it like a deployment, not a fire-and-forget script: check `audit.jsonl`
and the run logs daily at first, and keep `--live` off until the dry-run record
looks right for several sessions.

## Layout

```
robinhood-agent/
├── run.py          # entrypoint + scheduler (--once / --interval / --live)
├── agent.py        # builds the Agent SDK options and runs one cycle
├── risk.py         # RiskGuard: the deterministic can_use_tool gate + audit log
├── config.py       # loads and validates config.yaml OR config.json
├── config.yaml     # strategy prompt + risk limits (commented default)
├── config.json     # equivalent JSON profile, sized for a small balance
├── requirements.txt
├── .env.example
└── .gitignore
```
