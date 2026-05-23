import streamlit as st


def render_header():

    st.markdown(
        """
        <div class="main-title">
            Institutional Algo Trading Platform
        </div>

        <div class="sub-title">
            Zerodha • Quantitative Trading • Multi Asset • AI Assisted
        </div>
        """,
        unsafe_allow_html=True
    )