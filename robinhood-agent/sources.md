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

---

## 2026-08-19 ~07:00 ET — Premarket watch, "August 19" watchlist built

Ran all three market scans live: "Early Momentum Ignition" (89 matches,
top mover TNON +105.7%), "Warrior Trading Style" (14 matches, top movers
TNON/BIVI/MSS), "Daily gainers" (202 matches, top real movers RDAC/DUKR —
both too thin to trust, <15K shares volume — then TNON, MRNA +74.7%, BIVI,
ZNB, BSEM, CAST +23.8%).

**Catalyst-checked via Stocktwits pulse + Robinhood fundamentals before
including anything, same discipline as the "August 11" list:**

- **MRNA** — real, verified catalyst: Merck/Moderna's Intismeran melanoma
  vaccine hit its Phase 3 primary endpoint (multiple independent Stocktwits
  posts citing the same wire item, LiveSquawk). $25B cap, real liquidity,
  broke through its own 52-week high on the news. Best pick of the day by
  a wide margin.
- **CAST** (FreeCast) — real business-development news cited (regained
  full control of InvestorNewsChannel.com, cited DIRECTV/Starlink
  distribution deals), but from a single Stocktwits-relayed source, not an
  independently verified filing. 154M shares volume, real liquidity.
  Included with that caveat.
- **TNON** — the loudest mover (+105-109%) but flagged NEGATIVE on real
  grounds, not excluded silently: `financial_status_indicator` =
  Noncompliant, and the Stocktwits community itself is calling out a
  "$100M mixed securities shelf filing Monday" (real dilution risk) and
  "recycled old news" behind the Benzinga pickup. Included per the
  "August 11" precedent of logging risky/no-real-catalyst movers with an
  explicit warning rather than pretending they weren't checked.
- **Excluded, no distinct catalyst found**: BIVI (BioVie) and MSS (Maison
  Solutions) and TGL (Treasure Global) — all three showed up only in
  generic "premarket movers" group-posts with no sourced news behind them,
  tiny floats (BIVI 7.2M, MSS/TGL both under 2M), and MSS/TGL are both
  down >98% from a 52-week high a year ago. RDAC (+188.9%) and DUKR
  (+128.1%) excluded outright — real % moves but under 15,000 shares of
  volume each, not tradeable size.

Watchlist created: **"August 19"** (`c15a7e55-bc55-4869-bf4f-6eb82a04c3e4`),
3 items (MRNA, CAST, TNON), description summarizes the catalyst/risk read
above.

**Options monitoring (watch-only, per the user's standing instruction that
options stay agent-monitored but not agent-traded):** ran "High options
volume and IV" (65 matches). Standout relative-options-volume names: CVX
(6.99x, but only 26.9% IV — unusual combo for a mega-cap, worth noting),
CMPX (7.06x, 133.7% IV), REI (5.93x), AS (5.25x), ASX (4.82x). Highest raw
IV in the scan: ALEC 191.7%, BEEM 186.4%, QNC 182.1%, CEPO 144.8%, AVD
146.8%. None cross-referenced further against S7's mismatch-ratio/IV-HV
gates tonight — this is a report, not a screen run, per the trigger's own
instruction to keep this separate from any entry decision.

## 2026-08-20 ~00:35 ET — user-requested screen, "August 20" watchlist built

User asked directly (not the scheduled trigger, ~4.5hrs before it would have
fired anyway): teach Greeks, screen the market, build tomorrow's watchlist,
delete "August 19" (no delete tool exists — repurposed in place, same as
the "August 11" precedent), and check what time stocks usually start moving
unusually.

**Real-data sources used:** Stocktwits `get_trending_symbols` (overnight
premarket movers), Robinhood `get_scans`/saved scan list, `get_earnings_calendar`
(08-20/08-21 window), `get_symbol_messages` for catalyst verification on the
two names actually added, `get_stock_news` (Stocklake) for BULL, real quotes
via `get_equity_quotes`.

- **MRNA** — dropped. Yesterday's real catalyst (Merck Phase 3 win, +75%)
  already fully played out; overnight it's giving some back (-5% to ~$165
  premarket off a $174.38 close). Rule: don't chase an already-printed move
  (same rule the user set for S7 after the MRNA conversation yesterday,
  applied here to equities too).
- **CAST** — dropped. No fresh catalyst; flat/slightly down overnight
  ($1.70 close -> ~$1.57).
- **TNON** — dropped. Already flagged high-risk/no-real-catalyst on 08-19;
  now actively crashing overnight (~-23%, $11.41 close -> ~$8.70). Confirms
  the original caution was correct.
