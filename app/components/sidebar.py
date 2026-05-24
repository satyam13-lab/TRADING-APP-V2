import streamlit as st


def render_sidebar():

    with st.sidebar:

        st.markdown(
            """
            <div class="sidebar-title">
                TRADING-APP-V2
            </div>

            <div class="sidebar-subtitle">
                Quant Trading System
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        st.markdown("### WORKSPACES")

        st.page_link(
            "app/streamlit_app.py",
            label="Broker Terminal"
        )
        st.page_link(
            "app/pages/1_Market_Overview.py",
            label="Market Overview"
        )
        st.page_link(
            "app/pages/2_Live_Trading.py",
            label="Live Trading"
        )
        st.page_link(
            "app/pages/3_Risk_Control.py",
            label="Risk Control"
        )
        st.page_link(
            "app/pages/4_Backtest_Analytics.py",
            label="Backtest Analytics"
        )
        st.page_link(
            "app/pages/5_Research_AI.py",
            label="Research and AI"
        )

        st.markdown("<br><br>", unsafe_allow_html=True)

        st.success("System Operational")
