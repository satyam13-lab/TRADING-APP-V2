import streamlit as st
import subprocess
import webbrowser
import time
import socket
import sys
import requests
from pathlib import Path
from urllib.parse import urlparse

from config.settings import settings


ROOT_DIR = Path(__file__).resolve().parent.parent.parent

_redirect_url = urlparse(
    settings.REDIRECT_URL
    or "http://127.0.0.1:5000/"
)

CALLBACK_HOST = (
    _redirect_url.hostname
    or "127.0.0.1"
)

CALLBACK_PORT = (
    _redirect_url.port
    or 80
)

CALLBACK_HEALTH_URL = (
    f"http://{CALLBACK_HOST}:{CALLBACK_PORT}/health"
)

CALLBACK_SERVER_ID = "trading-app-v2-zerodha-callback"


def _is_callback_server_running():

    with socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    ) as sock:

        sock.settimeout(0.25)

        return sock.connect_ex(
            (
                CALLBACK_HOST,
                CALLBACK_PORT
            )
        ) == 0


def _is_expected_callback_server():

    try:

        response = requests.get(
            CALLBACK_HEALTH_URL,
            timeout=0.5
        )

        response.raise_for_status()

        return (
            response.json().get(
                "server_id"
            )
            == CALLBACK_SERVER_ID
        )

    except Exception:

        return False


def render_broker_panel(
    auth,
    session,
    api_status=None
):

    st.subheader(
        "Broker Authentication"
    )

    st.caption(
        "Secure connection to Zerodha Kite Connect API"
    )

    st.info(
        """
        1. Start new session

        2. Login to Zerodha

        3. Redirect handled automatically

        4. Session created automatically
        """
    )

    if session is None:

        callback_port_active = _is_callback_server_running()

        expected_callback_active = (
            callback_port_active
            and _is_expected_callback_server()
        )

        if callback_port_active and not expected_callback_active:

            st.error(
                f"""
                Zerodha callback port {CALLBACK_PORT} is occupied by another process.
                Stop the old callback server, then start a new Zerodha session.
                """
            )

        elif expected_callback_active:

            st.info(
                """
                Zerodha callback server is running.
                Complete login in the browser; this page will update after the session is saved.
                """
            )

        if st.button(
            "🚀 Start New Session With Zerodha"
        ):

            try:

                if callback_port_active and not expected_callback_active:

                    st.error(
                        f"""
                        Port {CALLBACK_PORT} is already used by another callback server.
                        Stop that process, then start a new Zerodha session again.
                        """
                    )

                    return

                callback_port_active = _is_callback_server_running()

                if not callback_port_active:

                    subprocess.Popen(
                        [
                            sys.executable,
                            "broker/zerodha/callback_server.py"
                        ],
                        cwd=ROOT_DIR
                    )

                    st.session_state.callback_server_started = True

                    time.sleep(2)

                else:

                    st.session_state.callback_server_started = True

                login_url = auth.get_login_url()

                webbrowser.open(login_url)

                st.success(
                    """
                    Zerodha login flow started successfully.
                    """
                )

            except Exception as e:

                st.error(str(e))

    else:

        user_name = session.get(
            "user_name",
            "Unknown User"
        )

        api_connected = bool(
            api_status
            and api_status.get(
                "status"
            )
        )

        api_line = (
            "Zerodha API: ● Connected"
            if api_connected
            else "Zerodha API: ● Session saved, verification pending"
        )

        st.success(
            f"""
            Connected Successfully

            {api_line}

            User:
            {user_name}
            """
        )