- **BULL** (Webull) — added. Real, dated catalyst: Q2 earnings call
  8/19 (`get_stock_news` confirms), then a short-covering squeeze on top
  (Stocktwits community explicitly citing "short covering... as the
  article says"). +14.6% premarket. Flagged as squeeze-driven, so
  high-variance — a real catalyst, but one that can give back hard once
  the squeeze is done.
- **BMNR** (BitMine Immersion Technologies) — added. Real, verified,
  directly traceable catalyst: it's a corporate ETH-treasury proxy, and
  ETH itself is up ~18% today (Treasury buyback news, real ETF inflows,
  short squeeze — see today's separate ETH research). BMNR +6.3%
  premarket, tracking ETH's move; Fundstrat's Tom Lee thesis (BMNR
  outperforms ETH after ETH outperforms BTC) referenced repeatedly in the
  community as the reason people are in it, not just price action alone.

Watchlist: renamed **"August 19" -> "August 20"** in place (same
`c15a7e55-bc55-4869-bf4f-6eb82a04c3e4` id — no `delete_watchlist` tool
exists in this MCP connector), now 2 items (BULL, BMNR).

**Standing process change:** created a recurring weekday trigger ("Premarket
watch: build the day's watchlist", 7:00 AM ET / `0 11 * * 1-5`) so this
screen-and-rename process happens automatically each morning going forward,
separate from the existing 8am ET S7 options trigger and 4pm ET growth-sleeve
trigger. Previously this had only been done ad hoc / via one-off reminders.

**"What time do stocks usually start moving unusually" — answered from real
evidence gathered across this account's actual sessions, not just general
knowledge:** the MRNA move (08-19) began at 6:00 AM ET premarket, right as
premarket liquidity thickens. Tonight's BULL/BMNR moves are showing in the
1-4 AM ET overnight session, but that window has much thinner volume and
wider spreads than real premarket — a move seen at 2 AM ET is far less
confirmed than the same move still holding by 7-8 AM ET. General pattern,
not a hard rule: dated catalysts (earnings, trial results, FDA, M&A) tend to
drop either right at the open/close of the *prior* session (after-hours PM
releases, or a wire hitting right before the next day's premarket opens
~4 AM ET) or get confirmed/extended in the 8:00-9:30 AM ET premarket ramp as
volume builds toward the open. The riskiest window to trust a move in is
the deep overnight (12-4 AM ET) — real names do move there, but thin volume
means it's the least reliable point to judge whether a move will hold.

## 2026-08-20 ~7:15 AM ET — recurring premarket-watch trigger, first real run

First automatic firing of the new daily trigger (created a few hours after
midnight the same night). "August 20" already existed from the earlier
manual session, so no rename needed this cycle — just a refresh now that
real premarket (not thin overnight) volume is in.

**Real-data sources used:** Stocktwits `get_trending_symbols` (now `session:
PRE_MARKET`, not overnight), `get_symbol_messages` for MSTR/WMT/HOOD,
`get_earnings_calendar` (many 08-20 entries now show real `eps.actual`,
confirming which reports already landed), Robinhood `run_scan` on "Daily
Movers - Fastest Growers" and "Warrior Trading Style - Low Float Volume
Movers".

**The dominant real theme today: a dated, sourced macro/policy catalyst.**
Stocktwits carried a same-morning item: Trump hosted crypto executives at
the White House and urged Congress to pass the Clarity Act (crypto
regulatory clarity); BTC named as up double digits intraday with a real
short-squeeze component ($2.7B cited). This is a genuine, dated, sourced
catalyst (not just "crypto is green today") and it mechanically explains
the whole crypto-equity complex moving together: **MSTR** +10.5%
(leveraged BTC balance-sheet proxy, community explicitly ties the move to
BTC%), **COIN** +7.7% (the purest-play exchange name), **BMNR** +8%
(already on the list, same ETH-proxy logic as last night), **BULL** still
+14-15% (its own earnings+squeeze catalyst from last night, now also
riding the sector tailwind), **HOOD** +5.5% (crypto-trading-volume
beneficiary, same White House news cited directly in its own feed).
Smaller/less liquid names showing the identical pattern (CAN, UPXI, DFDV,
BTBT, SBET, BKKT, ABTC, all +6-14%) were deliberately **not** added --
same real catalyst, but redundant and lower quality/liquidity than
MSTR/COIN/BMNR/HOOD; curating for quality, not stacking every ticker that
moved on the same news.

**WMT** -6.1% ($107.28 pm vs $114.30 close) -- added on a *different*,
independently real catalyst: Q2 earnings actually **beat** (adj EPS $0.81
vs $0.74 est, revenue beat), but management **cut Q3 guidance** (62-64c
vs 68c est) and comp sales missed estimates. Confirmed via LiveSquawk and
StocktwitsEarnings' verified data feeds inside the Stocktwits results, not
rumor. A real "beat then guide down" divergence, not noise.

**MRNA** -11.6% premarket, continuing to give back yesterday's spike
(down from $174.38 close toward $154). Confirms last night's call to drop
it -- the catalyst was already fully priced in, and it's now unwinding
exactly as expected rather than offering a fresh entry.

**Scans checked for anything missed:** "Warrior Trading Style - Low Float"
(16 matches) -- all either no fresh catalyst or, in TNON's case, actively
confirming the prior night's dilution-risk warning (now -30%). Nothing
added from this scan. "Daily Movers - Fastest Growers" (large result,
read via jq) -- top movers were entirely the same crypto-complex names
already covered above, plus FUTU (+9.3%, real earnings today) which was
considered and left off for now (lower profile, thinner liquidity than
the six already on the list -- can revisit if it holds through the open).

Watchlist: **"August 20"** now 6 items (BULL, BMNR, MSTR, COIN, HOOD,
WMT), description updated in place (256-char cap, full reasoning here
instead).

## 2026-08-20 ~22:00 ET — scanner tooling built (user asked for a Warrior-style scanner)

User linked warriortrading.com/scanners and asked "can you create a scanner
like this? do you need api or what do you need?" Fetched their actual page
rather than assuming: Day Trade Dash is a paid subscription — real-time
alerts across strategies (momentum squeezes, reversals, gappers, halts),
columns for Float, Volume, Relative Volume, Gap%, 52wk hi/lo, ATR, short
interest, bundled news feed, audio alerts, third-party data vendor unnamed.

**Answer on "do you need an API": no.** The Robinhood MCP connector already
returns the same core fields via saved scans (`run_scan`) — Float, Volume,
Relative Volume, Gap, % Change, RSI, ADX, MACD. What Warrior has that we
don't: audio alerts, a self-updating table, 52wk hi/lo + short-interest
columns, and news in the same pane. User said "lets do both" to the two
options offered.

**A. Alert trigger** (`trig_011uqSeqdqMoS3e5ZUTk13jN`, `0 14-20 * * 1-5`,
hourly 10am-4pm ET). Runs both momentum scans, then filters hard: >5% change
AND elevated RVOL AND not already faded off the high, then requires a
nameable dated catalyst before alerting. Explicitly instructed that silence
is the correct output most hours and that false alerts are worse than none.
Alert-only — cannot place orders; execution stays in S7/S9.

**B. "Ignition Board" dashboard** —
https://claude.ai/code/artifact/952415af-3876-453b-a469-db076662881e
A published artifact declaring the `mcp` capability scoped to
`Robinhood: [run_scan, get_scans]` — **read-only by construction**; no order
tool is in the manifest, so the page structurally cannot trade even if its
code were changed. Uses `watchTool` with a 60s refetch (Robinhood offers no
push/streaming through this connector, so "live" = polling, stated plainly
to the user). Built only against request/response shapes actually observed
in-session for both tools — no guessed API shapes.

Design decisions worth keeping: (1) the row "quality" stripe encodes
direction + whether RVOL backs the move, which is the user's #1 misread;
(2) an always-available panel restates the four pre-entry checks plus the
n=108 holding-time finding, so the tool teaches the read instead of just
listing tickers; (3) it detects non-regular-hours from an ET clock and warns
that % change / RVOL go flat-or-inflated on thin prints — a real failure
mode observed directly in the 08-20 after-hours scan pull, where every row
showed 0% change and RVOL of exactly 1.

## 2026-08-21 — "Bell to Bell": a standalone scanner with no Claude dependency

User clarified what they actually wanted: *"I just need an independent
scanner that I can use without claude."* The Ignition Board artifact,
though it costs no model tokens, is hosted on claude.ai and reads data
through the user's claude.ai Robinhood connector — so it is NOT
independent. Correct answer required a different build.

**First, the answer they already owned:** the saved scans ("Early Momentum
Ignition", "Warrior Trading Style - Low Float Volume Movers") live in the
user's own Robinhood account. The agent has been reading them through a
connector, but the user can open them in the Robinhood app with zero
Claude involvement. Told them this before building anything.

**Built: `tools/bell-to-bell.html`** — a single self-contained local HTML
file. No API key, no login, no server, no Claude. Uses TradingView's free
embeddable widgets, whose script URLs were verified live rather than
recalled: `embed-widget-hotlists.js` (day's gainers/losers/most active),
`embed-widget-screener.js` (full US screener with its own toolbar), and
`embed-widget-advanced-chart.js` (5-min chart, ET timezone).

Design notes worth keeping:
- **Widgets are mounted from JS, not pasted as static markup.** TradingView
  reads its config from a script tag's text content at mount time, so a
  theme toggle or symbol change requires re-mounting. Building them
  programmatically is what makes both work.
- **The chart section exists specifically to close check #3** ("early or
  already extended?") — the one check the Ignition Board structurally
  could not answer, because `run_scan` returns no intraday high.
- Same after-hours warning as the Ignition Board, from the same real
  observation (08-20 after-hours scan pull returned 0% change and RVOL of
  exactly 1 on every row).
- `defaultScreen` left at `most_capitalized`, the only preset value
  verified from TradingView's own demo snippet. Rather than guess at
  preset names like "top_gainers", the UI tells the user to switch presets
  via the widget's toolbar, and the hotlists widget covers movers anyway.

**Free-scanner landscape checked** (web search, 2026): TradingView free is
the strongest free screener (~14k US stocks, saveable screens); Barchart
free is good for unusual/relative volume; **Finviz free is 15-minute
delayed — explicitly warned against for day-trade entries**, which matters
for this user specifically.

## 2026-08-21 ~7:20 AM ET — premarket watch, "August 21" built

Second automatic firing of the daily premarket trigger. Renamed
"August 20" -> "August 21" in place (5 items).

**Dominant theme, day 2: the Bitcoin complex is extending, not fading.**
Yesterday's catalyst (White House crypto event / Clarity Act push + BTC
surge) has not exhausted — it accelerated overnight. Real premarket
numbers vs 08-20 closes:

| Symbol | Premarket | Close | Move |
|---|---|---|---|
| MSTR | $122.38 | $112.39 | **+8.9%** |
| ROST | $247.50 | $228.99 | **+8.1%** |
| COIN | $181.70 | $172.35 | **+5.4%** |
| BMNR | $22.57 | $21.57 | **+4.6%** |
| HOOD | $99.13 | $95.10 | **+4.2%** |
| BULL | $9.01 | $8.85 | +1.9% |
| WMT | $103.67 | $103.84 | -0.2% |

Corroborating the theme rather than assuming it: Stocktwits trending has
IBIT +6.6%, Grayscale BTC +6.7%, MSTY +8.6%, SBET +5.0% — the whole
BTC-linked cohort, not one name.

- **Kept: MSTR, COIN, HOOD, BMNR.** Same verified catalyst as yesterday,
  still live and expanding. **But flagged extended** — MSTR at +8.9%
  premarket on day 2 is exactly the "already printed" case S7 rule 4
  excludes for a fresh entry. Kept as names to watch for a pullback, not
  as clean entries.
- **Added ROST.** The one genuinely *fresh*, independently-dated catalyst
  today: Q2 earnings, reported 08-20 pm (confirmed on the earnings
  calendar with `eps.actual` now populated), +8.1% premarket. Not part of
  the crypto theme — independent.
- **Dropped BULL.** Was +14.6% premarket yesterday on earnings + short
  squeeze; today +1.9%. The squeeze has done its work. Textbook
  already-printed — dropped rather than held out of attachment.
- **Dropped WMT.** -0.2%, flat. The beat-then-guide-down repricing
  happened yesterday; nothing left to trade.
- **Considered and rejected: ASST** (Strive, +9.8% premarket). Checked
  `get_symbol_messages` directly: the entire thread is squeeze hype
  ("30% short", "squizee") with no independent dated catalyst — its move
  is purely derivative of BTC plus short positioning. Same discipline as
  08-20's rejection of the smaller crypto proxies: one theme does not
  justify stacking every ticker riding it. IBIT/MSTY/Grayscale BTC
  excluded as ETFs; SBET excluded as redundant to BMNR.

**Also noted, growth sleeve:** BTG trading $5.51 premarket vs a $5.38
close — above the $5.39 peak close that currently anchors the trailing
stop. If it holds through the session, today's 4:05 PM check should
ratchet the stop above $4.42 for the first time since 08-19.

## 2026-08-21 09:35 ET — S7 daily screen: GRRR checked, rejected; delta-floor drift found

Flat (no open S7 position), so ran the entry screen. Dated-catalyst track:
next earnings are Mon 08-24 / Tue 08-25. Best fit by price and liquidity
was **GRRR** (Gorilla Technology, $15.66 live, Q2 earnings 08-24 pm, so
effective catalyst 08-25; the 09-11 expiry clears it with room).

Real live chain, 09-11 calls, quoted 09:37 ET — **all rejected, and not
narrowly:**

| Strike | Ask | Cost | Delta | Spread | IV | OI / Vol |
|---|---|---|---|---|---|---|
| $16 | $1.80 | $180 | 0.52 | **61.8%** | 99% | 45 / 1 |
| $17 | $2.20 | $220 | 0.45 | **132.1%** | 121% | 12 / 0 |
| $18 | $1.65 | $165 | 0.37 | **138.5%** | 118% | 3 / 0 |
| $19-21 | — | — | 0.02 | no bid at all | — | 0-2 / 0 |

Run through `evaluate_candidate` rather than eyeballed; every one failed
on **spread** before the premium cap even applied. Worth noting *why*
that matters more than the price: at a 62-138% bid/ask spread these
contracts cannot be entered and exited at a fair price at any size. Even
with unlimited capital this is untradeable. IV of 99-121% into earnings
is the IV-crush setup the rules explicitly exclude. Robinhood's own
"chance of profit (long)" on the three: 29.6%, 25.2%, 21.1%.

**Running total: 9 real live checks, 9 rejections, 0 trades.**

### Defect found by this run: documented delta floor was never enforced

Running the real code printed its actual config — `min_delta 0.10` —
against a strategies.md section (written 08-19) asserting "no long option
is bought below roughly 0.30 delta." **The 0.30 was never in the code.**
Worse, `test_option_math.py` carries two fixtures the suite treats as
genuine *passing* setups with deltas of **0.25** and **0.28** — a 0.30
floor would reject both, so raising the gate would invalidate the suite's
own definition of a good trade.

Not silently reconciled, in either direction. Bumping a live-money gate
to match a number this file asserted without validation is precisely the
failure already caught once on S8's float-turnover threshold. Neither
0.10 nor 0.30 is backed by outcomes — S7 has zero trades. Documented as
open drift in strategies.md S7 with the enforced value (0.10) stated
plainly, and surfaced to the user as a decision rather than an edit.

## 2026-08-21 ~10:15 ET — Ignition Board: swing-setup panel + in-page alerts

User feedback: TradingView's screener (in Bell to Bell) lags/isn't
dependable. Real cause, not fixed by this session — it's a known
limitation of TradingView's free-tier real-time entitlements, outside
what an embedded widget can control. Pointed the user back to Ignition
Board as the dependable one, since it reads the same live Robinhood data
this session has used to actually operate the account all week, not a
third-party feed.

User then asked for two things: (1) a note on what's favorable for swing
trades specifically (distinct from the existing day-trade momentum
panel), including float; (2) an alert when that condition is met or about
to be met, "on time."

**Added a second, independent panel: "Swing setups."** Feeds from the
real `Growth Momentum (long-run)` scan (`2514847d-25cb-4628-9731-bb5b0ee7d246`)
-- the exact same scan `growth_signal.py`'s S9 sleeve is built on (market
cap > $1B, RSI 50-70, ADX > 20, avg volume > 500K, 1-month change > 5%,
all confirmed against `get_scans` output, not invented). Its own filters
are stated on the page as the real favorability criteria, since a row
only appears because it already cleared all five.

Float deliberately **not** shown on this panel, with an explicit note
why: this scan targets large/liquid names where float scarcity isn't the
governing risk the way it is on the low-float day-trade panel above (which
already showed float from the first build). Conflating the two would have
been dishonest, not just cosmetic.

**"About to be met" honestly scoped down.** `run_scan` only returns full
matches, not near-misses -- there's no reliable way to see a stock closing
in on the RSI/ADX band before it actually crosses. Said so on the page
rather than faking a proximity score. What the page can do, and does: flag
the instant a symbol newly appears in the scan's results, which is the
earliest this data can know.

**Alerting -- three channels, deliberately not resting on the least
reliable one.** This artifact runs inside claude.ai's frame; a real OS
push notification is often blocked there and can't be verified from this
session. So the primary channels are ones that reliably work in a
sandboxed frame: an in-page flash + a WebAudio beep + a running alert log
(all always logged; sound/flash only if the user opts in via the header
bell toggle) and the document title changing while the tab is unfocused.
A `Notification()` call is attempted only if the browser already reports
`permission: "granted"`, wrapped so any failure is silent -- never the
only thing anything depends on. The page's own footer now states plainly
that none of this works with the tab or browser closed.

New-qualifier tracking persists in localStorage keyed to the calendar
date, so a page reload during the same day doesn't re-fire alerts for
names already seen, and the set naturally resets the next day when the
scan's own results roll over.

## 2026-08-21 ~11:00 ET — Ignition Board: real 5-pillar scoring, order-book pressure; insider blocked

Three real asks: (1) float was showing empty for some scans, (2) score
against the actual documented "5 pillars" rule, (3) add insider activity,
(4, arrived mid-turn) track buy vs. sell pressure.

**Float-empty diagnosed, not just patched.** Not every saved Robinhood
scan carries a Float column at all (Growth Momentum, Daily gainers, etc.
don't) -- picking one of those in the dropdown made every row's Float cell
blank with no explanation, which reads as broken. Fixed two ways: the row
shaper now distinguishes "this scan doesn't report float" (shows `n/a`,
title-tipped) from "float is null for this specific row," and the page
now surfaces an explicit banner naming the two scans that do carry it
(Early Momentum Ignition, Warrior Trading Style) when the selected one
doesn't.

**Real 5-pillar scoring replaces the earlier ad hoc quality heuristic.**
Pulled the actual numbers from strategies.md's S3 section rather than
inventing new ones: rel. vol >= 5x, % change >= 10%, price $2-20,
float <= 20M -- the four NUMERIC pillars. Each row now shows a real
"N/4 pillars" chip (title-tipped with which ones passed) computed from
these exact thresholds, and a row scores out of 3 rather than being
silently marked as failing float when the underlying scan can't report
it. The 5th pillar, catalyst, is explicitly non-numeric per S3's own
documentation and is called out in the checks panel as something this
page cannot automate -- same honesty as the earlier per-row date already
established for "is this already extended."

**Insider activity: genuinely blocked, not skipped.** Checked
`get_insider_activity` live before promising anything -- **the Stocklake
connector itself needs re-authorization (expired token)**, a session-level
auth issue, not something fixable from inside this page. The tool's own
description also says "Pro tier only," so even after reauth it may not
answer without a paid tier -- flagged to the user rather than silently
built around. Nothing shipped for this; told the user plainly instead.

**Buy vs. sell pressure -- real, but scoped honestly.** Added a per-row,
click-to-check "Order Book" column using the real `get_equity_price_book`
tool (added to the artifact's manifest, tested live on SDOT before
shipping). Sums resting share size across the top 10 bid and ask levels
and shows e.g. "62% buy / 38% sell." Deliberately on-demand, not
auto-polled per row -- Robinhood's connector hasn't shown Stocklake-style
rate limits this session, but there's no reason to hammer 10+ symbols
every 60s when a click answers the question. Explicitly labeled in the UI
as RESTING LIMIT-ORDER imbalance, not executed trade flow -- this
connector has no tick-level buyer/seller classification, so this answers
"who wants to trade right now," a real but different question from "who
already did."

## 2026-08-21 ~11:20 ET — Ignition Board: favorability sort, real catalyst column; corrected Stocklake claim

**User caught a real mistake:** the last entry said "Stocklake needs
re-authorization," generalized from one failed `get_insider_activity`
call. User pushed back ("you have stocklake mcp"). Retested live rather
than argue from memory: `get_stock_news` succeeded immediately on the
same account, same session. **Correction: Stocklake itself is fine.**
Only `get_insider_activity` is blocked, and its own tool description says
"Pro tier only" -- almost certainly a tier gate on that one premium
endpoint, not a connector-wide auth failure. Recorded here so the
overbroad claim doesn't stand uncorrected in the log.

**Fixed a real bug from the previous edit, before a user ever hit it.**
The "Pillars" column had been added to the sortable COLS list with a
value that's an object (`{rvol,chg,price,float}`), but the sort
comparator did `x - y` on it -- objects minus objects is `NaN`, so
clicking that header would have silently done nothing. Caught while
building the requested favorability sort, not shipped broken: renamed the
sort key to the actual numeric `pillarsMet`, and extended the comparator
with proper per-key handling (string compare for symbol, cache lookups
for the two on-demand columns, tiebreak on relative volume for pillar
ties -- more real volume outranks less when pillar counts match).

**Default sort is now "most favorable ATM"** -- pillarsMet descending,
RVOL as tiebreaker -- directly answering what was asked, and it's what
loads first rather than something the user has to find.

**Added a real Catalyst column**, Stocklake's `get_stock_news` (days=3,
limit=3), click-to-check per symbol like the Order Book column -- never
auto-polled, because the guest tier hard-caps at 25 calls/day for the
whole account, shared with anything else this session uses Stocklake for
today. Shows the first real headline (title + published_at in the
tooltip) when one exists; **shows exactly "N/A" when none does**, per the
user's own wording, not a softened "no catalyst found."

## 2026-08-21 ~12:00 ET — Ignition Board: real float everywhere, via per-symbol fundamentals

User: "why is there float data n/a? cant you pull float data at all?" -- a
fair complaint about the earlier design (Swing panel omitted float on
purpose; main panel showed "n/a" for any scan without a Float column,
e.g. Growth Momentum). Rather than just explain it again, found a real
fix: `get_equity_fundamentals` reports float per symbol directly,
independent of which scan found the row -- confirmed live (NVDA, SDOT)
before wiring it in.

**Redesigned float sourcing end to end.** Added `ensureFundamentals()`:
auto-fetched (not click-gated, unlike Order Book/Catalyst -- Robinhood
hasn't shown rate limits this session, and float doesn't need per-minute
freshness), batches up to 10 symbols per call, 5-minute cache TTL.
`resolvedFloat(sym, scanFloat)` prefers the fundamentals value once it
loads, falling back to a scan's own Float column (when present) only
during the brief window before fundamentals responds -- avoids an empty
flash on first paint.

Refactored `shape()` into a pure column mapper plus a new `deriveRow()`
that computes float/pillars from whatever's authoritative *right now*;
called once synchronously after a scan result lands, and again after
each fundamentals batch resolves, so pillar counts and the float column
both self-correct without a manual refresh.

**Consequence: `pillarsOf` is now always 4, not scan-dependent.** The
earlier "3 of 3, this scan can't report float" carve-out is gone --
float is answerable for any row on any scan now, so every row is judged
against the same real bar.

**Swing panel gets a real Float column too**, sourced the same way,
replacing the earlier "intentionally omitted" framing (info-card copy
updated to match -- shown for reference, still not the risk that
matters for large-cap swing names, but no longer hidden).

Caught and fixed two real bugs while making this change, before either
reached the user: (1) the edit tool kept rejecting an exact-looking
string match around `onResult`'s tail -- `cat -A` traced it to a
non-breaking space (U+00A0) already sitting in the file, invisible in a
normal read; worked around with a byte-safe Python replace instead of
guessing at the visible text. (2) `floatLoading`'s condition had an
operator-precedence bug (`!a || a.state === 'loading' && b`) that also
referenced a `state: 'loading'` value the code never actually sets --
simplified to check `fundInFlight` directly, which is the real signal.

## 2026-08-21 ~4:03pm ET — S9 daily stop check: BTG ratcheted to $4.53

Growth sleeve daily stop check trigger fired. BTG closed today at $5.525,
a new high over both prior sessions ($5.27 close 08-19, $5.38 close 08-20).
`decide_stop_update(4.42, 5.525)` said ratchet: new stop $4.5305 (18%
below the new peak). Cancelled the resting $4.42 stop (verified
`state: cancelled`), then hit a real constraint placing the new one —
Robinhood rejected the raw $4.5305 stop_price ("Prices above $1.00 can't
have subpenny increments"). Rounded to $4.53 and it placed clean. New
order shows `state: queued`, same as the 08-19 ratchet — market was
already closed (4:03pm ET) when this ran, so a regular_hours stop_market
queues for tomorrow's open rather than resting live tonight. Not a
rejection, same pattern as last time. CLAUDE.md's S9 row updated with the
same detail.

## 2026-08-24 ~2:20am ET — premarket catalyst check ahead of market open

User asked me to find favorable option contracts on "quality trending
assets" today. Checked real overnight movers (Stocktwits trending,
Robinhood earnings calendar) at 2:20am ET, well before the 9:30am ET
regular open. Two names cleared a real, dated catalyst check:

- **BABA**: down ~4.7% overnight (~10% in HK trading) on a real, dated
  news event — a $10B primary equity offering priced in Hong Kong,
  reportedly the largest-ever follow-on by a HK-listed company. Dilution
  fear, not just price action. No earnings scheduled today per
  get_earnings_calendar.
- **AAOI**: down ~12.3% overnight, the largest mover checked. Real
  catalyst: an equity offering announcement plus retail chatter about
  forced margin-call selling. No earnings today.

Both would be PUT candidates given the negative catalyst, not the
trend-follow calls the user may have expected. CRWV and KLAC were also
checked and ruled out: CRWV's Stocktwits chatter was pure anonymous
prediction-posting with no linked news; KLAC's weakness reads as broad
semicap-sector sympathy, not a company-specific catalyst — flagged as
"no catalyst, price action only" per the standing rule, not surfaced as
a setup.

Also excluded on sight: PDD, XPEV, TUYA, NSSC, PICS, AAPG all report
earnings today (2026-08-24) per get_earnings_calendar — event risk,
out of scope regardless of any move.

Did NOT pull option chain data for BABA/AAOI at this hour — this repo
already learned (S7, 2026-08-20) that quotes/greeks don't refresh until
the 9:30am ET regular open, so anything pulled now would be stale
extended-hours numbers. Real gate-checking (mismatch_ratio, iv_hv_ratio,
delta floor, premium cap, no-chasing-an-already-printed-move) deferred
to the already-scheduled 7:00am ET "Premarket watch" and 9:35am ET "S7
options" triggers, which will re-verify with live data rather than
trust this premarket read — a premarket move can reverse by the open.
This entry exists so those triggers have a starting reference, not a
conclusion to just carry forward uncritically.

Also note: EMA fan-out backtest run tonight (S11, see strategies.md) --
tested negative, not usable as an entry filter for today's picks.

## 2026-08-24 ~7:20am ET — Premarket watch: watchlist rebuilt for the day

Trigger fired. Renamed "August 21" -> "August 24" (list
c15a7e55-bc55-4869-bf4f-6eb82a04c3e4).

**Dropped (5): ROST, HOOD, COIN, MSTR, BMNR.** All flat premarket this
morning (ROST +0.4%, HOOD -1.2%, MSTR +0.2%, BMNR +1.1%, COIN -0.8%) --
Friday's "BTC complex day 2, already extended" catalyst and ROST's
earnings pop are both fully digested over the weekend. No fresh
information today, so per the no-chasing-an-already-printed-move rule
these are out, not held over on inertia.

**Added (4), all with a real dated catalyst verified today:**
- PDD: reported Q2 this morning, EPS $2.85 actual vs $2.77 est (beat).
  +3.4% premarket.
- XPEV: reported Q2 this morning (EPS -0.19, no estimate given to
  compare). -3.1% premarket -- down despite reporting, likely a
  guidance/revenue read, not verified further at this hour.
- BABA: -2.2% premarket, continuation of the $10B Hong Kong equity
  offering / dilution story flagged at 2am -- still live, not faded.
- AAOI: -12.8% premarket (previous close $124.82 -> $108.90 as of this
  read), continuation of the equity-offering + margin-call chatter
  flagged at 2am -- the single biggest real move on the list.

**Checked and excluded:** SMCI (-2.9% premarket) -- Stocktwits chatter
is pure "red across the board" sector-sympathy noise alongside NVDA/AMD/
AVGO, no company-specific news found. TUYA/PICS/AAPG report PM today --
event risk, excluded regardless of any move (none currently moving
anyway). NSSC also reported this morning but wasn't a trending/notable
mover.

Time-sensitive note for the user: PDD, XPEV, NSSC already reported
before this check ran -- their earnings reactions are live catalysts
today, not scheduled events still pending. BABA and AAOI's moves are
now ~1 trading day old (first surfaced 2am premarket) but neither has
faded, so both stay live watchlist candidates. Full option-chain gate
check (mismatch_ratio/iv_hv_ratio/delta/premium cap) deferred to the
9:35am ET S7 trigger as planned -- quotes are still premarket/stale
here.

## 2026-08-24 ~9:40am ET — S7 daily screen: 9th/10th real checks, both rejected

Market open. Flat (no open S7 position). User had directly asked me to
find favorable option contracts today, on top of the standing 9:35am ET
trigger, so this run covers both.

**PDD and XPEV excluded before reaching the option chain.** Both
reported Q2 earnings this morning (PDD beat, +3.4%; XPEV -3.1% despite
reporting) -- the reaction already happened at the open. Buying either
now is chasing an already-printed move, not a real mismatch_ratio setup
(that track needs a catalyst still ahead, not one that already fired
and already got priced in). Rejected on rule 4, not run through the
chain math at all.

**AAOI** (9th real check): equity-offering/margin-call story, down
-17.5% by the open (accelerated from -12.8% premarket -- still live,
not faded). realized_volatility from 250 real daily closes: 157%
(20-day), 147% (60-day), 144% (90-day) -- already an extremely volatile
name before today. Checked real option quotes, 08-28 expiry (4 DTE):
  - $85p: mark $0.475, delta -0.071
  - $80p: mark $0.275, delta -0.041
  - $95p (much closer to ATM, current price $102.93): mark $2.20
    (**$220/contract, 4.4x the $50 cap**), delta -0.246 -- still short
    of the 0.30 floor even at 4.4x the allowed premium.
No strike clears both the $50 cap and the 0.30 delta floor -- same
structural conflict as BMNR (2026-08-20).

**BABA** (10th real check): $10B HK equity offering / dilution story,
-0.85% at the open (much of the premarket -2.2% faded by 9:38am --
already showing signs of the already-printed pattern too).
realized_volatility not separately needed once the delta problem showed
up: 08-28 $100p mark $0.02 (delta -0.007), $95p mark $0.01-0.26
range/illiquid (delta -0.003). Both essentially worthless-delta lottery
tickets at the cap. Not checked closer to ATM given AAOI's result
already proved the shape of the problem on a similarly-priced,
similarly-volatile name.

**Running total: 10/10 real checks rejected, 0 trades placed.** The
screen is doing exactly what it's designed to do on a $50/contract cap
against $100+ underlyings -- these two names were real, catalyst-backed,
still-live moves, and they still don't clear the gates. CLAUDE.md's S7
row updated with the running total.

## 2026-08-24 ~12:45pm ET — Direct request: screen for calls/puts, sell-put feasibility, watchlist cleanup

User directly asked me to screen for any option contract (buy calls or
sell puts), clean up the watchlist, and flag anything worth watching.

**Buying power check: $77.21 cash (account 432805174).** This
effectively rules out selling puts on any real-quality name -- a
cash-secured put needs strike x 100 in collateral, so even a $1 strike
needs $100, more than the account has. Not a policy question, a hard
capital constraint. Told the user plainly rather than screening for
something the account cannot execute.

**Re-checked PDD/BABA/XPEV/AAOI now that prices have moved since the
9:35am screen:**
- PDD: round-tripped from +3.4% premarket to -1.5% now ($87.06 vs
  $88.38 close) -- the whole earnings pop reversed. No longer notable.
- BABA: back to flat (+0.02%, $119.36 vs $119.34 close) -- the dilution
  dip fully round-tripped too.
- XPEV: still down -7.2% ($11.315), but real 5-min bars show it gapped
  down at the open then sat dead-flat in an $11.28-11.40 range for
  2.5+ hours, volume drying up from 300K+/bar to ~40K/bar. Checked its
  08-28 $11 put anyway out of thoroughness: mark $0.135 ($13.50/
  contract), delta -0.308 -- the FIRST contract all day to clear both
  the $50 cap and the 0.30 delta floor. Rejected anyway on rule 4 --
  the move is already fully printed and stalled, not a live edge, no
  matter how clean the numbers look.
- AAOI: bounced off its -17.5% intraday low back to -11.4% ($110.575),
  still the one name with a real ongoing catalyst, but the earlier
  09:40am chain check already showed the $50 cap can't reach a
  qualifying delta on this underlying at its price level.

**Watchlist cleanup ("August 24"):** removed PDD and BABA (both
round-tripped to flat, no longer live). Kept AAOI and XPEV as the two
still-real movers, flagged in the description that neither is a live
S7 buy today.

**Bottom line for the user:** nothing today clears every real gate for
a real reason. The XPEV near-miss is the closest anything has come, and
it's still a reject on the already-printed rule, not a close call worth
funding.

## 2026-08-24 ~12:47pm ET — BTG stop ratcheted mid-day, user-prompted

User noticed BTG running and asked directly to check/raise the sell
order, outside the normal 4pm ET scheduled check. Real intraday high
today: $5.7005 (5-min bars), a new peak over the $5.525 close that set
Friday's $4.53 stop. decide_stop_update(4.53, 5.7005) said ratchet:
new stop $4.6744, rounded to $4.67 (penny tick). Cancelled the $4.53
stop (verified state: cancelled), placed the new one -- this time the
market was open, so it went straight to state: confirmed and rests
live immediately, no next-open queuing like the two prior ratchets.
Third ratchet on this position, same mechanism (decide_stop_update,
18% trail) each time. CLAUDE.md's S9 row updated.

## 2026-08-24 ~12:49pm ET — BTG stop manually tightened to $5.50, user override

Two minutes after the systematic ratchet to $4.67, user said "let's
take the profit? maybe increase the sell order to $5.50?" -- an
explicit manual override of the 18% trail, not a decide_stop_update
output. Confirmed BTG's live quote first ($5.695, so $5.50 is a valid
stop below market). Cancelled the $4.67 stop (verified state:
cancelled), placed a new one at $5.50 (verified state: confirmed,
resting live). This locks in roughly +4.6% from the $5.26 average cost
as a floor, trading the systematic trail's wider room for a firmer
profit lock -- the user's explicit real-time call on their own
position, not a strategy change to S9 itself. CLAUDE.md's S9 row noted
this as a manual override, distinct from the mechanical ratchets.

## 2026-08-24 ~2:40pm ET — S9: BTG closed outright, +$35.69 (+8.0%)

User pushed back hard on the trailing-stop approach: sitting a stop
below a running price and waiting for a pullback to sell is backwards
when the goal is taking profit. Direct instruction: "take the profit.
scan, check, compare, buy/sell and take profit." Also corrected my
earlier framing -- the $4.67 ratchet WAS the stop sitting below a
rising price waiting for a reversal, and that's exactly the pattern
being pushed back on, even though it was later manually tightened to
$5.50 per their own request minutes after.

Executed: cancelled the resting $5.50 stop (verified state: cancelled),
sold all 85 shares via marketable limit at the live bid ($5.68), GFD,
regular_hours. Filled in full within 4 minutes, average $5.68, $0.02
fee. Realized profit: (5.68 - 5.2599) x 85 - 0.02 = **+$35.69 (+8.0%)**
on the $5.2599 average cost basis.

This closes the second growth-sleeve position (first, PLTR, was
reversed same-day on 08-18 after discovering fractional orders can't
carry a stop). BTG is now the first growth-sleeve trade to close with
a real, positive, deliberate exit rather than a reversal or a
stop-out. trades.csv row 13 updated with full close detail. CLAUDE.md's
S9 row updated: n=2, one reversed same-day, one closed +8.0%.

Account is now flat on the growth sleeve -- no open position. Next
step per the user's explicit direction ("scan, check, compare,
buy/sell"): treat finding the next position as active work, not
something to wait on. Will re-run the Growth Momentum scan
(2514847d-25cb-4628-9731-bb5b0ee7d246) live to see what real
candidates exist right now.

## 2026-08-24 ~2:50pm ET — S9: new position, LYFT (3 sh, $17.5779, stop $14.42)

Same afternoon BTG was closed, acted on the user's direct instruction
to keep finding the next opportunity rather than sit flat. Real
constraint: buying power was only $57.13 -- BTG's $482.78 sale
proceeds are unsettled (T+1, cash account), so this had to work within
the small settled-cash figure. Flagged the limited-margin upgrade path
to the user (eligible=true) as a permanent fix for this T+1 lag going
forward; not yet acted on.

Re-ran the Growth Momentum scan live (356 real matches, up from the
prior runs). Sorted by price, checked real fundamentals on 12
whole-share-affordable names: SNAP, RIG, PSKY, NXE, OWL, UEC, PATH,
LYFT, ARCC, CDE, AG, S. Most were unprofitable on a real PE basis
(SNAP -28.2, RIG -3.3, PSKY -18.3, NXE -35.6, UEC -58.3, S -22.2).
LYFT stood out: PE 2.44, unusually cheap for a name that's actually
profitable, with momentum already confirmed by the scan's own filters
(RSI 50-70, ADX>20, 1mo change >5%, market cap $6.65B).

Bought 3 whole shares at $17.5779 (marketable limit at the $17.58 ask,
filled immediately, no fee). Placed GTC stop_market at $14.42
(growth_signal.trailing_stop_price, 18% below entry) -- verified
state: confirmed within 8 seconds, resting live (market open). Third
growth-sleeve trade overall; first same-day rotation (close one
position, open the next, same afternoon) rather than a standalone
entry. trades.csv row 14, CLAUDE.md's S9 row updated to n=3.

## 2026-08-24 ~4:11pm ET — S9 daily stop check: LYFT ratcheted + resized, real gap caught

Scheduled trigger fired. Its stored instructions still referenced BTG
(closed earlier today) -- ran the real check against the actual
current position (LYFT) instead, and updated the trigger's own prompt
afterward so it stops drifting from reality.

Real intraday high since entry: $17.8698 (5-min bars). decide_stop_update(14.42,
17.8698) said ratchet to $14.6532 (rounded $14.65).

While doing this, get_equity_positions showed LYFT quantity=4, not the
3 the agent bought -- get_equity_orders confirmed a 4th share was
bought directly by the user (placed_agent: user, 2026-08-24T19:05:32Z,
$17.585), right around the time the agent explained buying power
couldn't cover another share. The resting $14.42 stop was still sized
for only 3 shares, meaning the 4th sat unprotected all afternoon until
this check caught it.

Cancelled the 3-share $14.42 stop, placed a new 4-share stop at $14.65
covering the full real position. Verified via get_equity_orders:
state: queued (market closed right as the order went in, same
next-open queuing pattern as every other post-close ratchet today, not
a rejection).

Updated the growth-sleeve trigger's own stored prompt (via
update_trigger) to explicitly check resting-stop quantity against real
position quantity every run, not just price -- the user trading
directly on this account is apparently a real, recurring thing, not a
one-off, so the standing check needs to catch it going forward rather
than relying on this session catching it by chance.

trades.csv row 14 and CLAUDE.md's S9 row both updated with the full
detail.

## 2026-08-25 ~7:21am ET — Premarket watch: watchlist rebuilt for the day

Trigger fired. Renamed "August 24" -> "August 25" (list
c15a7e55-bc55-4869-bf4f-6eb82a04c3e4).

**Kept: AAOI.** +4.8% premarket ($112.85 vs $107.63 close) -- bouncing
off yesterday's lows, the equity-offering/dilution story from earlier
this week is stabilizing rather than continuing to fall. Still the one
real, live name on the list.

**Dropped: XPEV.** Flat overnight (+0.9%), the earnings-reaction
catalyst from 08-24 has fully played out -- no longer notable.

**Added: OXY.** Real, sourced, sector-wide catalyst discovered earlier
this session (via direct user question, not the scanner): crude oil
extending its fall despite new US sanctions on Iran -- the market
"shrugging off" what would normally be a bullish supply-tightening
signal. Confirmed broad -- XOM, CVX, OXY, SLB, HAL, COP, DVN, APA all
down 0.6-2.0% premarket together, not one name. OXY picked as the
representative name (highest oil-price sensitivity of the group,
clearest mover at -2.0%).

**Checked and excluded:** AMIX -- real volatility (hit $16 after-hours,
now $7.40, already faded hard), but the only "catalyst" circulating is
retail chatter about an unverified "patent catalyst" and warrant
mechanics, no linked/sourced news article found. Sentiment on the name
is also split (some calling it a pumper, real disagreement in the
thread) -- not a clean, verifiable setup. DAIC, PMI, BTCT, LUCY, DXST,
SUGP, SDOT all checked via the scan, all lack a fresh catalyst beyond
"still moving."

No high-market-cap earnings scheduled today that overlap the current
watchlist names. ZM/NCNO/QFIN/BOX/HEI/SMTC report PM today -- noted,
none currently on the watchlist.

## 2026-08-25 ~9:40am ET — S7 daily screen: 11th/12th real checks, both rejected

Market open. Flat (no open S7 position). Checked today's watchlist:
AAOI and OXY.

**AAOI** (11th check): now $111.45, bouncing off yesterday's lows.
08-28 $100p: mark $125/contract (2.5x the cap), delta -0.168 -- worse
than yesterday's rejection, not better, despite the higher price. Same
structural wall.

**OXY** (12th check): real, fresh, sector-wide catalyst (oil extending
its fall despite new Iran sanctions, confirmed broad across 8 major
names yesterday). realized_volatility from real daily closes: 30.4%
(20d), 33.6% (60d) -- much calmer than AAOI, worth checking properly.
09-04 $58p: mark $48.50 (clears the cap), delta -0.241 (misses the
0.30 floor). 09-04 $59p: delta -0.463 (clears the floor with real
conviction), but mark $121.50 (2.4x the cap). IV ~33.5% vs realized
vol ~30-34% -- roughly fair pricing, not the deciding factor here; the
cap/delta conflict alone is enough to reject.

**Pattern now confirmed across four different underlyings** (BMNR
08-20, AAOI 08-24/08-25, BABA 08-24, now OXY): whenever the underlying
trades much above ~$50-60/share, the $50/contract premium cap and the
0.30 delta floor are structurally incompatible -- no strike satisfies
both regardless of how good the catalyst is. This isn't a screening
failure, it's a real, repeatedly-confirmed fact about what this cap
can reach. Running total: 12/12 rejected, 0 trades.

CLAUDE.md's S7 row updated with the running total and pattern note.

### 2026-08-25 ~4:04pm ET -- S9 daily stop check, LYFT ratchet
Position verified: 4 sh, avg $17.58, resting stop $14.65 covered all 4 shares
(quantity check passed, no gap this cycle). Real intraday high today (5-min
bars) was $17.97, a new peak over yesterday's $17.8698 -- `decide_stop_update`
said ratchet. Cancelled the $14.65 stop (verified `state: cancelled`), placed
$14.74 (18% below $17.97, verified resting/queued not rejected). Order landed
4 minutes after the 4pm close, so it shows `state: queued` for next-open --
same as the 08-24 precedent, not a problem.

### 2026-08-25 ~10:55pm ET -- S9 fourth position, SMCI (order placed, pending fill)
User: "you have more money to spend so go for options stock and anything
that you can hunt" -- real settled buying power $489.67 (confirmed via
get_portfolio, unsettled_funds $0). Market closed (10:55pm ET), so this is
a queued entry for tomorrow's 9:30am open, not a live fill tonight.

