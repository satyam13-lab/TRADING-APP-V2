import streamlit as st

from broker.zerodha.market_data_handler import (
    MarketDataHandler
)


def render_live_market_panel():

    st.subheader(
        "Live Market Feed"
    )

    st.caption(
        "Real-time market data"
    )

    data = MarketDataHandler.get_data()

    if not data:

        st.warning(
            "No live market data available"
        )

        return

    for token, values in data.items():

        st.metric(
            label=f"Instrument {token}",
            value=values.get(
                "last_price"
            )
        )