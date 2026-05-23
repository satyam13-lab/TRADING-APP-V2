import streamlit as st

from app.components.metric_card import (
    render_metric_card
)


def render_health_panel():

    st.subheader(
        "System Health"
    )

    st.caption(
        "Runtime diagnostics"
    )

    render_metric_card(
        "CPU Usage",
        "3%",
        "Healthy"
    )

    render_metric_card(
        "Memory Usage",
        "24%",
        "Stable"
    )

    render_metric_card(
        "Latency",
        "12ms",
        "Low Latency"
    )