Re-ran the Growth Momentum scan live (2514847d-25cb-4628-9731-bb5b0ee7d246,
360 real matches). Filtered to whole-share-affordable (<$60), liquid
(avg vol >500k) names, sorted by 1-month change: mostly silver/gold miners
(HL, CDE, AG, HBM) and uranium (UEC) riding a real sector rally (matches
the CCJ/UUUU/OKLO story from earlier today), plus SMCI, SNAP, ZETA, GTLB.
Checked real fundamentals on 7: SNAP (PE -31.8), UEC (PE -60.7), ZETA
(PE -2020), GTLB (PE -278.7) all unprofitable -- same pattern as every
prior growth pick. SMCI stood out: PE 10.79 (cheap for +35.8% 1mo),
RSI 55 (not yet overbought, unlike the 65-70 RSI mining names), ADX 25.2,
$66.9M avg volume, still well off its 52wk high ($58.78 vs $38.57 now).
HL/CDE also real and profitable (PE 26/17) but more extended (RSI 66-67).

Placed: BUY 12 sh SMCI, limit $39.50 (above tonight's $38.57 close, price
protection against an overnight gap), regular_hours, gfd. Verified state:
queued (not rejected -- market closed, this is the expected next-open
queuing behavior, same as every stop order placed after 4pm this week).
Scheduled a check for ~9:31am ET tomorrow (trig_01RA1izVEShePzEdWd5t9ETh)
to verify the real fill and place the initial 18% GTC stop immediately,
per the fractional-share/unprotected-position lessons from PLTR and the
Rule Zero standard of never assuming a queued order becomes a real fill.

