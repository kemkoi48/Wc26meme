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

## Also available (not from a user-provided link)

- **Robinhood connector** (`get_earnings_calendar`, `get_earnings_results`,
  `get_financials`) — earnings dates/results and fundamentals for specific
  symbols. Already wired into research; see README.
- **General WebSearch** — works for "what's happening with X today" style
  queries; quality varies by query specificity.
