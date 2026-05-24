import pandas as pd
import streamlit as st

from app.components.metric_card import render_metric_card
from app.components.page_shell import render_panel, render_workspace_header, setup_page, status_pill
from broker.zerodha.market_data_handler import MarketDataHandler
from broker.zerodha.session_manager import SessionManager


setup_page("Live Trading")
render_workspace_header(
    "Live Trading",
    "Execution readiness, positions, orders, and live feed state."
)

session = SessionManager.load_session()
live_data = MarketDataHandler.get_data()

status_cols = st.columns(4)

with status_cols[0]:
    render_metric_card(
        "Broker Session",
        "ACTIVE" if session else "OFFLINE",
        "Zerodha access token",
        "#16A34A" if session else "#DC2626"
    )

with status_cols[1]:
    render_metric_card(
        "Feed Snapshots",
        str(len(live_data)),
        "Latest instrument ticks"
    )

with status_cols[2]:
    render_metric_card(
        "Open Positions",
        "0",
        "Position manager"
    )

with status_cols[3]:
    render_metric_card(
        "Order Mode",
        "PAPER",
        "Live guard enabled",
        "#D97706"
    )

st.markdown("---")

left, right = st.columns([2, 1])

with left:
    render_panel(
        "Positions",
        "Intraday exposure and realized state."
    )
    st.dataframe(
        pd.DataFrame(
            columns=[
                "Symbol",
                "Side",
                "Qty",
                "Avg Price",
                "LTP",
                "PnL",
                "Risk"
            ]
        ),
        use_container_width=True,
        hide_index=True
    )

with right:
    render_panel(
        "Execution Status",
        "Current operating guardrails."
    )
    st.markdown(
        status_pill("Paper mode", "amber"),
        unsafe_allow_html=True
    )
    st.markdown(" ")
    st.markdown(
        status_pill("Live orders blocked", "green"),
        unsafe_allow_html=True
    )
    st.markdown(" ")
    st.markdown(
        status_pill("Risk approval required", "green"),
        unsafe_allow_html=True
    )

st.markdown("---")

render_panel(
    "Order Blotter",
    "Submitted, filled, rejected, and cancelled order state."
)
st.dataframe(
    pd.DataFrame(
        columns=[
            "Time",
            "Order ID",
            "Symbol",
            "Side",
            "Type",
            "Qty",
            "Status",
            "Reason"
        ]
    ),
    use_container_width=True,
    hide_index=True
)