Also raised the S7 options premium cap $50 -> $150/contract this same
session per direct user instruction (see CLAUDE.md's S7 row and
strategies.md's Governing rules section for the full record).

### 2026-08-26 ~2:15am ET -- Watchlist rebuild: "August 25" closed, "August 26" created
User asked for a fresh watchlist after screening the market, moving over
anything from "August 25" that's still good. Real research, not a coin
flip on which to keep:

**CCJ/UUUU/OKLO (uranium/nuclear)** -- carried forward. All three closed
higher than their mid-day levels yesterday (CCJ $106.96 vs $107.39
intraday, UUUU $15.97 vs $16.04, OKLO $44.27 vs $44.13) -- the sector
rally kept running overnight into premarket (CCJ #4 on Stocktwits
trending, +0.27% in the overnight/premarket session). No pullback
materialized yet, but the thesis is intact and real, not stale.

**AAOI dropped** -- real, fresh, specific risk found on the tape tonight
(2-3 posts within the last ~3 hours): "AAOI is the company desperate to
raise money", explicit speculation about an imminent dilutive secondary
offering, with a cited historical precedent (an unrelated company's
50->24 offering-driven crash in 3-4 days used as the cautionary
comparison). Real bullish catalyst also present (potential FCC ban on
Chinese optical transceivers, AI datacenter demand) but the acute
dilution risk right now outweighs it for a "still good" call.

**OXY dropped** -- real bearish technical (a trader's "head and shoulders
on the one week" call) plus a sourced negative-impact article ("oil
extends fall as investors shrug off latest US sanctions on Iran", 79%
confidence negative for OXY) confirm the original bounce thesis has
turned; Stocktwits' own sentiment score flipped to BEARISH (26/100)
despite bullish-leaning post volume. No longer a clean setup.

**New adds, from Robinhood's own "Building Momentum Candidates" scan**
(8083a928-4c3c-4dfe-915c-66b6d89a490b: RSI>55, ADX>25, MACD>0, vol >1M,
price $1-50), filtered to market cap >$2B and checked against real
fundamentals:
- RRC (Range Resources): PE 11.38, profitable, real ~0.9% dividend,
  mid-range of its 52wk band ($32.68-$48.31 vs $40.50 now), RSI 59.7/
  ADX 25.1/MACD +0.35 -- real natural-gas E&P momentum, ties into the
  same energy-sector thread as OXY/CCJ this week.
- ET (Energy Transfer): PE 14.44, profitable, real 6.3% dividend, large
  ($72B cap), at a fresh 52-week high ($21.64 on 08-19). RSI 59.5/
  ADX 31.4/MACD +0.16.
- ACAD (Acadia Pharmaceuticals): PE 13.35, profitable, real biotech at a
  fresh 52-week high ($30.96 on 08-19). RSI 67.9/ADX 42.4/MACD +0.60.
Ruled out from the same scan on real negative PE: CRGY (-315.7), and
SONY's headline PE (-102.9, likely a one-time charge on an otherwise
real/profitable business) was flagged as not a clean value story either
way. VERA (real overnight pop, Stocktwits trending #7) also unprofitable
(PE -6.0) -- skipped on the same standing rule.

**Flag for the live SMCI position (not part of this watchlist task):**
the AAOI research surfaced a real historical pattern worth watching on
our own SMCI holding -- a Stocktwits post cited SMCI's own June dilutive
offering (~$50 -> $27.50/share offering price, stock fell 50->24 in 3-4
days) as the cautionary precedent for AAOI. Real, dated history on the
same company we now hold 12 shares of. No current offering rumor found
on SMCI itself tonight, but worth a periodic real check (get_stock_news /
Stocktwits) rather than assuming it can't recur.

Result: "August 25" emptied and marked closed/superseded (list_id
c15a7e55-bc55-4869-bf4f-6eb82a04c3e4). "August 26" created (list_id
28897739-a4e8-40fa-ac57-6fb0eb30137b): CCJ, UUUU, OKLO, RRC, ET, ACAD.

### 2026-08-26 ~7:30am ET -- Premarket watch (scheduled trigger)
No separate dated day-trade list exists right now -- "August 25" was
closed and superseded by "August 26" a few hours ago per the user's own
request. Treating "August 26" as today's one list rather than creating a
naming collision; added this cycle's real premarket findings into it.

Real premarket movers checked (Stocktwits trending + Robinhood's "Daily
Movers - Fastest Growers" scan): INTU -10.7% (real, dated catalyst --
FY26 beat but FY27 guidance disappointed, multiple analyst PT cuts same
morning: Morgan Stanley 335->315, Goldman 500+->276, Truist 410->350) --
already-printed reaction, informational only, not added. ZM -6.8%
premarket, not investigated further (no position/thesis overlap). NVDA
flat premarket but reports Q2 earnings AFTER CLOSE TODAY -- real, large,
market-wide event; noted for awareness, not actionable for any current
position.

Two real additions, both independently cross-confirming the live
uranium/nuclear theme already on the list (CCJ/UUUU/OKLO):
- SMR (NuScale Power): real premarket move (+3.16%), a Stocktwits post
  explicitly grouped $OKLO $SMR $CCJ $UUUU together this morning. Real
  technical setup (RSI 53.7 neutral, MACD bullish, broke above the $9.89
  resistance level, volume above average). Same early-stage/unprofitable
  profile as OKLO (PE -4.31) -- tracked as thematic/sector momentum, not
  a value pick, same basis OKLO was already being tracked on.
- LEU (Centrus Energy): surfaced independently in the real quality-
  momentum scan (RSI 56.6, ADX 17.5 -- weaker trend signal than the
  others). Different link in the nuclear value chain (fuel enrichment/
  services, not mining or reactor-building) -- real diversification
  within the theme. Profitable but expensive (PE 80.8), 52wk range
  $142-$464 vs $195.80 now.

"August 26" now: CCJ, UUUU, OKLO, SMR, LEU, RRC, ET, ACAD.

### 2026-08-26 ~9:36am ET -- S9: SMCI fill verified, initial stop placed
Scheduled follow-up from last night's queued buy fired at market open.
Verified via get_equity_orders: filled 12 sh @ $38.00 (average_price),
09:30:00.095 ET -- better than the $39.50 ceiling, real confirmation of
how a limit buy actually works (ceiling, not target). Computed
growth_signal.trailing_stop_price(38.00) = $31.16, placed GTC
stop_market, verified state: confirmed (resting, not rejected) 98
seconds after the fill. Logged to trades.csv row 15 and CLAUDE.md's S9
row. Fourth growth-sleeve position, second currently open (alongside
LYFT).

### 2026-08-26 ~4:03pm ET -- S9 daily stop check, LYFT holds, SMCI ratchets
LYFT: real position 4 sh, stop $14.74 covers all 4 (quantity check passed).
Today's real high ($17.80, 5-min bars) didn't exceed the existing peak
($17.97 from 08-25), so decide_stop_update correctly said no change.

SMCI: real position 12 sh, stop $31.16 covered all 12 (quantity check
passed -- no manual-buy gap this time). Today's real high since entry
was $38.27 (11:40am ET) -- decide_stop_update said ratchet. Cancelled
$31.16 (verified state: cancelled), placed $31.38 (18% below $38.27).
Order landed 3.5 min after the 4pm close -- state: queued, next-open,
not a rejection.

Real, separate finding while checking positions: the user bought 1 share
of SMR directly on the account this morning (~8:30am ET, $10.00,
placed_agent: user) -- SMR is one of the names added to the "August 26"
watchlist during the premarket check. This share is outside S9's scope
(not picked via the growth scan, not an agent order) and currently has
NO resting stop. Flagged to the user directly rather than silently
adding it to growth-sleeve tracking or leaving it unmentioned.

### 2026-08-27 ~12:20am ET -- Watchlist schedule fixed; XPON added after a real miss
User asked for a standing daily schedule: new dated watchlist every
trading day, previous day's list closed out by moving/removing names,
done before 7am. This mechanism already existed (the "Premarket watch"
trigger, trig_01QgTDVhFfLA6ZpAvrLYactt) but had two real gaps, both
fixed tonight:

1. **Timing.** Cron was `0 11 * * 1-5` (7:00am ET) but the real fire
   yesterday landed at 11:25:49 UTC (7:25am ET) -- ~25 min of real
   drift, after the user's 7am deadline. Moved to `30 10 * * 1-5`
   (6:30am ET) to build in buffer.
2. **Coverage blind spot -- the actual cause of missing XPON.** The
   trigger only looked for a fresh, dated catalyst (news/earnings) each
   morning. XPON had no single new press release today -- it was
   already flagged and tracked informally starting 2026-08-24 (real
   dilution/offering unwind), then kept posting genuine, large moves on
   08-25 and 08-26 without one new headline. Real result: XPON hit
   $11.76 today (from a real ~$5.15-5.45 support base cited by multiple
   independent Stocktwits traders), message volume EXTREMELY_HIGH
   (score 97), and it's on several different traders' own posted "watch
   Thursday" lists right now. My own hourly momentum checks this week
   saw XPON's price ($6-9 range) but never caught the full move because
   each cycle re-tested only "is this near its OWN highest point in the
   last hour" -- a real, sustained multi-day mover with heavy chatter
   was never given credit for being real just because it lacked a fresh
   single-day catalyst. Rewrote the trigger's prompt to explicitly treat
   "sustained real momentum + heavy real chatter across days" as a valid
   watchlist inclusion basis, separate from the fresh-catalyst screen.

Real action taken tonight: renamed "August 26" -> "August 27" (list_id
28897739-a4e8-40fa-ac57-6fb0eb30137b), added XPON. Kept CCJ/UUUU/OKLO/
SMR/LEU/RRC/ET/ACAD as-is (no new reason to drop any tonight; the
6:30am run will re-check all of them with fresh data). Tomorrow's
6:30am ET run is the first live test of both fixes.

### 2026-08-27 ~6:35am ET -- Premarket watch (first run under the new schedule/rules)
Fired 5 min after its new 6:30am ET target (real improvement over
yesterday's 25min drift). "August 27" already existed (built ad hoc the
prior night); no rename needed, treated as today's list per the
merge rule.

Real premarket movers (Stocktwits trending): NVDA +6.8% ($209.66->$224.01),
CRM +11.4% ($205.62->$229.01), CRWD +9.3% ($189.18->$206.70) -- all real,
dated: NVDA/CRM/CRWD all reported earnings after 2026-08-26's close per
the earnings calendar, and all three show genuine premarket follow-
through, not just an after-hours print. Added all three.

Kept the rest of the list unchanged (CCJ/UUUU/OKLO/SMR/LEU/RRC/ET/ACAD/
XPON) without re-verifying each individually this cycle -- explicit
token-conservation instruction from the user, real re-checks resume as
normal going forward.

## 2026-08-28 (~1:30am ET) — PPCB miss, root cause, and two real fixes

User flagged missing PPCB's real move on 2026-08-27. Reconstructed from
real data (get_equity_historicals hourly bars, get_stock_news,
get_symbol_messages): PPCB had a real, dated catalyst -- positive
preclinical pancreatic-cancer data (PRP showed >90% tumor growth
inhibition), Stocklake headline published ~10:36am ET -- and gapped from
a ~$1.07 prior close to open $4.22, peak $4.35, right at the 9:30am
open. By the time the momentum-scanner trigger's OLD window even started
(10:00am ET), PPCB was already down to ~$2.60-2.74 -- the ignition
itself happened entirely outside the scan's coverage window, not a
catalyst-detection failure. This was NOT random chatter/pump -- a real
headline existed and should have been checked once the price move was
seen, but by then it read as "already faded" and got skipped per the
old rule.

Two real fixes shipped same session:
1. Momentum-scanner trigger (trig_011uqSeqdqMoS3e5ZUTk13jN): window
   widened from 10am-4pm ET to 9am-4pm ET (hourly is the platform's
   confirmed minimum interval -- 30-min was tried and rejected with an
   explicit error). Also made the "already faded" rule time-aware (a
   high made <15-20min ago is still igniting, not stale) and added a
   standing instruction to always check the single biggest mover's
   catalyst each cycle regardless of fade status, logging a one-line
   note here even when it's not alert-worthy, so a real catalyst is
   never silently dropped from the record again.
2. Ignition Board artifact: catalyst lookup was 100% manual-click
   (Stocklake 25/day guest cap). Now auto-fires for any row clearing 3+
   of the 4 real numeric pillars, capped at 15 auto-lookups per page
   load so manual clicks and other Stocklake use keep headroom. Also
   fixed a separate real bug found live the same session: Robinhood's
   own scan RVOL field is broken outside regular hours (flat placeholder
   of 1x, or spikes into the thousands off a near-zero off-hours
   denominator) -- the RVOL pillar is now excluded from scoring outside
   9:30am-4:00pm ET instead of firing off garbage numbers.

## 2026-08-28 (~7:12am ET) — Momentum scan, first fire under new 7am schedule

Top real mover: AEMD +50% premarket ($2.17 -> $3.25), real volume
16.5M vs 30-day average 778K (21x). No catalyst -- confirmed directly
via Stocktwits chatter: "AEMD - low float/getting volume - but no
news - float under 1M" (685K float). Pure low-float squeeze, not a
dated-catalyst setup. No alert sent (fails the catalyst gate).

Also confirmed live: get_equity_historicals returns ZERO bars for
today's session this early (~7:11am ET), even for an actively-moving
stock -- a real data-availability gap, not specific to this symbol.
Ignition Board's self-computed RVOL got a fallback for this (30-day
average volume comparison) same session.

