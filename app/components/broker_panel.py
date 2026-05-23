import streamlit as st
import subprocess
import webbrowser
import time


def render_broker_panel(
    auth,
    session
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

        if st.button(
            "🚀 Start New Session With Zerodha"
        ):

            try:

                subprocess.Popen(
                    [
                        "python",
                        "broker/zerodha/callback_server.py"
                    ]
                )

                time.sleep(2)

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

        st.success(
            f"""
            Connected Successfully

            User:
            {user_name}
            """
        )