import streamlit as st

from broker.zerodha.market_data_handler import (
    MarketDataHandler
)
from broker.zerodha.instruments import ZerodhaInstrumentRegistry


instrument_registry = ZerodhaInstrumentRegistry()


def _instrument_label(token):

    instrument = instrument_registry.get_by_token(
        int(token)
    )

    if not instrument:

        return f"Instrument {token}"

    return instrument.tradingsymbol


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

        candle = MarketDataHandler.get_latest_candle(
            token
        )

        delta = None

        if candle:

            delta = (
                f"O {candle.open:.2f} | "
                f"H {candle.high:.2f} | "
                f"L {candle.low:.2f} | "
                f"C {candle.close:.2f}"
            )

        st.metric(
            label=_instrument_label(
                token
            ),
            value=values.get(
                "last_price"
            ),
            delta=delta
        )
