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
**Status: Live via the AMP URL. Canonical URL is blocked (truncates).**

**Use `https://www.warriortrading.com/amp/momentum-day-trading-strategy/`.**
The canonical URL was tested twice on 2026-08-10 with different extraction
prompts and both times returned only the page title followed by "[Content
truncated due to length...]" — the body sits past nav/ad markup that eats the
fetch window. The AMP copy strips that markup and returned the **complete,
untruncated article** on the first try. Generalize this: for any content site
that truncates, try `/amp/` before declaring it blocked.

**Correction — an earlier WebSearch summary of this page got several numbers
wrong.** Before the AMP read, a search-engine summary was logged claiming
$1–10 price / <10M float / ≥5% change / 5x rel. volume. The actual article
says none of those things except approximately the float ideal. Lesson: a
search summary of a page is *not* a read of the page — label it as such and
replace it once the real text is obtained. Do not cite those figures.

**What the article actually says (read directly, 2026-08-10):**

*Selection:* float **under 100M shares**, with **under 20M ideal**; relative
volume **at least 2x** average; stocks moving **20–30%+** on the day; on the
daily chart, price above its moving averages with **no nearby resistance**; a
fundamental catalyst — PR, earnings, FDA news, activist investor, breaking
news.

*Entry patterns (named):* **Bull Flag** — buy the first candle to make a new
high after the breakout — and **Flat Top Breakout**, where resistance forms
across several candles before an explosive move.

*Exits:* sell **half** the position at the first profit target; **the first
candle to close red is an exit indicator**; exit into extension bars (spikes
of $200–400+).

*Risk:* **2:1 profit/loss ratio** required. Max stop distance **20 cents** —
if the technical stop is further away, stop out at −20¢ anyway. Position size
falls out of that: `shares = max_risk ÷ stop_distance` (their example: $500
risk ÷ $0.20 = 2,500 shares).

**The finding that matters most here: a hard time window of 9:30–11:30am ET,
with the first hour called optimal, and 5-minute charts only after 11:30am.**

This reframes a result from live testing the same day. Two scanner runs at
**12:43pm and 1:07pm ET** — both more than an hour past this strategy's own
cutoff — found that every "building" name from the earlier run had flipped to
fading 24 minutes later, none breaking to a new high (WFF 20.9x→0.16x, VERU
3.4x→0.26x, GLBS 1.9x→0.34x, HKIT 2.5x→0.34x). That was recorded as a
weakness of the acceleration signal. Per this article it is at least partly
the expected behavior of the *market* in that window, not only a defect in the
metric: the strategy does not claim to work at 1pm. **Any future test of an
intraday momentum signal should run inside 9:30–11:30am ET before its decay is
attributed to the signal itself.**

*Not from this page:* a "switch from Top Gainer to a High of Day Momentum
Scanner as the day progresses" workflow appeared in search results, but the
article text does not mention it — it belongs to Warrior's separate scanner
pages (`/day-trading-scanners/`, `/how-to-use-stock-scanners/`), unread as of
this entry. Worth reading before building a high-of-day strategy on it.

**Where this conflicts with config.json** (which encodes the YouTube-class
numbers — $2–20 price, <20M float, ≥10% change, ≥5x rel. volume): this page is
looser on relative volume (2x vs 5x) and float (<100M vs <20M), and much
tighter on the move size (20–30% vs 10%). It states no price band at all.
These are two different write-ups of the same house strategy and they do not
agree; treat neither as authoritative and keep config.json's numbers unless
there's a reason to change them.

## daytrading.com — Strategies overview
`https://www.daytrading.com/strategies`
**Status: Live, fetchable.**

Tested 2026-08-11 — full page fetched cleanly, no truncation. A survey
article naming six strategies plus a general risk-management section.
Shallower than the Warrior Trading source (a few sentences per strategy, not
a full walkthrough), but two pieces are concretely new and worth carrying
forward.

**The six strategies, briefly:**
1. **Breakout** — close above resistance = long bias, close below support =
   short bias; price target from the average size of recent swings. No
   numeric thresholds given.
2. **Scalping** — sell the instant a trade is profitable; needs a broker that
   explicitly permits it (worth checking on the Robinhood Agentic account
   before ever building toward this).
3. **Momentum** — "there is always at least one stock that moves 20-30% each
   day"; enter on news + high volume, exit on reversal signs or volume
   drying up. This is the same shape as momentum_scanner.py's Strategy 1,
   just without numeric filters — doesn't add anything config.json doesn't
   already have more precisely.
4. **Reversal / mean reversion** — trade pullbacks against the trend;
   flagged in the article itself as needing more experience than the others.
5. **Pivot points** — classic floor-trader formula: `P = (H+L+C)/3`,
   `R1 = 2P-L`, `S1 = 2P-H`, `R2 = P+(R1-S1)`, `S2 = P-(R1-S1)`. Session
   range often runs between P and the first support/resistance. More a
   forex/futures tool per the article; untested against any of this repo's
   equity candidates so far.
6. **Moving average crossover** — three SMAs (20/60/100 period); buy when
   the 20 crosses above the 60, sell on the cross below; the 100-period line
   sets trend bias (price above it = uptrend context, below = downtrend).
   **This is a direct, more specific version of the trend rule already coded
   into `run.py`'s strategy prompt** (20-day above 50-day = uptrend) — same
   idea, different period pair and an added third line for regime context.
   Worth testing 20/60/100 against the existing 20/50 pair before assuming
   either is better.

**The two genuinely new things, not present anywhere else in this repo:**

- **Position sizing formula, stated generally (1% risk convention, not
  specific to any one strategy):** `position_size = max_risk ÷ (entry_price
  − stop_price)`, with max_risk itself capped at ~1% of account equity per
  trade (their example: £27,500 account → £275 max risk). This is a
  *relative* (% of equity) sizing rule. config.json's
  `risk.max_order_notional_usd` is a flat dollar cap (currently $5) —
  fundamentally different logic (fixed dollar ceiling vs. stop-distance-based
  sizing that shrinks or grows the share count with volatility). Not
  contradictory, just a different risk model; worth deciding deliberately
  which one this repo wants rather than defaulting to the flat-dollar one by
  omission.
- **Two-tier stop-loss:** a mental stop at the point the entry thesis breaks
  (exit criteria, not a price), plus a hard physical stop at the maximum
  tolerable dollar loss. Nothing in this repo currently encodes an exit rule
  tied to *thesis invalidation* rather than price — every stop discussed so
  far (Warrior Trading's 20¢, the momentum scan's pass/fail) is price- or
  filter-based only.

**Not tested against this session's actual data** (WXM, PLAG, GRI, etc.) —
this was a read of the source, not yet an application of pivot points or the
MA crossover to today's candidates. If asked to re-evaluate today's names
against this framework, that's a separate step.

