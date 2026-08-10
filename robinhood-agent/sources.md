# Research sources

A durable log of news/data sources evaluated for market research, so a future
session doesn't have to re-test them from scratch. Each entry: what it is,
whether it's directly fetchable, and how to actually use it.

Format: `## <name>` — `status`, then notes. Status is one of:
- **Live, fetchable** — WebFetch pulls real current content directly.
- **Educational, not a feed** — useful for framework/method, no live data.
- **Blocked** — direct fetch fails; may still surface via web search.

---

## Investing.com Economic Calendar
`https://www.investing.com/economic-calendar/`
**Status: Live, fetchable.**

Tested 2026-08-06 — returned real, current-dated events with forecast/previous
values and impact level (high/medium/low), e.g. that day's US Initial/
Continuing Jobless Claims (high impact), German Factory Orders, Eurozone
Retail Sales, etc. This is the primary macro-check source: ask for "today's
high-impact events" or "this week's calendar" before acting on a signal.

## Reuters Markets
`https://www.reuters.com/markets/`
**Status: Blocked (confirmed).**

Direct WebFetch fails outright ("unable to fetch from reuters.com") — tested
2026-08-06 across four variants (`www.reuters.com/markets/`,
`reuters.com/markets/` without www, `www.reuters.com/markets/us/`, and a
retry of the original URL): all four failed identically. This is a
domain-wide block on Reuters' side, not a one-off glitch or a paywall
message. High reputational quality as a source, but not usable as a direct-
check tool. Don't keep retrying variants — this is settled.

Workaround: Reuters-sourced content sometimes still surfaces through a
general web search (which indexes the page rather than fetching it live). If
you have a specific Reuters article you want analyzed, paste its text
directly and I can work with that.

## Investing.com Academy — "Stay Updated on the Stock Market"
`https://www.investing.com/academy/trading/stay-updated-on-the-stock-market/`
**Status: Educational, not a feed.**

Recommends a "Signal vs. Noise" framework: earnings reports and scheduled
economic data = signal; sensational headlines and minor price swings = noise.
Recommends a three-layer routine (macro calendar check, portfolio alerts,
curated analysis) and names WSJ, Financial Times, Reuters, and Investing.com
itself as sources. **Caveat: WSJ and FT are paywalled** — full article text
generally isn't fetchable unless pasted in directly.

## stockmarketterminology.com — "Stock Market News: What It Means"
`https://stockmarketterminology.com/stock-market-news-what-it-means/`
**Status: Educational, not a feed.**

Defines what counts as market-moving news (earnings, Fed actions,
geopolitical events, mergers) and stresses that markets are forward-looking
— news often confirms an already-priced-in expectation rather than surprising
the market. Useful lens for weighing a headline's actual price impact, not a
source of current headlines itself.

---

## Stocktwits (connector)
**Status: Live, connected, verified.**

Tested 2026-08-06: `whoami` confirms an authenticated session (real user
account); `get_trending_symbols` returns real live top-movers with price, %
change, intraday sparkline, watcher count, and extended-hours pricing (e.g.
SOUN, SNDK, IONQ, RDW, DKNG at test time). `get_symbol_pulse` and
`get_sentiment` return real aggregate sentiment for a symbol (bull/bear %, a
0-100 score, a label like "EXTREMELY_BULLISH") plus message-volume metrics
across multiple timeframes (now/15m/1D/1W/1M/3M/6M/1Y/ALL). Tested against
AAPL: price $313.07, sentiment 82/100 "EXTREMELY_BULLISH", 987,224 watchers.

Other available tools (not yet tested): `get_symbol_messages`,
`get_message_volume`(+`_history`), `get_sentiment_history`,
`get_following_feed`, `get_watchlist_feed`, `get_user_messages`,
`get_symbol`.

**Caveat — read before surfacing raw posts to a user:** the "top posts" in
`get_symbol_pulse` is unmoderated, real user-generated content. In testing,
AAPL's feed included off-topic, low-quality, and offensive material mixed in
with genuine stock chatter. **The aggregate metrics (sentiment score, message
volume, watcher count) are the reliable signal — don't relay raw post text
without screening it first.**

## Robinhood connector — no dedicated news tool
Confirmed via tool search: none of the Robinhood tools is a `get_news` /
article-feed endpoint. Closest equivalents are `get_earnings_calendar` /
`get_earnings_results` / `get_financials` / `get_equity_fundamentals` —
fundamentals and earnings data, not news articles. For actual news-adjacent
signal, use Stocktwits sentiment/chatter (above) or a general web search.

## Yahoo Finance — not actually connected
User mentioned adding a Yahoo Finance connector alongside Stocktwits, but
only Stocktwits tools appeared in the session (checked via tool search — no
match). If a Yahoo Finance connector gets added later, re-check and log it
here; don't assume it's present just because it was mentioned.

## Stocklake (connector)
**Status: Live, connected, verified — free tier.**

