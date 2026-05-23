import sys
from pathlib import Path
from datetime import datetime, time
from zoneinfo import ZoneInfo

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


MARKET_TIMEZONE = ZoneInfo("Asia/Kolkata")


def is_market_open():

    now = datetime.now(
        MARKET_TIMEZONE
    )

    return (
        now.weekday() < 5
        and time(9, 15) <= now.time() <= time(15, 30)
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


@st.cache_data(
    ttl=60,
    show_spinner=False
)
def get_zerodha_api_status(access_token):

    checker = ZerodhaAuth()

    return checker.validate_session(
        access_token
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

api_status = {
    "status": False,
    "state": "disconnected",
    "error": "No active session"
}


# =========================================================
# AUTO SESSION REFRESH
# =========================================================

if session is None:

    st_autorefresh(
        interval=3000,
        key="session_refresh"
    )

    session = SessionManager.load_session()

if session:

    api_status = get_zerodha_api_status(
        session.get(
            "access_token"
        )
    )


# =========================================================
# WEBSOCKET SESSION STATE
# =========================================================

if "ws" not in st.session_state:

    st.session_state.ws = None

if session is None and st.session_state.ws:

    st.session_state.ws.close()

    st.session_state.ws = None

current_ws = st.session_state.ws

feed_active = current_ws is not None

feed_connected = bool(
    current_ws
    and getattr(
        current_ws,
        "connected",
        False
    )
)

market_open = is_market_open()


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

    api_connected = api_status.get(
        "status",
        False
    )

    api_state = api_status.get(
        "state",
        "disconnected"
    )

    render_metric_card(
        title="Zerodha API",

        value=(
            "● CONNECTED"
            if api_connected
            else (
                "● CHECKING"
                if session and api_state == "unverified"
                else "● DISCONNECTED"
            )
        ),

        subtitle=(
            "Broker API verified"
            if api_connected
            else (
                "Session exists, API not verified"
                if session
                else "Authentication required"
            )
        ),

        value_color=(
            "#16A34A"
            if api_connected
            else (
                "#D97706"
                if session
                else "#DC2626"
            )
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
        session,
        api_status
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
            "▶ Start Live Feed",
            disabled=feed_active
        ):

            try:

                ws = ZerodhaWebSocket(
                    access_token
                )

                ws.connect()

                st.session_state.ws = ws

                current_ws = ws

                feed_active = True

                st.success(
                    "Live market feed started successfully"
                )

            except Exception as e:

                st.error(
                    str(e)
                )

    with col2:

        if st.button(
            "■ Stop Live Feed",
            disabled=not feed_active
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
        if feed_connected
        else (
            "📡 Data Feed\n\nConnecting"
            if feed_active
            else "📡 Data Feed\n\nDisconnected"
        )
    )

with b2:

    st.info(
        "🕒 Market Status\n\nOpen"
        if market_open
        else "🕒 Market Status\n\nClosed"
    )

with b3:

    st.info(
        "🔄 Next Update\n\nLive"
        if feed_active
        else "🔄 Next Update\n\nPaused"
    )

with b4:

    st.info(
        "⚡ Engine Status\n\nRunning"
        if feed_connected
        else "⚡ Engine Status\n\nIdle"
    )


# =========================================================
# AUTO REFRESH LIVE MARKET DATA
# =========================================================

if feed_active:

    st_autorefresh(
        interval=2000,
        key="live_market_refresh"
    )