## Michael Sincere — *Start Day Trading Now* (Adams Media, 2011)
Uploaded as EPUB 2026-08-11 (ISBN 1440511861). ~281K chars, read in full.
**Status: Educational, not a feed. The most directly relevant book-length
source logged so far — and it contradicts this repo's current setup in two
places that matter.**

### ~~THE BLOCKER: Pattern Day Trader rule~~ — OBSOLETE, see correction

The book's PDT chapter (>4 day trades in 5 business days ⇒ $25,000 minimum
equity, 90-day freeze as penalty) **is no longer current law.** Verified by
web search 2026-08-11:

- **2026-04-14** — SEC approved FINRA's amendments to Rule 4210.
- **2026-06-04** — rule took effect. The **$25,000 minimum equity requirement
  and the "pattern day trader" designation itself are both eliminated**; day
  trades are no longer counted.
- Replaced by **proportional margin requirements** — equity must be
  proportional to actual intraday market exposure during the session, rather
  than a flat account-size gate.
- **Brokerages have until 2026-10-20 (18 months) to implement.** So whether
  the new framework is live *at Robinhood specifically* is a separate
  question from whether it is law. Worth confirming before relying on it.

**Two corrections to my own earlier analysis, not just the book's:**

1. Sincere's book is 2011. Its regulatory content is 15 years stale and
   should not be treated as current on *any* rule — check anything
   regulatory against a live source before acting on it. (I initially logged
   the PDT constraint as a live blocker; that was wrong.)
2. More fundamentally: **PDT applied to margin accounts. This is documented
   as a cash account.** So PDT was likely never the operative constraint here
   even before the repeal — I conflated it with the real one.

**The constraint that does still apply, and is unaffected by this change:**
cash-account settlement. Same-day round trips on unsettled funds cause
good-faith violations regardless of PDT — that limit comes from Reg T
settlement mechanics, not Rule 4210, and is already documented in the
Warrior Trading entry above. The 2024 move to T+1 speeds up when capital
frees up; it does not permit same-day round trips.

### The cheap/illiquid question — separate the regulation from the mechanics

The PDT correction above does **not** transfer to the book's penny-stock
advice, because the two are different kinds of claim. PDT was a *rule*, and
rules get repealed. Bid/ask spread and halt risk are *market mechanics* —
they don't have an effective date.

That said, the book's "under $3" line is a 2011 heuristic and shouldn't be
treated as a threshold either. The defensible version is the mechanism, and
this session produced direct evidence for it rather than needing the book:

- **WXM halted 9:44am and PLAG halted ~11:25am on 2026-08-11** — both were
  full scanner passes, both sub-$10, neither had any confirmed news.
- **TISI quoted $21.55 bid / $22.55 ask** — a ~4.5% spread on a $22 stock.
  On a $28 account that spread is a larger cost than most realistic edges.

So the actionable takeaway is not "avoid stocks under $3" — it's **measure
spread and halt exposure directly instead of proxying them with a price
floor.** A max-spread-percent filter does that honestly; `min_price: 2.0`
only does it by accident, and (per the PLAG entry) also silently excluded a
name that ran while it was below the floor.

One open question raised by the new margin framework: it ties requirements
to **intraday exposure** rather than account size, which in principle could
make volatile, wide-spread names *more* expensive to hold than they were
under the flat-$25K regime. Unverified — worth checking against Robinhood's
actual implementation before assuming either direction.

### THE CONFLICT: the book says avoid exactly what our scanner surfaces

> "When looking for stocks to buy, avoid the cheap or illiquid stocks."
> "If you see a wide spread, you're either in the after-hours market or
> you're looking at a **penny stock trading for under $3**. As a day trader,
> you need liquid stocks, which is why you want to **avoid most penny
> stocks**."

config.json's `momentum_scan.min_price` is **$2.00**. Every full pass the
scanner produced on 2026-08-11 sat in or near the band this book tells you
to avoid — PLAG $2.57, GRI $2.13, WXM $8.01 (thin 577K float), and the
near-misses WAFU $1.74 / AIHS $1.79 were rejected *only* for being too
cheap. Two of those (WXM, PLAG) halted the same session.

The book also gives the diagnostic that would have flagged this
independently: **a wide bid/ask spread is the tell for illiquidity.** Live
example from the same session — TISI quoted **$21.55 bid / $22.55 ask, a
$1.00 spread on a $22 stock (~4.5%)**. Nothing in momentum_scanner.py looks
at spread at all; `get_equity_quotes` returns bid/ask and it is currently
ignored. **Cheapest available improvement to the scanner: add a
max-spread-percent filter.** It is a better liquidity proxy than either the
price floor or the volume minimum, and it is one field away.

Sincere's own target profile is different from Warrior Trading's: stocks
that move **2-5% intraday** (he names APC, AIG, TTWO, BCSI as examples) —
*not* the 20-30%+ low-float movers. Both books are "momentum day trading";
they disagree about what to point it at.

### Rules worth adopting regardless of the above

*Risk:* minimum **1:2 risk-reward, 1:3 better** — with the honest caveat
"as a day trader this may not always be realistic." Before entry, **the most
important calculation is what to do if you're wrong** (position size follows
from the stop, not the other way round). Never hold a losing stock overnight
hoping it recovers. **Do not carry a hard stop overnight** — gap-down risk
fills it far below the stop.

*Orders:* limit orders, not market orders — a market order in a fast tape can
fill "10, 15, or 20 points lower than you anticipated." Scale in (buy half,
add the rest only if it works). One pro (Kurisko) uses a conditional order
that won't trigger **until the market has been open at least 10 minutes**,
avoiding the opening auction — relevant given the 9:35am scan runs.
Toni Turner: place the protective stop **immediately on entry**, not later.

*Exits:* "When in doubt, get out" — the moment you first think about selling
is the signal. Trailing stop: after a 2-point gain, move the stop to +1 to
lock profit, then raise in ~$0.50 increments. **Cockroach theory** — one bad
piece of news about a position implies more you can't see yet.

*Indicators (defaults he teaches):* RSI 14-period, >70 overbought / <30
oversold, with 9-period and even 2-period as day-trading variants; explicitly
"guidelines, not fixed rules." MACD = 12/26 EMA difference with a 9-period
signal line; buy on cross above signal or above zero. Bollinger Bands default
(20, 2); band squeeze = low volatility, expansion = high; piercing a band is
"pay attention," *not* an actionable trade by itself. MA crossover: 8-day
above 13-day as a buy signal; on intraday charts use *period* not *day*
(20-period, 50-period). Timeframes: 5/15/30/60-minute intraday; one pro
deliberately uses an **8-minute** chart to "get off the fives" where everyone
else is looking.

*Expectations:* **"No more than 5 percent of people who try make a
consistently profitable living as a day trader."** And the Jim Rogers quote
he closes on — do nothing until there is something to do.

