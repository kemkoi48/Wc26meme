# Using Stocklake for Trade Screening

Stocklake is available as a connector in this Claude session. No setup needed — authentication is handled at the platform level. This guide explains which tools to use and when.

## Tool Reference

| Tool | Purpose | Cost | Use when |
| --- | --- | --- | --- |
| `get_insider_activity(symbol)` | Recent insider buys/sells/exercises | 1 quota | Verifying no distribution before entry |
| `get_stock_research(symbol)` | Research verdict, tape response, relative strength | 1 quota | Cross-checking headlines (NEVER trade signals alone) |
| `get_signals(symbol)` | Headline + AI conviction score | 1 quota | Finding catalysts (but always verify with research) |
| `get_stock(symbol)` | Fundamentals, insider/institutional flags | 1 quota | Quick check of relative strength vs peers |
| `get_news_feed(symbol)` | Recent news articles | 1 quota | Understanding the catalyst narrative |
| `get_indicator_history(symbol)` | Technical indicators and history | 1 quota | Rarely needed; tape analysis via research is better |

**Quota:** 5000 calls per day, reset at midnight UTC. Last quota burn: ChatGPT screener refreshed every 10 minutes.

## Recommended Workflows

### Pre-market check (every day, ~5 calls)

Before market open, screen your open positions for insider distribution signals:

```
get_insider_activity("AEYE")
get_insider_activity("HHS")
```

Look for **trend: distribution** (insiders selling). If officers are unloading, ask
"what do they know?" Often precedes halts or reversals in small caps.

### Deep dive (weekly, ~15 calls)

Once per week, verify research verdicts on candidates:

```
get_stock_research("AEYE")
get_stock_research("NEWCANDIDATE")
```

Compare verdict against your thesis:
- **BEARISH:** Tape rejecting the catalyst? Insider flow negative? → Pass
- **BULLISH:** Tape agreeing? Insiders buying? → Worth considering
- **NEUTRAL:** No edge. Wait for clarity.

### Emergency check (as needed, ~3 calls)

If a position looks about to reverse or you suspect a halt:

```
get_stock_research("AEYE")  # Check tape response
get_insider_activity("AEYE")  # Check if officers are selling
```

Act immediately if you see:
- Research BEARISH + insider distribution → Exit position, verify with rule 7 (close by bell)
- Insider distribution spike → This is what stops don't catch; rule 1 is your only defense

## Interpreting Results

### Insider Activity Trends

- **accumulation:** Insiders are buying (bullish)
- **distribution:** Insiders are selling (bearish, especially on micro-caps)
- **neutral:** Mixed or ambiguous

**Example:** AEYE shows 3 buys by officers this week vs 0 sells = accumulation. SMWB
shows CFO selling $50k this week = distribution. One week before SMWB halted, insiders
were selling. Correlation, not causation, but a useful early warning.

### Research Verdicts

- **BULLISH:** Tape, insider flow, and sentiment align positively. Catalyst worked.
- **BEARISH:** Insiders selling, tape rejecting headlines, or negative sentiment. The market disagrees.
- **NEUTRAL:** No clear signal. Wait for clarity.

**Real example (2026-08-13 MLTX):**
- `get_signals` said LONG: "Sonelokimab met primary endpoint in Phase 3"
- `get_stock_research` said BEARISH: "Positive Ph3 data can't stop the bleeding — insiders sold $6.1M, tape down 5% on headline, -72.5% from 52-week high"
- Market fell 5% on the headline. Research was right; the headline was a trap.

**Rule:** Never trade off signals alone. Always cross-check with research first.

## Coverage and Gaps

**Large caps (AAPL, MSFT, QQQ, SPY):**
- Full data available
- All fields populated
- Research verdicts reliable

**Small caps (SMWB, RSKD, AEYE, HHS):**
- Often missing
- If you see `symbol_not_found`, that ticker is outside Stocklake's ~3,501-symbol universe
- Fall back to Stocktwits + Robinhood fundamentals for catalyst verification
- Insider activity for small caps is harder to verify at the platform level

**Workaround:** Use Robinhood's built-in insider + institutional signal flags as a secondary check. They cover the micro-caps Stocklake misses.

## When NOT to Call Stocklake

- **Auto-refresh.** Never set up a loop calling Stocklake every 10 minutes (this is what burned ChatGPT's quota). Call deliberately: pre-market (once), weekly deep-dive (once), emergency (as needed).
- **On news headlines alone.** Headlines are the most unreliable signal. A stock can fall 5% on positive news if the tape rejects it.
- **For technicals.** Stocklake's indicator history exists but doesn't add value here. Tape analysis via research verdict is faster.
- **To predict halts perfectly.** Insider distribution is a warning sign, not a prediction. Rule 1 (name the news) + rule 3 (place stop within 60s) are your defenses.

## Quota Management

**Daily limit:** 5000 calls. Current usage:
- Pre-market check (2 symbols): 2 calls
- Weekly deep-dive (5 symbols × 3 tools): 15 calls
- Emergency checks: varies

**Safe monthly burn:** ~100–150 calls (well under daily limit). The danger is **automation**: ChatGPT's 10-minute refresh would burn 144 calls per day just to refresh 5 symbols.

**When quota is exhausted:** You'll see an error. Wait until tomorrow UTC for reset. Do not ask for an upgrade mid-month.

## Integration with S8 (Verified Catalyst Momentum)

Before entry:
1. Name the news (Rule 1)
2. Check insider activity: any distribution? → risk/reward shifts
3. Check research verdict: does tape agree? → if BEARISH despite bullish headlines, likely a trap
4. Log findings in `sources.md`

Example log entry:
```
2026-08-16: SMWB — Insider distribution 3 days before halt. get_insider_activity
showed CFO selling $50k; research was BEARISH (tape rejecting volume spike).
Verdict: Insider distribution + bearish tape = skip. Rule 1 (name the news)
would have caught halt risk, but Stocklake gave earlier warning.
```

After 15–20 trades with this check in place, you'll see if insider distribution is
predictive or noise. Log everything.
