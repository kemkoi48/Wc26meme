# Scanner board — target spec (from user screenshot, 2026-09-17)

Reference: thedesperatetrader.com/stock-market-today. User's verdict on my two
attempts: "ugly looking magazine with old ignition board in it. I NEED SOMETHING
MORE SOPHISTICATED AND ORGANIZED."

## What I got wrong twice — read before building

1. Built a **document** (prose, essays, marginalia, per-stock write-ups) when the
   ask was a **dense product dashboard**. No long-form prose anywhere on v3.
2. Used a **light editorial palette**. Target is **dark navy, high density**.
   "Sophisticated and editorial" meant sophisticated PRODUCT design, not print.
3. Carried teaching content into the primary view. Patterns/indicators/vault are
   secondary pages, not sections on the board.
4. Wrote per-stock narrative. **No stock is ever named in source.** Every name on
   screen is fetched live.

## Layout (three columns, dark)

- **Left sidebar, persistent nav**: Home · Stock Market Today · Top Stocks Today ·
  Live Radar · Alerts · My Watchlist · Charts · All Scanners · RVOL Scanner ·
  Stock Screener · Site Guide · Guides. Above it a TRENDING panel: ticker, volume,
  sparkline, price, % change chip.
- **Top bar**: brand, index strip (SPY/NDQ/DOW/RUT with %), search, actions.
- **Main column**:
  - Timeframe tabs: **Scalping / Day / Swing / Position / Investing** with a
    one-line description of what each horizon means.
  - Stat chip row: market status · alert count (2h) · active names · a meter.
  - Action row: Copy text · Share board · Stocks to watch · Full scanner.
  - Live indicator + "1m ago" + Refresh.
  - **TOP PLAY RIGHT NOW** hero card — the single highest-conviction name:
    ticker, price, % change, large sparkline, metric tags (on N boards, volume,
    most-alerted count, top RVOL x, EMA trend), and critically a
    **"Why:" line carrying the catalyst + its source** (their example cites
    SEC EDGAR). This is our catalyst gate rendered as the hero. Ours should say
    plainly when no catalyst is found rather than promoting the name.
  - **Three ranked card columns**: Most Alerted (last 2h) · Top Movers (last 15m)
    · Top RVOL (peak, last 2h). Each row: rank, ticker, price, % change, volume,
    sparkline, and the ranking metric on the right.
- **Right rail**: optional. Theirs is live chat; ours could be the alert log.

## Build notes

- Data: Robinhood connector, already proven working from the artifact runtime.
  `claude.use("mcp")` -> `watchTool("Robinhood","run_scan",{scan_id},cb,
  {cache:{staleTime:30000},refetchInterval:30000})`, payload at
  `res.payload.data.result.results`. Board d6619239 is the reference implementation.
- Sparklines everywhere -> `get_equity_historicals`, batched, cached.
- Density over whitespace. Small type, tight rows, tabular numerals.
- Keep: the encrypted strategy vault, candle patterns, indicator glossary —
  but on SEPARATE pages reached from the sidebar, not on the board.
- Ignition board (d6619239) stays untouched as the working fallback.

## Deferred to the weekend at user's request (token budget before Friday).
