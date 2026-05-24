import pandas as pd
import streamlit as st

from app.components.metric_card import render_metric_card
from app.components.page_shell import render_panel, render_workspace_header, setup_page, status_pill


setup_page("Research and AI")
render_workspace_header(
    "Research and AI",
    "Regime probabilities, signal quality, feature diagnostics, and model governance."
)

cols = st.columns(4)

with cols[0]:
    render_metric_card(
        "Regime Model",
        "OFF",
        "Manual mode",
        "#D97706"
    )

with cols[1]:
    render_metric_card(
        "Feature Store",
        "EMPTY",
        "Awaiting data"
    )

with cols[2]:
    render_metric_card(
        "Signal Ranker",
        "OFF",
        "Not trained",
        "#D97706"
    )

with cols[3]:
    render_metric_card(
        "Trade Quality",
        "Pending",
        "No scores"
    )

st.markdown("---")

left, right = st.columns([1, 1])

with left:
    render_panel(
        "Regime Board",
        "Probability-weighted market state."
    )
    st.dataframe(
        pd.DataFrame(
            [
                {"Regime": "Trending", "Probability": None, "Enabled Strategies": "ORB, EMA"},
                {"Regime": "Mean Reversion", "Probability": None, "Enabled Strategies": "VWAP fades"},
                {"Regime": "Vol Expansion", "Probability": None, "Enabled Strategies": "Breakout options"},
                {"Regime": "Low Vol", "Probability": None, "Enabled Strategies": "Theta systems"}
            ]
        ),
        use_container_width=True,
        hide_index=True
    )

with right:
    render_panel(
        "Model Governance",
        "Live trading requires measurable model quality."
    )
    st.markdown(
        status_pill("AI scoring disabled", "amber"),
        unsafe_allow_html=True
    )
    st.metric(
        "Training Samples",
        "0",
        "Validated rows"
    )
    st.metric(
        "Feature Drift",
        "Pending",
        "Requires history"
    )

st.markdown("---")

render_panel(
    "Signal Quality Queue",
    "Candidate trades ranked by regime fit, liquidity, and risk reward."
)
st.dataframe(
    pd.DataFrame(
        columns=[
            "Time",
            "Symbol",
            "Strategy",
            "Direction",
            "Confidence",
            "RR",
            "Regime Fit",
            "Decision"
        ]
    ),
    use_container_width=True,
    hide_index=True
)