### What this does NOT resolve
The book predates (2011) the current market structure and says nothing about
trading halts, which is the single most consequential thing observed in live
testing on 2026-08-11 (WXM and PLAG both halted; PLAG then reopened +71%).
Its "avoid penny stocks" guidance points away from the names that halt, but
it offers no framework for what to do when one is already in play.

## Robert C. Miner — *High Probability Trading Strategies* (Wiley, 2009)
Google Drive link supplied 2026-08-11. **The Drive `/view` page is a login
wall and WebFetch cannot read it** — but the public direct-download endpoint
works and returns the file:
`curl -L "https://drive.google.com/uc?export=download&id=<FILE_ID>&resourcekey=<RK>"`
290pp, 467K chars, text extracts cleanly (PyMuPDF; note `pypdf` fails in
this container — broken system `cryptography`/`_cffi_backend`).
**Status: Educational, not a feed. The most rigorous of the three trading
sources logged, and it contradicts the other two in specific places.**

### The core method: Dual Time Frame Momentum

The organizing idea is that a setup requires **two timeframes of momentum
agreeing**, and the rules are a 2x2 on the higher timeframe's state. Works
with any oscillator that has overbought/oversold zones (he uses DTosc, shows
the identical table for Stochastic), and for any timeframe pair "from
weekly/daily to 15m/5m":

| Higher TF momentum | Action on smaller TF |
| --- | --- |
| Bull, not OB | **Long** after a smaller-TF bullish reversal, provided that reversal happens *below* the OB zone |
| Bull, **OB** | No new longs. Possible short after a smaller-TF bearish reversal |
| Bear, not OS | **Short** after a smaller-TF bearish reversal, provided it happens *above* the OS zone |
| Bear, **OS** | No new shorts. Possible long after a smaller-TF bullish reversal |

Critical framing he repeats: **these are setup conditions, not execution
signals.** The higher timeframe sets direction; the lower timeframe reversal
is the filter. Execution is a separate step (below).

Also: a higher-timeframe OB reading is *not* a reason to exit an existing
long — only a reason not to open a new one.

### Two entry strategies — both require confirmation, never a target price

> "Never buy or sell at a target price. Always require the market to move in
> the direction of the anticipated trend to execute a trade."

1. **Trailing One-Bar entry (Tr-1BH/L):** buy-stop one tick above the
   trailing one-bar high (mirror for shorts). Trade doesn't execute unless
   the market takes out that bar high — smallest capital exposure of the two.
2. **Swing entry (SE):** buy-stop one tick above the prior swing high. Wider
   stop, therefore larger exposure, but a stronger confirmation.

**"Stops are always placed at the exact price that will void the setup."**
Because entry and stop are both defined by the setup, **capital exposure is
known before the trade is placed** — which is what makes the position-size
math below possible at all.

### Position sizing — concrete, and different from what config.json does

- **3% maximum capital exposure on any one trade; 6% across all open
  trades.** He calls this "the accepted standard, and it is a good one."
- `Maximum Position Size = (Available Capital × 3%) ÷ Capital Exposure per Unit`
- Gann's old 10%-per-trade rule: "way too much" — he says he learned that
  expensively.
- **Circuit breaker: if closed trades draw the account down 10% in under a
  month, stop trading for the rest of the month.** Nothing in this repo has
  a drawdown-triggered halt of any kind.
- Drawdown asymmetry as the justification: a 20% drawdown needs a 25% gain
  to recover; 50% needs 100%.

**How this sits against config.json:** `max_order_notional_usd: 5` on a ~$28
account is ~18% of capital per order — but that is *notional*, not *risk*.
Miner's 3% is risk (entry-to-stop distance), which on a stop a few percent
wide would permit a much larger notional than $5. The two numbers are not
comparable, and the repo currently has no concept of the one Miner cares
about. **Adding stop-distance-based exposure would be a real change, not a
retuning of the existing cap.**

### Where Miner and Sincere directly disagree — do not silently merge them

**Risk/reward ratios.** Sincere: minimum 1:2, "1:3 is even better." Miner
devotes a section to calling the idea "basically a bogus idea":

> "Most professional traders don't pay much attention to a risk/reward
> ratio... it is only a best guess... avoid any trading educators who claim
> they teach you how to only take trades with some minimum risk/reward
> ratio."

His replacement: "Focus on positive and logical trade management and the
risk/reward will take care of itself," and a warning about "paralysis of
analysis" from pre-trade ratio math. Both authors are credible; this is a
genuine disagreement about method, not one of them being wrong on a fact.
**Logged as a conflict; not resolved here.** Note the asymmetry that makes
it decidable in principle: a minimum-ratio rule is testable against a trade
log, and Miner's position is the one that predicts the filter adds nothing.

**Indicator settings.** Sincere gives defaults (RSI 14/70/30, MACD 12-26-9).
Miner explicitly rejects fixed settings: the right lookback varies by market
*and* timeframe *and* changes over time. His selection procedure is concrete
and worth stealing — test a few lookbacks over 2-3 different periods and
pick the one where (1) the indicator reaches OB/OS at most reversals,
(2) reversals land within a bar or two of the actual swing high/low, and
(3) there are no false reversals mid-range. His worked example landed on 13
over 8 (too many whipsaws) and 21 (too laggy, never reached OB/OS).

### Expectations, stated plainly

- **"If you get good at trading, you will have around a 30 to 40% win
  percentage."** Better than 50% over time = "trader elite."
- "The best professional traders rarely have a greater than 50% win record."

This is a materially different claim from the accuracy benchmarks in the
Warrior Trading worksheets logged above (40-50% novice rising to 70%+ pro).
Worth holding both loosely; Miner's is the more conservative and comes with
his position-sizing math attached, which only makes sense if most trades
lose.

### The one thing he says guarantees failure

> "I believe there is one primary reason traders are not successful: They
> lack a trade plan. All consistently successful traders have a written trade
> plan... A trade plan does not guarantee success, but lack of one guarantees
> failure."

Paired with record-keeping: every successful trader he knows has a
trade-record system; "a lack of it does ensure failure." Minimum contents of
a plan per Miner: the conditions that must be met to *consider* a trade,
objective entry strategies, and narrow guidelines for managing the trade
through exit.

**Relevance to this repo:** momentum_scanner.py implements the first third
(conditions to consider) and nothing of the other two. That is a fair
description of the actual gap — the scanner finds candidates; there is no
written entry strategy, no stop rule, no exit rule, and no trade log.

### Not applicable / untested here
Chapters 3-5 (Elliott-pattern recognition, Fibonacci price retracements and
projections, time-cycle projections) are the bulk of the book and are
discretionary chart-reading methods. None of it has been tested against this
session's data, and the connected tools expose no Fibonacci or wave
analysis. Logged as read, not adopted.

## WebSearch — cheap-option / catalyst-mismatch research (2026-08-12)

