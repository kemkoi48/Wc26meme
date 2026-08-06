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

## Also available (not from a user-provided link)

- **Robinhood connector** (`get_earnings_calendar`, `get_earnings_results`,
  `get_financials`) — earnings dates/results and fundamentals for specific
  symbols. Already wired into research; see README.
- **General WebSearch** — works for "what's happening with X today" style
  queries; quality varies by query specificity.
