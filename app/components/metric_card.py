import streamlit as st


def render_metric_card(
    title,
    value,
    subtitle,
    value_color="#0F172A"
):

    with st.container():

        st.markdown(
            f"""
            <style>
            .metric-title {{
                font-size: 15px;
                color: #64748B;
                margin-bottom: 10px;
            }}

            .metric-value {{
                font-size: 32px;
                font-weight: 700;
                color: {value_color};
                margin-bottom: 5px;
            }}

            .metric-sub {{
                font-size: 16px;
                color: #64748B;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="metric-title">
                {title}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="metric-value">
                {value}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="metric-sub">
                {subtitle}
            </div>
            """,
            unsafe_allow_html=True
        )