Tested 2026-08-06. 17 tools total; account is on the **free tier** (200
calls/day, 8 non-AI tools). Two tools require **Pro** ($20/mo, 7-day trial,
5000 calls/day) and returned `pro_required` errors when tested:
`get_news_feed` (market-wide AI-flagged news briefing) and `get_signals`
(AI-screened trade signals with conviction/rationale). Both gave a useful
`preview` of a few symbols even on free tier.

**Confirmed working on free tier:**
- `get_market_pulse` — VIX, Fear & Greed, market breadth (RSI distribution),
  SPY/QQQ/IWM + RSI, TLT/GLD. One call, no AI cost. Real live data verified.
- `get_market_movers` — gainers/losers/most-active with price, volume, RSI,
  ATR%, market cap. Real live data verified.
- `get_stock_news` — per-symbol news (docs say "1 article" on free tier;
  observed 5 articles per call in testing — better than documented, but
  don't rely on the discrepancy holding).
- `get_screener` — most filters (RSI/SMA/MACD/performance/volume/market cap/
  analyst rating) work on free tier; `min_flag_score` and the `high_conviction`
  preset are Pro-only (silently ignored on free tier per its own docs).
- `get_stock` — price/fundamentals/raw indicators on free tier; the four
  *interpreted* blocks (rating, signals, stance_signals, ai overview) are Pro.

**Not yet tested:** `get_earnings_calendar`, `get_earnings_intelligence`,
`get_indicator_history`, `get_insider_activity`, `get_market_assessment`,
`get_sector_intelligence`, `get_stock_history`, `get_stock_research`,
`get_stocks`, `get_watchlist`.

**Real finding worth remembering:** cross-referencing Stocklake's mover list
against Stocktwits trending caught a data-quality issue. Two names on
Stocklake's gainers list (CLBK +126.6%, VSCO +69.6%) had no same-day news
that explained a move that size, AND neither appeared on Stocktwits
trending at all. A third name, IOVA (+38.99% on Stocklake, +38.36% on
Stocktwits independently), had same-day news (8-K filing + a same-morning
article) and showed up on both platforms — that agreement is what makes it
trustworthy. **Lesson: an extreme single-source % move with no matching
same-day news and no cross-platform attention is a reason for suspicion, not
excitement — verify large movers against a second source before treating
them as real.**

## Robinhood native scanner (`get_scans` / `run_scan`) — covers names Stocklake misses
**Status: Live, verified — and catches a real gap.**

Tested 2026-08-06: the account has saved scans including "Daily gainers"
(294 matches, all Robinhood-tradable stocks, sorted % change desc).
`run_scan` on it surfaced **WYHG at +540%** (a $10.2M market-cap ADS) —
a move that **never appeared in Stocklake's `get_market_movers` gainers
list** (top Stocklake gainer at the same moment was CLBK at 126.6%, not
close). WYHG had zero news (`get_stock_news` returned empty) and classic
retail-hype-driven chatter with no informational catalyst — textbook thin/
low-float momentum spike, not a real opportunity, but the point stands
regardless of that stock's quality: **Stocklake's ~3,300-name tracked
universe does not cover everything Robinhood's own scanner does.**

**Process lesson: check both `get_market_movers` (Stocklake) AND
`run_scan` on Robinhood's "Daily gainers" (or equivalent) when looking for
"what's moving today" — they cover different universes and can each miss
names the other catches.** `run_scan` results can be large (200+ rows) and
overflow the tool-result limit; save to file and extract with
`python3`/`jq` rather than reading inline.

## Robinhood consumer app — "Short interest" / "Trading Trends" panels
**Status: Blocked — app-only, no MCP tool exposes it.**

Confirmed 2026-08-07: the Robinhood mobile app's stock-detail screen has a
"Short interest" chart (short interest in shares + short float %, ~2 months
trailing) and a "Trading Trends" chart (net buy/sell % by Robinhood retail /
Hedge funds / Insiders, weekly). Checked the full `Robinhood` MCP tool list
(`get_equity_fundamentals`, `get_financials`, `get_equity_technical_indicators`,
etc.) — none of them return short interest, short float, or ownership-flow
data. This is because the connected server is the narrower **Agentic Trading
API** (`agent.robinhood.com/mcp/trading`), not the full consumer-app backend;
`get_equity_fundamentals` gives float/shares outstanding but stops there.

**Workaround: read the values directly off a user-provided screenshot of the
app screen** — no live fetch is possible, but a pasted image can be
transcribed manually. Example (TSLA, screenshot dated through Aug 6 2026):
short interest ran ~75–79M shares (2.8–3.0% of float) from early June through
mid/late July, then dropped sharply ~Jul 25–28 to ~67–70M shares (2.4–2.6%
float) and held there — a short-covering signal, not something any connected
tool surfaced independently. Robinhood retail net-buy/sell trend for the same
symbol was net-positive overall Jul 8–Aug 3 with two sharp sell days.

If a dedicated short-interest data connector (e.g. Ortex, S3 Partners, or a
FINRA short-interest feed) gets added later, re-check and replace this entry.

## Warrior Trading — "Small Account Challenge" momentum strategy (YouTube + PDFs)
**Status: Educational, not a feed. Incompatible with this repo's cash account for live use.**

Reviewed 2026-08-08: a Ross Cameron / Warrior Trading YouTube class plus three
companion PDFs (strategy guide, sample trading-plan worksheet, blank trade-log
worksheet). This is promotional content for a paid course (PDF upsells, "check
out my class" links) — the $600→$20M / $2K→$65K-in-30-days figures are the
marketing hook; treat as a strategy description, not a performance claim.

**The strategy — 5 steps:**
1. **Stock selection** (scanner-driven): relative volume ≥5x (ideally ≥20x)
   50-day average, high total volume, gapping/up ≥10% intraday, price in a
   narrow band (video: $2–20; the trading-plan worksheet narrows this to
   **$5–10** as the small-account "sweet spot"), float **<20M shares in a hot
   market / <10M in a cold market** (lower = better). News preferred, not
   required if other criteria are strong.
2. **Entry — "first pullback" pattern**: buy the first candle to make a new
   high after a pullback that (a) retraces ≤50% of the prior move, (b) shows
   heavier volume on green than red candles, (c) holds above VWAP, (d) holds
   above the 9 EMA. Stop-loss = low of the pullback.
3. **Level 2 / tape** for entry timing and confirmation around psychological
   price levels (half-dollar/whole-dollar).
4. **Exit on indicators, not fixed targets**: a large resting sell wall, a
   suspected iceberg/hidden seller, a burst of red tape, a topping-tail /
   "jackknife rejection" candle, MACD crossing its signal line, or buying
   visibly slowing.
5. **Journal every trade** and mine the log for leaks (e.g. time-of-day
   win-rate) — the log template tracks P/L, accuracy, float, relative volume,
   news, hold time, and candlestick pattern per trade.

**Concrete risk rules from the worksheets** (not stated in the video):
7:00–11:00am ET trading window; risk ~5% of account per trade, profit target
~10% (2:1 reward:risk); daily max loss 10% of account; **3 consecutive losers
= stop for the day**; accuracy/P&L progression benchmarks from 40–50%
accuracy / 0.5–1.0 P/L ratio (novice) up to 70%+ / 1.0+ P/L ratio sustained
over 5+ weeks (pro).

**Why this doesn't map onto this repo:**
- It requires multiple same-day round trips (buy and sell the same low-float
  stock within minutes) on a **cash account** — this causes good-faith
  settlement violations regardless of the 2024 T+1 settlement change (T+1
  speeds up when capital becomes available again, it does not permit same-day
  round trips). Same restriction already documented for Pattern Scalp in the
  README — this strategy has the identical conflict, more so (it's designed
  around several round trips per session, not one).
- Exit logic depends on reading Level 2 order flow and tape **in real time,
  continuously** (spotting an iceberg seller, a burst of red tape). The
  Robinhood connector's `get_equity_price_book` returns a real Level 2
  snapshot, but only on-demand — a polling/interval-based bot cannot watch
  continuous tick-by-tick order flow the way this strategy requires.
- The target stock profile (float <20M, extreme relative volume, sometimes no
  news) is exactly the profile already flagged as suspicious in the WYHG
  entry above (extreme single-source move, no news, no cross-platform
  confirmation = reason for caution, not excitement in that entry). This
  strategy treats that same profile as the *goal* — the two takeaways only
  don't contradict each other because Warrior Trading's edge depends on
  discretionary skill/speed to tell a real squeeze from a pump, which isn't
  something this bot's tools or architecture can replicate safely.

## Warrior Trading — warriortrading.com/momentum-day-trading-strategy
`https://www.warriortrading.com/momentum-day-trading-strategy/`
**Status: Blocked (content truncated).**

Tested 2026-08-10, twice, with different extraction prompts. WebFetch returns
only the page title ("Momentum Day Trading Strategies for Beginners") followed
by "[Content truncated due to length...]" — no article body reaches the
extraction step either time. Unlike the Reuters block (a hard fetch failure),
this looks like the page's real content sitting past whatever nav/ad/header
markup consumes the fetch's content window. Don't treat this as equivalent to
the YouTube-class Warrior Trading entry above (which *did* return full
content) — this specific URL has not been read. If asked about this page's
contents specifically, say so rather than reusing the unrelated YouTube-class
summary.

Workaround untried: pasting the article text directly, or a search-indexed
excerpt via WebSearch, the same fallback documented for Reuters above.

## Also available (not from a user-provided link)

- **Robinhood connector** (`get_earnings_calendar`, `get_earnings_results`,
  `get_financials`) — earnings dates/results and fundamentals for specific
  symbols. Already wired into research; see README.
- **General WebSearch** — works for "what's happening with X today" style
  queries; quality varies by query specificity.