The account asked specifically about buying cheap (sub-$2, sometimes
sub-$0.10) option contracts ahead of a known catalyst. Researched via
WebSearch rather than a user-provided book; cross-checked several
independent sources rather than trusting one, per the "beware of wrong
learning material" instruction. Findings written into S7 in
`strategies.md`, not duplicated here — this entry is the source list.

- **Expected-move mechanics**: ATM straddle price × 0.85 ≈ market's priced
  expected move to expiry; equivalently `price × IV × sqrt(DTE/365)`.
  [tradealgo.com](https://www.tradealgo.com/trading-guides/options/expected-move-calculator),
  [MenthorQ](https://menthorq.com/guide/from-straddle-price-to-expected-move/),
  [optionspilot.app](https://optionspilot.app/blog/expected-move-calculation-implied-volatility)
- **IV Rank / IV Percentile** as the actual "cheap vs. expensive" metric —
  compares current IV to its own 12-month range, not to a dollar price.
  [Yahoo Finance](https://finance.yahoo.com/news/implied-volatility-rank-percentile-better-133416799.html),
  [projectfinance](https://www.projectfinance.com/iv-rank-percentile/),
  [MenthorQ](https://menthorq.com/guide/iv-rank-vs-percentile/)
- **IV crush around earnings**: IV peaks the day before the event and
  collapses (often 30-40%+) right after, independent of whether the
  directional call was correct.
  [EBC Financial Group](https://www.ebc.com/forex/implied-volatility-before-earnings-are-options-too-cheap),
  [MenthorQ](https://menthorq.com/guide/iv-crush-understanding-the-earnings-driven-volatility-spike-and-how-to-capitalize-on-it/),
  [Schwab](https://www.schwab.com/learn/story/trading-options-around-earnings-announcements)
- **"Lotto ticket" base rate**: far-OTM option buyers lose roughly 91% of
  the time on average — the honest floor under this whole category of
  trade, independent of any individual mismatch read.
  [Banyan Hill](https://banyanhill.com/losing-investors-trading-options-like-lottery-tickets/),
  [greeks.live](https://learn.greeks.live/path/what-is-a-lotto-ticket-trade-in-the-context-of-options-trading/)
- **Options Industry Council** (optionseducation.org) — free, non-commercial
  options education body; confirmed as a credible baseline for IV/earnings
  mechanics rather than relying solely on trading-blog summaries.
  [optionseducation.org](https://www.optionseducation.org/)

**Live verification, not just theory:** pulled ENVX's real option chain the
same session (reports after today's close) and confirmed the pattern by
hand — IV ~280-305% across strikes, ATM straddle pricing a ~15% expected
move, and a 36%-OTM call at $0.04-0.07 that *looks* like the pattern being
asked about but is actually IV correctly pricing in an earnings-sized
move, not a mismatch. See S7 in `strategies.md` for the worked numbers.
This is the standard applied going forward: a claimed mismatch needs a live
chain pull to confirm, not just a price that looks cheap.

## "Smart Money Concepts" (ICT) — Fair Value Gap — tested and rejected (2026-08-15)

**Status: own empirical test, not a fetched source.** The user shared a
social-media chart claiming an "SMT + IDM + FVG + OB = 6RR" setup. FVG (Fair
Value Gap — a 3-candle price gap where candle 3's low sits above candle 1's
high) is the only one of those four concepts with a fully mechanical,
non-subjective definition; OB, IDM, and SMT all require a judgment call
(what counts as an "obvious" liquidity pool, which correlated pair to use)
that can't be made objective without just encoding personal bias into the
test.

**Method:** pulled 1 year of SPY daily bars (2025-08-15 to 2026-08-14, 251
bars), detected every bullish and bearish FVG ≥$0.30 wide programmatically,
and measured (a) whether price retraced back into the gap within 20 trading
days, and (b) given a retest, whether the close 5 trading days later
continued in the gap's direction — compared against the unconditional base
rate for the same 5-day-forward move over the same sample.

**Result:**

| | n tested | Retested within 20d | Continuation after retest | Baseline (unconditional) |
| --- | --- | --- | --- | --- |
| Bullish FVG | 43 | 79.1% | 67.6% | 60.6% (5d-fwd-up rate) |
| Bearish FVG | 28 | 100% | 42.9% | 39.4% (5d-fwd-down rate) |

Two-proportion z-test on the bullish result (67.6%, n=34 retested vs.
60.6%, n=246 baseline): **z ≈ 0.79 — not statistically distinguishable from
noise.** The bearish side is weaker still. SPY spent this year in a strong
uptrend (646 → 776); the "edge" bullish FVG appeared to show was mostly the
trend itself, not the pattern.

**Verdict: no measurable edge found.** OB/IDM/SMT were not tested — see
above for why they can't be made objective with the tools available here.
Logged so a future session doesn't re-spend a data pull re-testing FVG from
scratch. See S8 in `strategies.md` for the standard this sets: a claimed
pattern needs its own backtest against a real baseline, not just a
retrospective chart that worked once.

## S8 float-turnover disqualifier — backtested and demoted (2026-08-16)

**Status: own empirical test, single day, n=11 — not independent.** S8's
first draft used float turnover (day volume ÷ float) above ~20–30× as a
disqualifier, reverse-engineered from about eight names rejected on
2026-08-14. `run_scan` only evaluates live data and cannot be replayed
against a past date, and it was the weekend, so no independent second
sample was available. The test run instead: pull the full 8/14 daily bar
for those same 11 names and check whether turnover magnitude actually
predicted how much of the day's gain got given back — the outcome the
disqualifier is implicitly trying to prevent.

**Result:** no monotonic relationship between turnover and giveback-from-
high (CGTL ran 1,172× and gave back 18.6%; STKH ran 49× and gave back
44.1%). Worse, turnover was **lowest on the name that was observed
actively halting** (AEHL, 2.0×) — halts cap tradeable volume, suppressing
the exact metric meant to flag danger on the exact name that most needed
flagging. Meanwhile LFS, at 2.5× turnover (well under any version of the
threshold), failed just as hard as the high-turnover names — it was caught
by the catalyst check ("$LFS news??" unanswered), not by any number.

**Verdict: the specific threshold is not supported by this data, and the
catalyst check — not turnover — is doing the real work.** Turnover was
demoted in S8 from a co-equal numeric disqualifier to secondary supporting
evidence. Full table and the one real miss (NMAX) are in S8's own
"Float-turnover backtest" subsection in `strategies.md` — logged here so a
future session knows this was tested, not assumed, before trusting either
version of the rule. Single-day, non-independent sample: the next real
step is repeating this same check on independent future trading days, not
re-deriving it from the same eleven names.

## 2026-08-16 — Execution audit: the formal strategies never ran

Prompted by "we are not making profit" and a proposal to allocate across S1,
S2 and S8 in parallel to see which performs best. Before splitting capital,
audited whether the strategies had ever executed. **Two of the three had
not.**

- **S1:** its universe is `daily_allowlist.json`, written by `screener.py`.
  That file does not exist in the repo. The universe is empty by
  construction — the loop can run and will buy nothing. No state files, no
  run logs. `deploy/crontab.example` is an example; nothing is scheduled,
  and this container is ephemeral so cron would not survive the session.
- **S2:** written for a single liquid equity/ETF, with SPY/QQQ/IWM named.
  All trade above $150 against a `max_order_notional_usd` of 150, and stop
  orders are whole-share. It cannot place one share. Also has no scheduler
  and needs invoking every ~5 minutes through the open.
- **Doc drift found in passing:** `strategies.md` asserted that S1 used "the
  flat $5 notional cap" and that `config.pattern-scalp.json` "still carries
  the old $5 cap." Both configs read `max_order_notional_usd: 150`. The
  prose was stale in a way that would have misdirected the sizing fix.
  Corrected in place.

So the premise "the formal strategies underperform the ad hoc screen" was
false. They never competed. Recorded in `CLAUDE.md` as a standing check:
distinguish "it doesn't work" from "it never ran" before diagnosing edge.

## 2026-08-16 — Trade log built and seeded from broker records

`trades.csv` + `tradelog.py`. Seeded from `get_pnl_trade_history`,
`get_equity_orders` (filled **and cancelled** — the cancelled stops are what
recover each trade's *initial* stop price, without which R is not
computable). Seven trades: five closed, two open.

Results in R rather than dollars, because this account funds strategies
unequally and dollar totals cannot rank them.

- **Expectancy +0.28R** per closed trade, n=4 with recorded stops. Positive:
  the process is not broken.
- **No trade reached +1.00R** (best LNSR +0.71R, worst AIRO −0.29R). Every
  winner was closed for less than the risk taken to earn it. Largest
  correctable leak identified so far, and it is on the exit side, not entry
  selection.
- **Stop latency median 16s** across five trades — genuinely good execution
  discipline — **except HHS at 675s (11m15s)**, the single S8 trade. The one
  strategy-generated entry is the one that sat unprotected, independently
  confirming the defect flagged in S8's section.
- Also surfaced: HHS's protective stop is **GFD**, so it expires at every
  close and must be re-placed nightly; AEYE's is **GTC** and does not. One
  missed evening on the GFD leaves the position naked overnight.

Statistical honesty recorded alongside the numbers: at ~5 closes/month,
splitting across three strategies is ~1.7 trades each per month, and
ranking edge needs n≈20–30 per arm. The log will not settle S1 vs S2 vs S8
this quarter. What it settles within 1–3 trades is mechanical — fires/does
not fire, order accepted/rejected, stop attached/missing — which is exactly
what the audit above needed and what the next fixes should target.

## 2026-08-16 — S2 backtested on real bars and rejected

Follow-on from the execution audit. The plan was to unblock S2 by finding a
sub-$100 underlying it could actually afford. Backtested it first, on the
principle that the repo tests before it commits — and the result reversed
the plan entirely.

Setup: `backtest_pattern_scalp.py` against real Robinhood 5-minute bars,
2026-06-15 → 2026-08-14 (29 trading days with a valid ATR), 12 underlyings
(SPY, QQQ, IWM, TLT, EEM, ARKK, KRE, SOXL, TQQQ, XLF, SLV, GDX). Zero
interpolated bars — checked explicitly, per the WOLF precedent.

**Result at default settings: 74 trades, 27% win rate, −20.84R, avg
−0.28R.** Exits 20 target / 51 stop / 3 time. Only 4 of 12 underlyings
positive, and SLV's +10.24R rests on n=3 — excluding it, the other 71
trades total −31.08R. QQQ and TQQQ were each 0-for-8.

Two things made this decisive rather than merely discouraging:

1. **It fails on SPY/QQQ/IWM**, the instruments it was written for. So the
   sub-$100-underlying hunt was the wrong fix aimed at the wrong problem —
   a cheaper ticker was never going to rescue it.
2. **The premise is inverted.** A 5×4 sweep (atr_frac × entry window,
   pooled across all 12) returned **0 of 20 parameter sets positive**, best
   −0.25R. More telling than the sign: raising `atr_frac` from 0.20 to 0.40
   degrades average R from −0.25 to −1.00 *monotonically*. The strategy's
   thesis is that a larger opening range is a bigger liquidity grab and thus
   a better reversal; the data says larger ranges reverse worse. The filter
   meant to select the best setups selects the worst. Tuning cannot repair a
   backwards premise.

Stated limits: the entry is a reclaim approximation rather than an exact
hammer/bullish-engulfing match, it is long-only (a real account
constraint), and 29 days is a single regime with per-symbol n of 3–10. This
does not prove opening-range reversal never works. It does establish that
this specification loses at every setting tested.

S2 moved from "VIABLE — top priority" to **do not fund**. Worth recording
that S2 held top-priority status for four days on the strength of having
the most complete written plan in the repo — entry, stop, target and time
stop all specified. Completeness of specification turned out to be
uncorrelated with profitability, and the blocker that stopped it trading
(a $150 cap against $600 shares) was protective, not merely inconvenient.

## 2026-08-16 — Exit analysis: 21% capture, and breakeven stops make it worse

The trade log showed +0.28R expectancy with no trade ever reaching +1.00R,
and this file had already called that "winners cut short." That phrasing was
an assumption, not a measurement — a sub-1R average has two possible causes
with opposite fixes (exits too early, or stops too wide for the move that
existed). Measured it on real 5-minute bars for the four closed trades with
recorded initial stops.

**It is exits, not stops.** Average MFE available +1.32R against +0.28R
captured — **21% capture efficiency**. Three of four trades offered ≥1.0R.
SMWB was sold 09:34 on 08/13 and peaked at 15:15 the same day (+1.20R
available, +0.21R taken). RSKD offered +2.21R and returned +0.50R.

Rule simulation with an explicit time stop (so nothing gains from holding
forever), stop winning within-bar ties: a fixed target anywhere in the
**1.0–1.5R band roughly doubles expectancy** — +0.68R at 1.0R and +0.74R at
1.25R with a same-session stop, +0.77R at 1.5R with a next-session stop,
against +0.28R actual. The optimum moves with the horizon, which is what
n=4 noise looks like, so the band is the finding and the peak is not.

Two counter-findings that matter more than the headline:

- **Breakeven/trailing stops were worse than doing nothing.** Break-even at
  +1R then trail 1R returned +0.17R; arming at +0.5R returned −0.03R. Both
  below the +0.28R hand-exit baseline. Moving the stop to breakeven turns
  ordinary pullbacks into scratches and taxes precisely the trades that
  later work. This is standard retail advice and it is the worst rule tested
  here.
- **Discretion helped on the loser.** AIRO was hand-closed at −0.29R; every
  mechanical rule that let it run took −1.00R. So the correct fix is
  asymmetric — mechanise the upside with a target, keep a same-session time
  stop on the downside rather than always riding to the price stop.

**Blocking constraint found while specifying the fix:** `place_equity_order`
has no bracket/OCO — market, limit, stop_market, stop_limit, single-leg
only. `get_advanced_orders` reads OCO but nothing places one. A resting stop
and a resting target therefore cannot coexist on the same shares, which is
precisely why Friday's $7.80 AEYE stop was rejected while the $7.08 GTC stop
held all 19 shares. The target has to come from a manually-placed app
bracket, or from intraday agent monitoring (same scheduling gap as S2), or
be downgraded to a time stop.

Limits: n=4, one week, one regime, one screen. Within-bar sequencing is
assumed on 5-minute bars. Limit-target fills are realistic; stop fills can
slip worse than modelled. Re-test at n≥15 before treating 1.0–1.5R as
settled.

## Also available (not from a user-provided link)

- **Robinhood connector** (`get_earnings_calendar`, `get_earnings_results`,
  `get_financials`) — earnings dates/results and fundamentals for specific
  symbols. Already wired into research; see README.
- **General WebSearch** — works for "what's happening with X today" style
  queries; quality varies by query specificity.

## 2026-08-17 S7 options screen — ZIM and BULL, both rejected on real numbers

Ran the S7 catalyst-mismatch methodology manually (option_scanner.py's own
process, executed via direct tool calls rather than the subprocess) against
the two most promising near-term earnings names from the 14-day calendar.

**ZIM** (reports 2026-08-19 am, Q2): 5 measurable past earnings-day moves
(close-to-close, am timing) from 2025-05-19 through 2026-05-20: +5.67%,
-1.41%, 0.0%, +4.67%, -1.53%. Mean |move| 2.66%, median 1.53% — smaller than
its EPS-surprise reputation suggests; the stock's price doesn't react
proportionally to trailing EPS beats/misses (freight-rate data likely leaks
ahead of the print for a shipping name). ATM straddle for the 2026-08-21
expiry ($29 call mid $0.80 + $29 put mid $0.875) implies a 4.95% expected
move. Mismatch ratio 1.86 (mean) to 3.24 (median) — both far above the 0.85
cutoff. IV is already pricing more than the stock's own history supports.
The $31 OTM call (delta 0.20, inside the 0.10-0.55 band) additionally fails
on spread: 40% vs the 15% max.

**BULL** (reports 2026-08-19 pm, Q2): 4 measurable past moves (pm timing,
report-close to next-close) from 2025-08-28 through 2026-05-21: -7.36%,
+0.48%, -5.60%, -6.51%. Mean 4.99%, median 6.06% — genuinely volatile,
unlike ZIM. But the ATM straddle for 2026-08-21 ($8 call mid $0.415 + $8 put
mid $0.315, haircut 0.85) implies a 7.66% expected move — still bigger than
the historical average. Mismatch ratio 1.27 (median) to 1.54 (mean), both
above 0.85. The $9 OTM call passes every structural filter (10.5% spread,
12518 OI on the $8 side, delta 0.20) but fails the same edge test. This is
IV correctly pricing a big mover, not a mismatch.

Conclusion: no options trade today. Two real candidates checked with real
option-chain data, both rejected on the actual math, not assumed. Matches
the S7 track record: 0 of 4 prior contracts (ONDS, LUNR, STNE, NKTR) passed
either; this makes it 0 of 6. The screen is built to say no most days — see
option_scanner.py's own framing. Did not force a marginal trade to have
something to report.

## 2026-08-17 The user's own scalping — the first real edge in this repo

The account's Investing account (••••7822, margin, NOT the Agentic account
this agent trades) was up **+$137.44 / +36.29%** on 2026-08-17. The Agentic
account was up $6.03 / 1.37% the same day on the same tape. That gap is the
most useful data this repo has produced, and it is the user's own execution,
not a book.

Pulled the real fills with timestamps from `get_equity_orders` on ••••7822
rather than reading the screenshots. Six IPST round trips:

| # | Buy ET | Sell ET | Hold | Buy | Sell | P&L | % |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 10:21:51 | 10:27:02 | 5.2m | 6.84 | 7.26 | +8.45 | +6.2% |
| 2 | 10:31:05 | 10:33:34 | 2.5m | 7.55 | 7.13 | −8.40 | −5.6% |
| 3 | 10:57:45 | 10:59:53 | **2.1m** | 7.72 | 9.57 | **+36.96** | **+23.9%** |
| 4 | 11:33:23 | 11:38:37 | 5.2m | 8.24 | 8.39 | +4.27 | +1.7% |
| 5 | 11:45:32 | 11:46:19 | **0.8m** | 8.54 | 8.23 | −9.30 | −3.6% |
| 6 | 12:23:28 | 12:25:04 | 1.6m | 7.71 | 7.63 | −2.40 | −1.0% |

**IPST net +$29.58 on 3 wins / 3 losses.** Median hold **149 seconds**;
fastest exit 46 seconds. Same pattern on WFF ($4.49 → $10.20 range traded
repeatedly) and OSRH. This is the same instrument (IPST) this agent screened
at 08:56 ET and rejected as "pump chatter, sit this window out."

### What the minute bars say about entry and exit

Trade 3, the +23.9% winner. Minute volume around the 10:57:45 entry:

| Bar | Volume | vs prev | Close |
| --- | --- | --- | --- |
| 10:56 | 62,551 | — | 7.47 |
| **10:57** | **251,916** | **4.0x** | 7.685 |
| 10:58 | 283,689 | 1.1x | 7.881 |
| 10:59 | 660,285 | 2.3x | **9.66** |
| 11:00 | 420,764 | 0.6x | 8.645 |

Entry was **into** the 4.0x volume-surge bar, filled at 7.7174 near that
bar's 7.75 high. Exit at 9.5654 came 2m08s later, inside the 660k-share
climax bar whose high was 9.66 — **sold within 1% of the absolute peak.**
The very next minute closed 8.645, a −10% drop. Getting out on the climax
rather than after it is the whole trade.

Trade 2, the −5.6% loser, is the same setup entered one bar too late:

| Bar | Volume | vs prev | Close |
| --- | --- | --- | --- |
| 10:30 | 368,036 | 3.3x | 7.615 |
| **10:31** | **149,480** | **0.4x** | 7.58 |
| 10:32 | 206,055 | 1.4x | 7.30 |

The surge bar was 10:30. The 10:31 entry landed as volume collapsed to 0.4x
— buying the extension after the buyers were gone. Cut 2.5 minutes later.

**The mechanism, stated plainly:** buy *during* a volume surge that is
breaking price upward; sell into the climax; and when volume does not follow
within a minute or two, exit immediately for a small loss. Three losers
averaged −3.4%; the one winner made +23.9%. **The asymmetry is manufactured
by exit speed, not by entry accuracy** — a 50% hit rate is fine when losers
are cut in ~90 seconds and the winner is allowed to go vertical.

### Why this repo's rules produced the opposite

Direct contradictions with `RULES.md`, all of them load-bearing:

- **Rule 1 (name the news before buying)** is an entry gate built for a
  position held over hours. It rejected IPST at 08:56 ET on correct
  reasoning — the Stocktwits chatter genuinely was pump talk, and the stock
  genuinely did round-trip. But a 2-minute trade does not need the narrative
  to be *true*, only the volume to be *real*. Rule 1 is the right gate for
  S8 and the wrong gate for a scalp.
- **Rule 4 (target = entry + 1.25R)** caps the winner. Applied to trade 3 it
  would have exited around 8.1 instead of 9.57 — turning +23.9% into roughly
  +5%, throwing away three quarters of the day's profit on the single trade
  that carried it.
- **Rule 7 (close by the bell)** implies a hold measured in hours. The real
  time stop here is ~90 seconds.

Not a reason to delete those rules — they belong to S8, which is a different
strategy with a different holding period. It is a reason to stop pretending
one rule set covers both.

### What this agent can and cannot do about it — stated honestly

**Cannot:** replicate this. A 149-second median hold with a 46-second
fastest exit requires reacting inside a single minute bar. This agent runs
on scheduled check-ins and each one costs 30–60s of tool calls before a
decision exists. By the time a 4x volume bar is detected, read, and acted
on, the move it signalled is over. Promising to auto-scalp would be
promising something the execution model cannot deliver, and the honest
version of that promise is "no."

For scale: at 11:45:32 ET the user bought IPST at 8.54; at 11:45:38 — six
seconds later — this agent bought OCUL at 10.59. The user was flat 47
seconds later for −3.6%. The agent held four hours for +0.36R (+$0.70).
Same minute, same tape, two entirely different games.

**Can:** watch far more names at once than a human, and compute the surge
condition on live minute bars across a whole watchlist. The realistic
division of labour is **agent detects, human executes** — this agent
monitoring N symbols for the 3–4x volume-surge-with-price-breakout
condition and surfacing it fast, the user pulling the trigger. That plays to
what each side is actually good at instead of asking either to do the
other's job badly.

### The scanner built from it — `scalp_signal.py` + `scalp_scan.py` (2026-08-17)

Thresholds derived by measuring 1,530 minute bars from the five symbols the
user traded that day, NOT by picking round numbers. Entry modelled at the
signal bar's close (the earliest a scanner can honestly act — a bar must
finish before its volume is known).

**The negative result came first and is the more useful half.** Volume surge
alone is worse than random: bars at >=4x median volume had a median 5-bar
MFE of +0.95% versus a +1.35% all-bars baseline. A volume spike with no
price response is as often a selling climax as a breakout. The scanner
enforces this — `detect_entry` reports a 10x-volume flat bar as an explicit
non-signal, and `test_scalp_signal.py` asserts it.

Volume only earns its place as *confirmation*. At bar return >= 2%:

| filter | median MFE | median MAE | reach +3% |
| --- | --- | --- | --- |
| no volume filter | +4.31% | −3.76% | 61% |
| **+ surge >= 3x** | **+7.52%** | **−2.84%** | **71%** |
| + surge < 3x (control) | +3.57% | −4.15% | 57% |

**The magnitudes are not trustworthy and the module says so in its own
docstring.** Simulating the full rule over the 41 signals returns +709%,
which is not an edge: 28 of 41 lost money, the median outcome is the −2%
stop, three trades produced 86% of the profit, and +699.6% of the +709.4%
came from a single symbol (WFF, $4.49 → $10.20 that session). IPST
contributed +9.2%, OSRH −0.2%. Strip WFF and the rule is flat. One stock's
trend on one day, caught three times.

What survives is the *shape*: most signals lose a little, a few win a lot —
the same asymmetry as the user's own day (three losers averaging −3.4%, one
winner +23.9%).

**Tested and rejected: mechanizing the user's climax exit.** The user sold
the +23.9% trade at 9.5654 inside the 660k-share vertical bar, within 1% of
its 9.66 high. The mechanical trailing rule (exit on a close below the prior
bar's low) instead held through the pullback and exited at **+12.17%** —
roughly half. Tempting to add "sell into any bar up X%" to close that gap.
Tested across all 41 signals, it makes things much worse:

| exit rule | total | best trade |
| --- | --- | --- |
| **trail only** | **+761.8%** | **+247.6%** |
| + sell into any bar >= 5% | +186.4% | +50.8% |
| + sell into any bar >= 10% | +165.9% | +50.8% |
| + sell into any bar >= 20% | +410.1% | +121.6% |

Every version truncates the fat tail that produces all the profit. **The
user's discretionary climax read beat the mechanical rule on that one trade
and would lose to it as a policy** — so it stays out of the code, and the
judgment stays with the human. This is also why `decide_exit` has no profit
target at all: this repo's own Rule 4 (target = entry + 1.25R) would have
exited the user's winner near $8.10 instead of $9.57.

**Live check:** replaying the scanner against the tape as of 10:57 ET fires
on IPST and only IPST out of the five symbols — the same minute the user
entered. The regression test in `test_scalp_signal.py` pins both sides: the
10:57 bar (before the +23.9% winner) must fire, and the 10:31 bar (before
the −5.6% loser, entered one bar after the surge had passed) must not.

### Out-of-sample test — WETO, 2026-08-17, and why the +709% number is wrong

Requested directly: "not just IPST, i trade wff, osrh, weto." WFF and OSRH
were already inside the original 41-signal study (per-symbol: IPST +9.2%,
WFF +699.6%, OSRH −0.2%, OABI +0.7%). WETO was not — it wasn't one of the
five symbols the thresholds were derived from, which makes it the first
real out-of-sample test the scanner has had.

**It failed.** 11 signals fired on WETO's regular session ($10.16 → $24.79,
arguably a bigger trend day than WFF's). Net result: **−4.4%, 3 wins of
11, 8 of 11 hit the −2% hard stop.** Same entry logic, same real bars,
opposite sign.

**Diagnosing rather than re-tuning** (re-tuning after seeing the failure
would be curve-fitting the failure away, exactly what Rule 0 forbids):
traced WFF's four biggest signals (bars 35/38/39/40) and found every one
exited on the **time cap**, not the trail — cut at 15 bars while still
running +150% to +248%. The rule never told those trades to exit; the
15-bar limit did, and the trend happened to still be climbing when it hit.
That is a property of where the clock ran out, not a property of the
entry signal.

WETO's 11 signals fired at points inside its own comparably large trend
that were *not* followed by a clean run — mid-trend pauses that rolled
over, caught by the tight stop before anything developed.

**Conclusion, stated as precisely as the evidence allows:** the rule
reliably detects a real, volume-confirmed local breakout (that half is
still supported — WETO's signal bars were genuine breaks, not noise, same
shape as IPST's). It does **not** reliably distinguish the start of an
hours-long move from a pause inside one that is about to fail. The
+709%/mostly-WFF backtest number should be read as one lucky mechanical
accident, not a rate. `scalp_signal.py`'s `confidence` field now says this
on every fired signal, not just in the docstring — the honest limitation
travels with the alert, not just the source code.

Pinned as a permanent regression test in `test_scalp_signal.py` against
real WETO bars (21 minute bars ending 16:09 UTC, transcribed by script from
`get_equity_historicals`, not by eye) so this cannot silently get
oversold later: the signal bar correctly fires, and the very next real bar
correctly hits the stop for −1.09%, matching the full-day simulation
exactly.

### Surge Watch dashboard — 2026-08-18, and the capability check behind it

Before building: checked whether a published page could poll Robinhood
directly on its own (no agent in the loop). It cannot, in this environment
— the `mcp` artifact capability needs `mcp__claude_ai_*`-prefixed tools to
exist for the target connectors, and none do here, even though
Robinhood/Stocklake/Stocktwits are all connected for this agent's own tool
calls. Checked via `ListConnectors` and `ToolSearch`, not assumed.

So the page (`surge-watch.html`) is honest about what it actually is: a
static artifact at one stable URL, refreshed by this agent pulling real
data and republishing — not a page that live-polls the market in the
viewer's browser. The UI says this explicitly ("This page updates when
refreshed and republished — not on its own while you're looking at it").

Two lean scheduled refreshes set for 2026-08-18: ~7:00 ET (early premarket)
and ~8:40 ET (RULES.md's entry window open), each pulling live quotes +
minute bars and re-running `scalp_signal.py`'s `detect_entry` for real,
then republishing to the same artifact URL. Deliberately not a dense chain
of wakeups overnight — nothing meaningful happens in the dead hours, and
the user asked to keep this efficient.

URL: https://claude.ai/code/artifact/0c00fa02-b7c2-47cd-8074-224d17f2fbcf

### Robinhood's own scanners beat Stocklake's screener for this job — 2026-08-18

The user's account already has saved scanners (`get_scans` / `run_scan`),
built in Legend, not something this session created. One is called "Early
Momentum Ignition" (scan_id `9d3566de-aca8-4b0e-8099-304a3e474d92`):
price $2-20, day volume >300k, float <20M shares, **1-hour relative
volume >3x**. That last filter is exactly the "surge" half of
`scalp_signal.py`'s detection rule, computed by the broker on real
intraday volume, not derived after the fact.

Ran it live, premarket 2026-08-18: 98 matches, sorted by % change. Real
verification, not assumed: **IPST and WFF — two of the user's own traded
symbols — were both in the results**, IPST specifically flagged with
1h relative volume of 3,753x. The top result, XOS (premarket +82%), was
checked against real 5-minute bars (`get_equity_historicals`, not
interpolated fill): $2.09 at 20:00 UTC on 8/17 to $4.69 by 21:30 UTC on
volume climbing from ~300k to over 1M shares per 5-min bar. The move is
real.

This is a better coarse filter than Stocklake's `get_screener` for this
specific use case: it's sourced directly from the broker (no second data
vendor to go stale — see the 2026-08-13 Stocklake staleness note above),
it already has float and hourly relative volume built in (Stocklake's
screener doesn't), and it's the same feed the orders execute against.
**Stocklake still has a job** — `get_stock_research` and
`get_insider_activity` for catalyst/insider verification once a candidate
is found — but it should not be the primary momentum scanner. Switched
Surge Watch's "Today's market scan" section and both scheduled refreshes
to run Robinhood's `run_scan` first.

A second saved scan, "Warrior Trading Style - Low Float Volume Movers"
(scan_id `32ff11e9-065f-40b0-99a0-c5971241c435`, float <50M, volume
>500k AND >=10M, price $1-20) is a looser secondary net — not yet used,
noted here in case Early Momentum Ignition's float cap of 20M ever proves
too tight.

### All saved Robinhood scans checked, 2026-08-18 overnight — account safety + full inventory

User: "check my other saved scans too... anything that is similar and
seems important do it." Ran every remaining saved scan live and checked
account state before the user slept. Real results, not summarized from
memory:

**Account safety (both accounts checked directly):**
- Agentic account (432805174): zero positions, and its order history's
  only two non-terminal-looking entries (IVF, WETO buys) were both
  `state: rejected` — never live. Flat, nothing at risk overnight.
- Real trading account (5SH47822): one open position, `ACETQZZ` (200 sh,
  avg $0.22). Checked, not assumed: `get_equity_quotes` returned
  `inactive_instruments: ["ACETQZZ"]` and `search` found nothing — this
  is a dead/delisted ticker, not a live holding with overnight risk, just
  stuck. No open (non-terminal) orders on this account either — its two
  non-terminal-looking entries (IVF, WETO) were also both rejected.

**"Warrior Trading Style - Low Float Volume Movers"** (`32ff11e9...`,
float <50M, volume >=10M): 10 matches live. Overlapped with Early
Momentum Ignition on XOS/WFF/IPST, but also surfaced AUUD and IVF —
genuinely new names the first scan didn't catch. Wired in as a second
scan alongside Early Momentum Ignition (both scheduled refreshes updated
2026-08-18 ~03:45 ET).

**"Daily gainers"** (`4ace94c6...`, no real filter beyond asset type):
generic sorted list, 100+ matches. Useful as an independent cross-check —
it separately reconfirmed WETO as a real premarket mover (+40% shown),
same symbol the user already flagged as "going crazy." Not wired in
anywhere; redundant with the two scans above as a filter.

**"High options volume and IV"** (`ce0cc952...`, relative options volume
>2x): 112 matches (HDSN, NGEN, VNRX, WRAP, PROP at the top). Real and
working. This belongs to the S7 options track, not the scalp dashboard —
logged here for whenever options screening resumes, not merged into
Surge Watch.

**"Daily Movers - Fastest Growers (Quality Filtered)"** (`183fa533...`,
mcap >$50M, RSI/ADX computed) and **"Building Momentum Candidates"**
(`8083a928...`, RSI>55, ADX>25, MACD>0): both real and working, both
surfaced genuine trending names with real RSI/ADX values (AMLX, DFSC,
TNDM, CODI...). This is trend-following territory — S1 in CLAUDE.md's
strategy index, which has been blocked since 2026-08-16 because its
`daily_allowlist.json` doesn't exist. These two scans are a real,
live-verified source that could fill that gap someday. Deliberately
**not** wired into anything tonight — per CLAUDE.md's "strategies stay
separate unless told to merge," this is S1's problem to solve when asked,
not a reason to touch the scalp dashboard.

**"Untitled Scan"** (`c3d98719...`, volume >1M only): not run — no
distinguishing filter beyond what the others already cover, so running it
would add API calls without new information. Noted here, not tested,
consistent with Rule 0 (no claim is made about what it returns).
