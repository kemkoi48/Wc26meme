"""Tests for event_catalog.py.

The AAPL test replays REAL bars (get_equity_historicals, 2018-2026,
pulled live 2026-09-01, saved as fixture) and asserts
historical_moves_from_bars reproduces the same eight numbers computed by
hand that session -- a real cross-check, not a synthetic assertion, since
the whole point of this module is not to silently drift from what
actually happened.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from event_catalog import EventSeries, get_event_series, historical_moves_from_bars

FIXTURE = Path(
    "/root/.claude/projects/-home-user-Wc26meme/"
    "765d6f61-b995-5466-8187-9a1ba3fcf877/tool-results/"
    "mcp-Robinhood-get_equity_historicals-1788276990114.txt"
)

# Computed by hand from the same real fixture, 2026-09-01 (see sources.md
# "AAPL Sept-event trend"). Nearest-trading-day event closes:
# 2018-09-12 $55.27, 2019-09-10 $54.17, 2020-09-15 $115.54,
# 2021-09-14 $148.12, 2022-09-07 $155.96, 2023-09-12 $176.30,
# 2024-09-09 $220.91, 2025-09-09 $234.35 -- each compared against the
# PRIOR real trading day's close ('am' timing).
EXPECTED_MOVES = [
    (55.27 - 55.96) / 55.96 * 100.0,      # 2018 (prior close 2018-09-11)
    (54.17 - 53.54) / 53.54 * 100.0,      # 2019 (prior close 2019-09-09)
    (115.54 - 115.36) / 115.36 * 100.0,   # 2020 (prior close 2020-09-14)
    (148.12 - 149.55) / 149.55 * 100.0,   # 2021 (prior close 2021-09-13)
    (155.96 - 154.53) / 154.53 * 100.0,   # 2022 (prior close 2022-09-06)
    (176.30 - 179.36) / 179.36 * 100.0,   # 2023 (prior close 2023-09-11)
    (220.91 - 220.82) / 220.82 * 100.0,   # 2024 (prior close 2024-09-06)
    (234.35 - 237.88) / 237.88 * 100.0,   # 2025 (prior close 2025-09-08)
]


def _load_real_aapl_bars() -> list[dict]:
    with FIXTURE.open() as f:
        data = json.load(f)
    return data["data"]["results"][0]["bars"]


@pytest.mark.skipif(not FIXTURE.exists(), reason="live-pull fixture not present in this environment")
def test_historical_moves_from_bars_matches_real_aapl_series():
    series = get_event_series("AAPL", "product_event")
    assert series is not None
    bars = _load_real_aapl_bars()
    moves = historical_moves_from_bars(series, bars)
    assert len(moves) == len(EXPECTED_MOVES) == len(series.past_dates)
    for got, want in zip(moves, EXPECTED_MOVES):
        assert got == pytest.approx(want, abs=0.01)


def test_get_event_series_unknown_returns_none():
    assert get_event_series("ZZZZ", "product_event") is None
    assert get_event_series("AAPL", "not_a_real_catalyst_type") is None


def test_list_event_series_filters_by_symbol():
    from event_catalog import list_event_series

    all_series = list_event_series()
    assert len(all_series) >= 1
    aapl_only = list_event_series("aapl")  # case-insensitive
    assert all(s.symbol == "AAPL" for s in aapl_only)
    assert len(aapl_only) >= 1


def test_historical_moves_from_bars_discards_interpolated_and_zero_volume():
    series = EventSeries(
        symbol="TEST",
        catalyst_type="product_event",
        timing="am",
        past_dates=("2026-01-10",),
    )
    bars = [
        {"begins_at": "2026-01-09T00:00:00Z", "close_price": "100.0", "volume": 1000, "interpolated": False},
        # A synthesized gap-fill bar sitting right at the event date --
        # must be ignored, not treated as the real event-day close.
        {"begins_at": "2026-01-10T00:00:00Z", "close_price": "100.0", "volume": 0, "interpolated": True},
        {"begins_at": "2026-01-10T00:00:00Z", "close_price": "110.0", "volume": 500, "interpolated": False},
    ]
    moves = historical_moves_from_bars(series, bars)
    # Real event-day close ($110) vs real prior close ($100) -- +10%, not
    # the 0.0% a naive reader of the interpolated duplicate would compute.
    assert moves == pytest.approx([10.0], abs=1e-9)


def test_historical_moves_from_bars_am_vs_pm_timing():
    bars = [
        {"begins_at": "2026-03-01T00:00:00Z", "close_price": "50.0", "volume": 100, "interpolated": False},
        {"begins_at": "2026-03-02T00:00:00Z", "close_price": "55.0", "volume": 100, "interpolated": False},
        {"begins_at": "2026-03-03T00:00:00Z", "close_price": "60.0", "volume": 100, "interpolated": False},
    ]
    am_series = EventSeries("TEST", "x", "am", ("2026-03-02",))
    pm_series = EventSeries("TEST", "x", "pm", ("2026-03-02",))
    # 'am': event-day close (55) vs PRIOR close (50) -> +10%
    assert historical_moves_from_bars(am_series, bars) == pytest.approx([10.0])
    # 'pm': NEXT close (60) vs event-day close (55) -> +9.0909...%
    assert historical_moves_from_bars(pm_series, bars) == pytest.approx([9.0909], abs=1e-3)


def test_historical_moves_from_bars_skips_occurrence_with_no_data():
    series = EventSeries("TEST", "x", "am", ("1999-01-01",))  # far before any bar
    bars = [
        {"begins_at": "2026-01-01T00:00:00Z", "close_price": "10.0", "volume": 100, "interpolated": False},
    ]
    assert historical_moves_from_bars(series, bars) == []


def test_historical_moves_from_bars_skips_am_occurrence_missing_prior_bar():
    # Event is the very first bar in the series -- no prior close exists.
    series = EventSeries("TEST", "x", "am", ("2026-01-01",))
    bars = [
        {"begins_at": "2026-01-01T00:00:00Z", "close_price": "10.0", "volume": 100, "interpolated": False},
    ]
    assert historical_moves_from_bars(series, bars) == []


def test_historical_moves_from_bars_skips_pm_occurrence_missing_next_bar():
    # Event is the LAST bar in the series -- no next-day close exists yet.
    series = EventSeries("TEST", "x", "pm", ("2026-01-05",))
    bars = [
        {"begins_at": "2026-01-04T00:00:00Z", "close_price": "9.0", "volume": 100, "interpolated": False},
        {"begins_at": "2026-01-05T00:00:00Z", "close_price": "10.0", "volume": 100, "interpolated": False},
    ]
    assert historical_moves_from_bars(series, bars) == []
