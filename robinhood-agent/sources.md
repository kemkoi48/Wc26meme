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
**Status: Blocked.**

Direct WebFetch fails outright ("unable to fetch from www.reuters.com") —
this looks like a bot-block on Reuters' side, not a paywall message. High
reputational quality as a source, but not usable as a direct-check tool right
now. Reuters-sourced content sometimes still surfaces through a general web
search (which indexes the page rather than fetching it live), so it's not
fully unreachable — just not a page I can browse directly.

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

## Also available (not from a user-provided link)

- **Robinhood connector** (`get_earnings_calendar`, `get_earnings_results`,
  `get_financials`) — earnings dates/results and fundamentals for specific
  symbols. Already wired into research; see README.
- **General WebSearch** — works for "what's happening with X today" style
  queries; quality varies by query specificity.
