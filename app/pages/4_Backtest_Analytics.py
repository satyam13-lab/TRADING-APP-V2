import pandas as pd
import streamlit as st

from app.components.metric_card import render_metric_card
from app.components.page_shell import render_panel, render_workspace_header, setup_page, status_pill


setup_page("Backtest Analytics")
render_workspace_header(
    "Backtest Analytics",
    "Daily strategy evaluation, performance metrics, and edge decay monitoring."
)

cols = st.columns(4)

with cols[0]:
    render_metric_card(
        "Strategies Tested",
        "0",
        "Awaiting first run"
    )

with cols[1]:
    render_metric_card(
        "Best Sharpe",
        "Pending",
        "Risk adjusted"
    )

with cols[2]:
    render_metric_card(
        "Max Drawdown",
        "Pending",
        "Survival metric"
    )

with cols[3]:
    render_metric_card(
        "Leaderboard",
        "Empty",
        "Daily ranking"
    )

st.markdown("---")

left, right = st.columns([2, 1])

with left:
    render_panel(
        "Strategy Leaderboard",
        "Ranked by expectancy, drawdown, stability, and regime fit."
    )
    st.dataframe(
        pd.DataFrame(
            columns=[
                "Rank",
                "Strategy",
                "Regime",
                "Sharpe",
                "Max DD",
                "Profit Factor",
                "Expectancy",
                "Status"
            ]
        ),
        use_container_width=True,
        hide_index=True
    )

with right:
    render_panel(
        "Daily Backtest",
        "Scheduler and data readiness."
    )
    st.markdown(
        status_pill("Not scheduled", "amber"),
        unsafe_allow_html=True
    )
    st.metric(
        "Latest Dataset",
        "Pending",
        "No run recorded"
    )
    st.metric(
        "Last Run",
        "Pending",
        "No backtest log"
    )

st.markdown("---")

render_panel(
    "Trade Log",
    "Executed historical trades with slippage and costs."
)
st.dataframe(
    pd.DataFrame(
        columns=[
            "Entry Time",
            "Exit Time",
            "Symbol",
            "Strategy",
            "Side",
            "Entry",
            "Exit",
            "PnL",
            "Regime"
        ]
    ),
    use_container_width=True,
    hide_index=True
)
