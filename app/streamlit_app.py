import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import streamlit as st

from streamlit_autorefresh import (
    st_autorefresh
)

from broker.zerodha.auth import ZerodhaAuth

from broker.zerodha.session_manager import (
    SessionManager
)

from broker.zerodha.websocket_manager import (
    ZerodhaWebSocket
)

from app.styles.global_css import (
    load_css
)

from app.components.sidebar import (
    render_sidebar
)

from app.components.header import (
    render_header
)

from app.components.metric_card import (
    render_metric_card
)

from app.components.broker_panel import (
    render_broker_panel
)

from app.components.health_panel import (
    render_health_panel
)

from app.components.live_market_panel import (
    render_live_market_panel
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="TRADING-APP-V2",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# LOAD CSS
# =========================================================

st.markdown(
    load_css(),
    unsafe_allow_html=True
)


# =========================================================
# LOAD AUTH
# =========================================================

auth = ZerodhaAuth()


# =========================================================
# LOAD SESSION
# =========================================================

session = SessionManager.load_session()


# =========================================================
# AUTO SESSION REFRESH
# =========================================================

if session is None:

    st_autorefresh(
        interval=3000,
        key="session_refresh"
    )

    session = SessionManager.load_session()


# =========================================================
# WEBSOCKET SESSION STATE
# =========================================================

if "ws" not in st.session_state:

    st.session_state.ws = None


# =========================================================
# SIDEBAR
# =========================================================

render_sidebar()


# =========================================================
# HEADER
# =========================================================

render_header()


# =========================================================
# TOP METRIC CARDS
# =========================================================

c1, c2, c3, c4 = st.columns(4)

with c1:

    render_metric_card(
        title="Broker",
        value="Zerodha",
        subtitle="Kite Connect"
    )

with c2:

    render_metric_card(
        title="Session Status",

        value=(
            "CONNECTED"
            if session
            else "DISCONNECTED"
        ),

        subtitle="Authentication State",

        value_color=(
            "#16A34A"
            if session
            else "#DC2626"
        )
    )

with c3:

    render_metric_card(
        title="Environment",
        value="PAPER",
        subtitle="Simulation Mode"
    )

with c4:

    render_metric_card(
        title="Mode",
        value="MANUAL",
        subtitle="Manual Trading"
    )


# =========================================================
# MAIN PANELS
# =========================================================

left, right = st.columns([2, 1])

with left:

    render_broker_panel(
        auth,
        session
    )

with right:

    render_health_panel()


# =========================================================
# LIVE MARKET DATA SECTION
# =========================================================

st.markdown("---")

st.subheader(
    "Live Market Data"
)

st.caption(
    "Zerodha WebSocket Streaming"
)


# =========================================================
# LIVE FEED CONTROLS
# =========================================================

if session:

    access_token = session.get(
        "access_token"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "▶ Start Live Feed"
        ):

            try:

                ws = ZerodhaWebSocket(
                    access_token
                )

                ws.connect()

                st.session_state.ws = ws

                st.success(
                    "Live market feed started successfully"
                )

            except Exception as e:

                st.error(
                    str(e)
                )

    with col2:

        if st.button(
            "■ Stop Live Feed"
        ):

            try:

                if st.session_state.ws:

                    st.session_state.ws.close()

                    st.session_state.ws = None

                    st.warning(
                        "Live market feed stopped"
                    )

            except Exception as e:

                st.error(
                    str(e)
                )

else:

    st.info(
        "Connect Zerodha session first"
    )


# =========================================================
# LIVE MARKET PANEL
# =========================================================

render_live_market_panel()


# =========================================================
# LIVE FEED STATUS
# =========================================================

st.markdown("---")

b1, b2, b3, b4 = st.columns(4)

with b1:

    st.info(
        "📡 Data Feed\n\nConnected"
        if st.session_state.ws
        else "📡 Data Feed\n\nDisconnected"
    )

with b2:

    st.info(
        "🕒 Market Status\n\nOpen"
    )

with b3:

    st.info(
        "🔄 Next Update\n\nLive"
    )

with b4:

    st.info(
        "⚡ Engine Status\n\nRunning"
    )


# =========================================================
# AUTO REFRESH LIVE MARKET DATA
# =========================================================

if st.session_state.ws:

    st_autorefresh(
        interval=2000,
        key="live_market_refresh"
    )