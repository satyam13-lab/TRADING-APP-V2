import streamlit as st


def render_sidebar():

    with st.sidebar:

        st.markdown(
            """
            <div class="sidebar-title">
                📈 TRADING-APP-V2
            </div>

            <div class="sidebar-subtitle">
                Quant Trading System
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        st.markdown("### MODULES")

        modules = [
            "Broker",
            "Market Data",
            "Strategies",
            "Risk Engine",
            "Execution",
            "Backtesting",
            "AI Engine",
            "Reports",
            "Settings"
        ]

        for module in modules:

            st.markdown(
                f"""
                <div class="module-item">
                    • {module}
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<br><br>", unsafe_allow_html=True)

        st.success("System Operational")