## 2026-08-28 (evening) — SPY/QQQ: what actually moved the market this week

Real data (get_equity_historicals daily bars + get_equity_news, both symbols):

**Thursday 2026-08-27 (the up day):** SPY +0.8% to 7,734.44, QQQ (Nasdaq
100) +0.9% to ~29,500 -- NVDA's best day since April 2025, +9%, on
guidance for ~70% revenue growth next fiscal year. Real, single dominant
catalyst. Cybersecurity names melted up alongside it on agentic-AI demand
optimism (CRM/CRWD both up double digits, already logged separately).
Technology (XLK +2.9%) was the ONLY green S&P sector of 11 -- a narrow,
tech-only rally, confirmed by real fund flow: $3.8B out of SPY / $3.7B
into QQQ the same day (a real rotation, not broad buying). Backdrop:
hawkish-leaning data already out that morning (jobless claims below
forecast, wholesale inventories up more than expected, KC Fed
manufacturing index at its highest since April 2022) -- bond yields held
steady ahead of Friday's main event.

**Friday 2026-08-28 (the reversal):** Fed Chair Kevin Warsh's FIRST
Jackson Hole speech as chair (real, dated, scheduled event) came in
hawkish: "this summer's inflation data is better than expected, but do
not tell me underlying trends have meaningfully improved" -- dismissed
the encouraging inflation prints, said financial conditions aren't
restrictive and the labor market is at full employment. Real market
reaction: September rate-hike odds jumped to 60% from ~35% pre-speech
(CME FedWatch). 2-year yield +10bp to 4.34%, 10-year +4bp to 4.72%
(intraday touched 4.7%), 30-year flat at 5.20% -- a front-end-led
flattening, consistent with the market pricing a tighter Fed rather than
inflation/term-premium fear. Nasdaq 100 fell ~1% to 29,359, giving back
a chunk of Thursday's NVDA-powered rally; S&P 500 nearly flat (-0.1%) at
7,721. Gold -2.0% to $4,509, silver -2.2% to $67.75, Bitcoin -2%+ toward
$78K -- real risk-off move in alternative assets too. Also that morning:
Univ. of Michigan consumer sentiment revised up to 51.7 but still down
~6% from July; BLS revised payrolls (year through March 2026) down
79,000, a much smaller haircut than last year's 911,000 revision.

