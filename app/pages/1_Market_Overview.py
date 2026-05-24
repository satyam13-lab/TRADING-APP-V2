from pathlib import Path

import pandas as pd
import streamlit as st
import yaml

from app.components.metric_card import render_metric_card
from app.components.page_shell import render_panel, render_workspace_header, setup_page, status_pill
from broker.zerodha.instrument_manager import WATCHLIST
from broker.zerodha.instruments import ZerodhaInstrumentRegistry
from broker.zerodha.market_data_handler import MarketDataHandler


ROOT_DIR = Path(__file__).resolve().parent.parent.parent


def load_instrument_config():

    with open(
        ROOT_DIR / "config" / "instruments.yaml",
        "r",
        encoding="utf-8"
    ) as file:
        return yaml.safe_load(file) or {}


setup_page("Market Overview")
render_workspace_header(
    "Market Overview",
    "Live universe, breadth proxies, volatility watch, and instrument coverage."
)

registry = ZerodhaInstrumentRegistry()
live_data = MarketDataHandler.get_data()
config = load_instrument_config()

top = st.columns(4)

with top[0]:
    render_metric_card(
        "Watchlist",
        str(len(WATCHLIST)),
        "Streaming instruments"
    )

with top[1]:
    render_metric_card(
        "Live Ticks",
        str(len(live_data)),
        "Latest snapshots"
    )

with top[2]:
    render_metric_card(
        "Indices",
        str(len(config.get("indices", []))),
        "Configured universe"
    )

with top[3]:
    render_metric_card(
        "Equities",
        str(len(config.get("equities", []))),
        "Liquid basket"
    )

st.markdown("---")

left, right = st.columns([2, 1])

with left:
    render_panel(
        "Configured Instruments",
        "Primary trading universe and enablement state."
    )

    rows = []
    for item in config.get("indices", []):
        rows.append(
            {
                "Alias": item.get("alias"),
                "Symbol": item.get("symbol"),
                "Exchange": item.get("exchange"),
                "Token": item.get("instrument_token", ""),
                "Enabled": item.get("enabled", False)
            }
        )

    st.dataframe(
        pd.DataFrame(rows),
        use_container_width=True,
        hide_index=True
    )

with right:
    render_panel(
        "Market State",
        "Operational read of configured feeds."
    )

    feed_state = "green" if live_data else "amber"
    feed_label = "Live feed active" if live_data else "Awaiting live feed"
    st.markdown(
        status_pill(feed_label, feed_state),
        unsafe_allow_html=True
    )
    st.markdown("")

    st.metric(
        "Breadth Proxy",
        "Pending",
        "Requires equity feed"
    )
    st.metric(
        "Volatility Proxy",
        "Pending",
        "Requires VIX feed"
    )

st.markdown("---")

render_panel(
    "Latest Live Snapshots",
    "Current tick state keyed by resolved instrument name."
)

snapshot_rows = []
for token, values in live_data.items():
    instrument = registry.get_by_token(token)
    snapshot_rows.append(
        {
            "Instrument": instrument.tradingsymbol if instrument else f"Token {token}",
            "Token": token,
            "Last Price": values.get("last_price"),
            "Volume": values.get("volume"),
            "OI": values.get("oi"),
            "Timestamp": values.get("timestamp")
        }
    )

if snapshot_rows:
    st.dataframe(
        pd.DataFrame(snapshot_rows),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No live market snapshots yet.")