**On the "Trump" angle specifically:** no explicit Trump-administration
headline (tariffs, shutdown, etc.) appeared in either symbol's real news
feed this week. The real Trump connection is Kevin Warsh himself --
Trump has publicly pushed for Warsh as Fed Chair in real life, and this
was literally his first Jackson Hole speech in that seat. That's the
government/Fed linkage, not a separate policy headline.

Net read: the week's real move was NVDA-earnings-driven (narrow, tech-
only) up through Thursday, reversed Friday by a real, dated, hawkish Fed
speech -- not a broad economic or Trump-policy story beyond Warsh's own
appointment.

## 2026-08-30 -- SPY/QQQ: real 4-week catalyst-annotated high/low walk (07/31-08/28)

User asked for a table of the last 4 weeks' significant highs/lows with
the real catalyst behind each, "not every high and low" -- so this filters
to the moves that were actually catalyst-driven, not daily noise. Method:
real daily OHLC bars (get_equity_historicals, day interval, both symbols)
plus three full pages of real dated headlines (get_equity_news, both
symbols, paginated back to 07/29). Every number below is a real close or
intraday high/low from those bars -- nothing estimated.

**The one surprise re-deriving this fresh turned up:** the single LOWEST
close of the whole 4-week window for both SPY (747.03) and QQQ (687.99) is
right at the START of the period (07/31), not during the mid/late-month
pullbacks -- those only ever cooled the rally back to the high 760s/low
710s, well above the 07/31 base. The single HIGHEST close for both is
08/13 (SPY 777.88, QQQ 732.07). Worth saying plainly: the popular
narrative of "up then a big selloff" undersells it -- this was net a
one-way month (SPY +3.0%, QQQ +4.1% top-to-tail, 07/31 close to 08/28
close) with two real but shallow pullbacks along the way.

| Date(s) | SPY | QQQ | Move | Real catalyst |
|---|---|---|---|---|
| Fri 07/31 | close $747.03 (period low) | close $687.99 (period low) | -- | AMZN earnings beat offsets Apple weakness; market's footing the day after the 07/29 FOMC meeting. |
| Mon 08/03 - Tue 08/04 | close $771.33 | close $723.85 | SPY +3.25%, QQQ +5.21% in 2 sessions | US-Iran truce hopes, then Strait of Hormuz reopening hopes -- oil-supply-risk premium unwinding, tech-led. |
| Wed 08/05 - Thu 08/06 | intraday low $767.46 | gapped -0.9% at 08/06 open | shallow, single-sector dip | SanDisk/Western Digital earnings disappoint, SK Hynix "flash crash" -- chip-sector-specific, not broad. |
| Fri 08/07 | close $773.26 | close $723.03 | SPY +0.61%, QQQ +1.17% | July nonfarm payrolls unexpectedly CONTRACTED -- market rallied anyway on rate-cut hope ("bad news is good news"). |
| Wed 08/12 - Thu 08/13 | close $777.88 (period high) | close $732.07 (period high) | SPY +4.13%, QQQ +6.41% from the 07/31 low | Two straight cool inflation prints: July CPI in-line, then July PPI unchanged/below expectations -- market priced a more dovish Fed. |
| Fri 08/14 | -- | -- | -- | "The Warsh rate-hike trade collapses" -- September hike odds fell to ~30% by 08/17, a dovish repricing that let the market coast near its highs. |
| Tue 08/18 - Thu 08/20 | close $762.60 (-1.96% from the high) | close $710.93 (-2.89% from the high) | real but shallow pullback | Trump rejects extending the Iran ceasefire (08/18) -> "no talks" with Iran (08/19) -> Trump launches "Operation Economic Fury" on Iran (08/20), stacked with AI-bubble-fear commentary (Ray Dalio: 1929/2000 comparison; JPMorgan's Bill Eigen: 2008-crash warning). |
| Mon 08/24 | close $763.47 | close $706.32 (period's 2nd-lowest close) | QQQ -0.65% from 08/20 | Samsung semiconductor-stock crash triggers chip-sector selling ahead of NVDA earnings, plus Bessent launches "Economic D-Day" sanctions escalation against Iran. |
| Tue 08/25 | close $765.91 | close $710.72 | -- | Bessent expands Iran sanctions further, yet oil fell anyway ("toughest sanctions on record sent oil lower, not higher") -- a real "market shrugs off the headline" moment (also logged separately re: OXY). |
| Thu 08/27 | close $771.10 | close $721.11 | SPY +0.66%, QQQ +1.37% | NVDA's best day since April 2025 (+9%), guided ~70% revenue growth -- but narrow: real fund flow shows $3.8B OUT of SPY, $3.7B INTO QQQ same day (rotation, not broad buying); tech (XLK) was the only green S&P sector of 11. |
| Fri 08/28 | intraday high $775.30 (2nd-highest of the period), closed $769.35 | closed $716.43 | SPY -0.23%, QQQ -0.65% from 08/27's close | Fed Chair Kevin Warsh's first Jackson Hole speech as chair came in hawkish; September rate-hike odds jumped from ~35% to 60% (CME FedWatch); gave back a chunk of Thursday's NVDA rally. Already filed 2026-08-28 (see above). |

Filed alongside the Ignition Board's professional redesign this same
session (qualified-at timestamps, live candlestick charts, candlestick-
reading education panel) -- the 08/28 shooting-star-shaped candle (spike
to $775.30 intraday, closed near the day's low at $769.35) is a live,
real example of exactly the pattern the new education panel teaches.

## 2026-08-31 ~6:35am ET -- Premarket watch: watchlist rebuilt for the day

Trigger fired. Renamed "August 28" -> "August 31" (list
28897739-a4e8-40fa-ac57-6fb0eb30137b). Very quiet premarket overall
(6:35am ET, well before the 7am+ window the user flagged as when most
real moves happen) -- checked Early Momentum Ignition, Warrior Trading
Style, Daily Movers - Fastest Growers, and Daily gainers scans plus
Stocktwits trending, all cross-checked against get_equity_quotes.

**Dropped: the whole 08/27-PM earnings-reaction cluster** (IREN, RBRK,
AFRM, MRVL, PYPL, CRWD, CRM, NVDA) -- verified via get_equity_quotes all
are flat (within ~1%) vs Friday's close, 3 days after their earnings
reactions; fully priced in, no edge left for a day-trade list.

**Dropped: XPON** -- real activity still present (8.1M volume) but now
-3.6% and cooling, not the breakout mover it was on 08/27-28; multi-day
run has played out.

**Kept: the nuclear/growth core** (LEU, SMR, ACAD, ET, RRC, OKLO, UUUU,
CCJ) -- no bearish news found, thesis intact, same as every prior day
this week.

**Added, all real and dated (Benzinga premarket-movers article,
2026-08-31 04:53am ET, cross-checked against the scan data):**
- **NCRA** (Nocera) +21.7% premarket to $2.30 -- real, clean catalyst: a
  binding term sheet with INERGX Energy to form a 50/50 joint venture.
- **AEHL** (Antelope Enterprise) +73.5% premarket to $6.14 -- real but
  risky: this is a mechanical bounce off Friday's 30% dilution-driven
  crash (an $18.99M private placement, 15M shares at $1.266). Flagged as
  volatile chop, not a clean directional setup.
- **WETO** (Wetour Robotics) +25% premarket to $7.15 -- same pattern as
  AEHL: real catalyst is a $75M share-sale agreement with Rodman &
  Renshaw (dilutive), and its last week of prints ($15 -> $8.92 -> $10.81
  -> crash -> bounce) is pure whipsaw, not trend. Same risk flag.
- **ELMT** (The Elmet Group) +10.5% premarket to $18.39 -- real catalyst:
  better-than-expected quarterly results, distinguishing it from AEHL/
  WETO's dilution-bounce pattern. Largest/most stable name of the four
  adds ($509M market cap vs. single-digit-to-low-double-digit millions
  for the others).

No high-market-cap earnings today overlapping the watchlist (SAIC
reports am today, not on any list; PANW/DELL/MDB/CRDO/NIO report
tomorrow 09/01).

## 2026-08-31 ~7:10am ET -- Momentum scanner alert: 7am cycle, 4 names

First hourly cycle of the day (7am-4pm ET job). Early Momentum Ignition
(84 matches) and Warrior Trading Style scans both run; regular-hours
bounds returned zero bars for today (expected, market not open until
9:30am) so RVOL was self-computed from EXTENDED-hours 5-minute bars
(today's premarket volume-so-far vs. the same time-of-day on the one
prior day with comparable premarket data) instead of trusting Robinhood's
own Relative volume field.

**AEHL** $6.46, +80% vs Friday's close, self-computed RVOL ~22,100x
(premarket volume already 2.66M vs. a ~120-share same-time baseline --
directionally enormous, but the baseline sample is thin, 1 prior day).
Real catalyst already logged this morning: mechanical bounce off
Friday's dilution-driven crash. ~10% off today's premarket high ($7.18),
made within the last few minutes.

**NCRA** $2.67, +41% vs Friday's close. Real volume 3.15M shares already
premarket -- more than 2x its entire 1.35M float has already turned over.
No prior-day premarket baseline exists to compute a clean RVOL ratio, but
that turnover alone is real and extreme. Real, clean catalyst: binding
JV term sheet with INERGX Energy (logged this morning). ~11% off today's
premarket high ($2.98).

**WETO** $7.05-7.30, +26% vs Friday's close, self-computed RVOL ~5.5x.
Real catalyst: $75M dilutive share-sale agreement (logged this morning).
~8-11% off today's premarket high ($7.90).

**BRNX** $4.48, +15% vs Friday's close, self-computed RVOL ~5.4x. NO
DATED CATALYST FOUND -- Stocktwits shows EXTREMELY_HIGH message volume
and EXTREMELY_BULLISH sentiment (94.7% bull), but the actual posts are
pure speculation/chatter ("expected to see 7-8 today", short-squeeze
claims), including one trader noting "shorting all the pumps on this has
been a winning strategy. It always dumps." Flagged explicitly as price
action only, not a clean setup.

Messaged the user with all 4 (including BRNX's caveat) since AEHL/NCRA/
WETO already clear every bar and BRNX's real, extreme message volume
made it worth surfacing with the warning attached rather than silently
dropping it.

## 2026-08-31 ~8:05am ET -- Momentum scanner alert: re-scan, one new name (XAIR)

User asked to re-scan ~1 hour after the 7am cycle. Re-ran both scans.

**AEHL, NCRA, WETO, BRNX** (all alerted last cycle): none made a new
high since -- AEHL rolled over hard (was $6.46/+80% at 7:10am, now
$5.86/+66%, ~18% off its premarket high of $7.18); NCRA faded the most,
down from $2.67-2.77/+41-46% to $2.25-2.26/+19%, a real ~24% pullback
off its $2.98 high -- squarely the "already printed, faded off the high"
case the job excludes, not re-alerted. WETO and BRNX roughly flat, no
material change. Per the job's own rule (skip unless materially
changed), none were re-alerted.

**XAIR (Beyond Air) -- new, real catalyst, alerted.** +34% to $5.87-5.97
(Stocktwits real-time price + get_equity_quotes bid/ask both confirm;
Friday close $4.48). Real, clean, dated catalyst quoted directly in
Stocktwits posts and corroborated independently: "Beyond Air Receives
FDA Breakthrough Device Designation for LungFit GO to Treat
Nontuberculous Mycobacterial Pulmonary Disease (NTM-PD)." Float ~700K
(tight). Message volume EXTREMELY_HIGH, sentiment 93% bullish.

Note on data quality: get_equity_historicals for XAIR returned almost
entirely interpolated (flat, zero-volume) bars for today even as of
8:04am ET -- a real ingestion lag on this symbol specifically (the same
known issue documented for AEMD 08-28), not a broken move. Real price
was independently confirmed via get_equity_quotes and Stocktwits' own
live feed, both agreeing on ~$5.87-5.97, so this was not treated as
unverified -- but no self-computed RVOL number could be produced from
historicals for this one; said so rather than guessing a figure.

## 2026-08-31 ~8:10am ET -- Momentum scanner alert: standing 8am cycle, XAIR continuation

Standing hourly trigger fired (its own 8am cycle, ~5 min after the
user's manual "scan again"). AEHL ($6.00, +69.5%), WETO ($7.29, +27.5%),
BRNX ($4.45, +14.4%), MODD ($3.69, +6.6%) all roughly unchanged or
fading further -- no material change, not re-alerted.

**XAIR materially changed: real continuation, not just noise.** $5.87-
5.97 five minutes ago -> $6.01-6.07 now (get_equity_quotes confirms,
12:10:50 UTC), +34-35% vs Friday's $4.48 close. Same catalyst as before
(FDA Breakthrough Device Designation for LungFit GO). Told the user
briefly rather than staying silent, since this is exactly the "still
igniting, not already printed" case the job is meant to catch.

## 2026-08-31 ~9:10am ET -- Momentum scanner alert: 9am cycle -- XAIR fully reverses, AEHL fresh high

**XAIR round-tripped completely.** Peaked $6.01-6.07 at 8:10am (real, FDA
Breakthrough Device Designation catalyst); by 9:10am it's back to
$4.58-4.59, essentially Friday's $4.48 close (+2.2% only) -- the entire
+34% move gave back in under an hour. A real, clean example of exactly
the risk the standing reminder warns about (trades held past 5 minutes
net negative in the user's own history): the catalyst was real and the
early move was real, but chasing it an hour in would have meant buying
the top. Logged for the record, not re-alerted (no longer clears the
bar -- fully faded, catalyst already priced out).

**AEHL made a fresh high, materially changed since the 8:10am note.**
$6.00-6.07 at 8:10am -> $6.56-6.58 now (get_equity_quotes, 13:10:41 UTC),
a real ~9% continuation, back above its earlier $7.18 high's approach
range. Same catalyst as logged this morning (mechanical bounce off
Friday's dilution crash). Notably dropped OUT of the Early Momentum
Ignition scan's results this cycle even as price climbed -- Robinhood's
own Relative volume (1, 1H) field for AEHL has read a static
3.677398522899389 across all three checks this morning (7:10, 8:10,
9:10am), which looks stuck/stale rather than tracking the real
continuation; flagged here rather than trusted at face value, consistent
with the standing distrust of that field before 9:30am.

WETO ($7.01, +22.5%, fading from its $7.90 high), BRNX ($4.51, +15.9%,
flat), MODD ($3.59, +3.8%, further fading) -- no material change, not
re-alerted.

## 2026-08-31 ~9:36am ET -- Pre-open watchlist rectify + S7 daily screen (13/13 rejected)

**Part A, watchlist rectify (list 28897739..., "August 31"):** real
quotes on all 12 names since the 6:30am build. Nuclear/growth core (LEU,
SMR, ACAD, ET, RRC, OKLO, UUUU, CCJ) flat, no material change. NCRA
($2.42, +28%), AEHL ($6.49, +83%) still real and live. **WETO hit a
fresh high** ($7.90, +38%, up from $7.01 25 min earlier). **Dropped
ELMT**: its premarket earnings-beat pop (+10.5%) fully round-tripped to
flat/-0.4% by 9:36am -- no edge left for a day-trade list. Checked
Stocktwits trending for anything new: MOVE (Movano) was real (+10.8%,
3.9M volume) but had already faded hard from a $17.18 intraday high to
$12.73 -- the "already printed" case, not added.

**Part B, S7 options screen. Flat (no open position), ran the
dated-catalyst track.** get_earnings_calendar (high-market-cap,
next 3 days): only SAIC reports today, and it already reported this
AM (real EPS beat, $3.01 vs $2.30 est, stock +6.7% premarket) -- the
mismatch_ratio methodology is built for BEFORE a report (comparing
priced-in IV move to history), not chasing an already-realized gap, so
SAIC wasn't a fit for this track today. Real upcoming reporters (09-01,
09-02): PANW/DELL/MDB/CRDO/SNOW/AVGO/FIVE/NTAP all trade well above the
confirmed ~$50-60 cap/delta danger zone (BMNR/AAOI/BABA/OXY pattern) --
skipped without spending calls on them. Checked the two price-eligible
ones:

- **NIO** ($4.40, reports 09-01 AM): 6 real historical earnings-day
  moves (get_equity_historicals, 2025-03 through 2026-05) -- median
  absolute move 3.74%. ATM ($4.50) straddle for the 09-04 expiry:
  call mid $0.165, put mid $0.26, IV ~110%. Expected move 8.2%
  (straddle) to 11.5% (IV formula) -- mismatch_ratio 2.20-3.09 vs the
  0.85 cap. **Rejected: options price 2-3x more movement than NIO's own
  earnings history justifies** -- rich, not cheap. (Premium $16.50-26/ct
  and delta 0.45-0.55 both would have cleared the $150/0.30 gates --
  this rejection is purely a pricing call, not a structural cap
  conflict.)
- **GTLB** ($45.13, reports 09-01 PM): 6 real historical moves
  (2025-03 through 2026-06) -- median 8.975%. ATM ($45) straddle for
  09-04: call mid $3.45 ($345/ct), put mid $3.525 ($352.50/ct), IV
  173-187%. **Rejected on premium alone** (both legs >2.3x the $150
  cap) **and on mismatch_ratio** (1.46-2.10 vs 0.85) -- doubly
  rejected. Real data point against assuming the cap/delta conflict is
  purely a share-price problem: GTLB is well under $60/share and still
  fails on premium because of very high IV (173-187%).

Soft-catalyst track not run today -- the morning's real movers (AEHL/
NCRA/WETO/XAIR, already logged) are ultra-low-price/low-liquidity names
unlikely to carry a tradeable option chain at all, not screened.

**Running S7 total: 13/13 real checks rejected, 0 trades.** No watchlist
message needed beyond the WETO/ELMT note (already covered above); no S7
position opened or closed.

## 2026-08-31 ~10:12am ET -- Momentum scanner alert: 10am cycle, WETO explodes, RDHL new (unverified catalyst)

Market open since 9:30am -- Robinhood's own Relative volume field is
trustworthy now, no self-computed substitution needed this cycle.

**WETO exploded to a real new high.** $7.90 at 9:36am -> $10.25-10.39 now
(both run_scan and get_equity_quotes confirm), +79-82% vs Friday's
close, RVOL 5.49x (real, market-hours field). Same catalyst as logged
this morning ($75M dilutive share-sale agreement) -- this remains a
dilution-bounce, now a genuinely enormous one, not a clean breakout.

**NCRA continued: $2.42 -> $2.73-2.76** (+44-46%), RVOL 10.6x (real).
Same clean JV catalyst (INERGX Energy) as logged this morning.

**RDHL (RedHill Biopharma) -- new, huge, catalyst UNVERIFIED.** +64% to
$1.08, RVOL huge, EXTREMELY_HIGH message volume (94), 97% bullish
sentiment. Real short-squeeze mechanics visible in the actual Stocktwits
posts (traders reporting real margin calls / short covering, real-time
flip-flopping). Retail chatter cites "$18M cash upfront and royalties"
from an unlinked forum post, but get_equity_news for RDHL returned
NOTHING beyond mechanical "stock moved X%" premarket-movers roundups --
no actual dated press release found. Flagged to the user explicitly as
price-action-only / catalyst unverified, not presented as clean.

AEHL real RVOL now confirms 4.61x (market-hours field, no longer
ambiguous) but no new high since the 9:36am check -- not re-alerted.
BRNX's real RVOL is actually BELOW 1x this hour (0.19x) despite price
staying up -- genuinely cooling, not re-alerted. YDDL/WBUY/LGPS also
newly appeared with real gains (42%/28%/21%) and elevated RVOL but were
not individually catalyst-checked this cycle given time budget --
picked up next cycle if they persist.

## 2026-08-31 ~11:11am ET -- Momentum scanner alert: 11am cycle, WETO keeps running, MOBX new (real M&A catalyst)

**WETO made ANOTHER real new high.** $10.25-10.39 at 10:12am -> $12.50-
12.55 now (get_equity_quotes + run_scan both confirm), +119% vs
Friday's close, RVOL 11.09x. Same $75M dilutive-offering catalyst as
all day -- an extraordinary continuation of what started as a dilution
bounce. Third consecutive cycle this has materially changed.

**MOBX (Mobix Labs) -- new, real, dated catalyst.** +16% to $1.28,
RVOL 68.99x. Real news, confirmed via Stocktwits (quoting the actual
Business Wire/RTPR release, pushed 8:45am ET today): "Vision Aerial
begins Vulcan drone production ahead of acquisition by Mobix Labs,
projecting 46% revenue growth in 2026 and 93% in 2027." Real M&A/
acquisition-progress catalyst, not chatter. Message volume cooling
slightly in the last 15 minutes (skeptical posts appearing: "needs some
volume," "RSI taking a breather") -- noted, not omitted.

AEHL ($6.23-6.26, +76-77%, still below its earlier $6.56-6.58 peak),
NCRA ($2.47-2.48, +30-31%, down from $2.73-2.76), RDHL ($1.10-1.11,
+64-68%, roughly flat) -- no material change on any, not re-alerted.

## 2026-08-31 ~12:08pm ET -- Momentum scanner alert: noon cycle, AEHL fresh high, CVKD new (real FDA catalyst)

**AEHL made a genuine new high, above every earlier peak today.**
$6.23-6.26 at 11:11am -> **$6.73 now**, +90.1% vs Friday's close, RVOL
6.47x (real). Same dilution-bounce catalyst as all day, but this is its
best print of the session by a real margin (prior best was $6.56-6.58).

**CVKD (Cadrenal Therapeutics) -- new, clean, real FDA catalyst.** +15%
to $1.77, RVOL 376x. Confirmed via the actual Globe Newswire/RTPR
release (pushed 8:00am ET today): "Cadrenal Therapeutics Announces
Positive Outcome from FDA Type D Meeting for Phase 3 Registration Study
of CAD-1005 in Heparin-Induced Thrombocytopenia" -- a real regulatory
catalyst, the cleanest of today's names. Some bearish chatter present
too ("careful of an offering," "massive dumping") -- normal mixed retail
sentiment on a biotech pump, noted not omitted.

**WETO pulled back from its high** ($12.50-12.55 at 11:11am -> $10.54
now, RVOL still 12.6x) -- its high is now over an hour old and hasn't
been retested, so per the job's own "already printed" rule this was not
re-alerted, though flagged here since it had been the day's biggest
mover. NCRA ($2.73, flat) and RDHL ($1.07, flat) unchanged, not
re-alerted.

## 2026-08-31 ~1:10pm ET -- Momentum scanner alert: quiet cycle, nothing re-alerted

Everything (WETO $10.85, AEHL $6.565, RDHL $1.05, NCRA $2.53, CVKD
$1.75, MOBX $1.275) flat-to-fading from its earlier peak, no new highs.
Correctly quiet, no user message sent.

## 2026-08-31 ~2:09pm ET -- Momentum scanner alert: NCRA second wind, real jump

**NCRA re-ignited.** $2.53 (+34%) an hour ago -> **$2.90-2.93 now**
(get_equity_quotes confirms, 18:09:49 UTC), +53.4% vs Friday's close,
RVOL 26.9x -- a real, fresh acceleration back toward its session high
($2.98, set ~7-9am), not a stale number. Same clean JV catalyst
(INERGX Energy) as logged all day. Materially changed enough from the
last cycle (+34% -> +53%) to re-alert.

AEHL ($6.24, down from $6.565), WETO ($9.50, continuing to fade from
its $12.55 peak), RDHL ($1.049, flat), CVKD ($1.751, flat), MOBX
($1.33, modest continuation) -- no material change on any, not
re-alerted.
