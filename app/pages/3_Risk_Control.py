from pathlib import Path

import pandas as pd
import streamlit as st
import yaml

from app.components.metric_card import render_metric_card
from app.components.page_shell import render_panel, render_workspace_header, setup_page, status_pill


ROOT_DIR = Path(__file__).resolve().parent.parent.parent


def load_risk_config():

    with open(
        ROOT_DIR / "config" / "risk_config.yaml",
        "r",
        encoding="utf-8"
    ) as file:
        return yaml.safe_load(file) or {}


setup_page("Risk Control")
render_workspace_header(
    "Risk Control",
    "Portfolio limits, kill switch state, exposure checks, and sizing controls."
)

risk_config = load_risk_config()
risk = risk_config.get("risk", {})
guards = risk_config.get("execution_guards", {})

cols = st.columns(4)

with cols[0]:
    render_metric_card(
        "Risk / Trade",
        f"{risk.get('risk_per_trade_pct', 0)}%",
        "Capital at risk"
    )

with cols[1]:
    render_metric_card(
        "Daily Max Loss",
        f"{risk.get('daily_max_loss_pct', 0)}%",
        "Hard stop"
    )

with cols[2]:
    render_metric_card(
        "Weekly Max Loss",
        f"{risk.get('weekly_max_loss_pct', 0)}%",
        "Hard stop"
    )

with cols[3]:
    render_metric_card(
        "Open Positions",
        str(risk.get("max_open_positions", 0)),
        "Portfolio cap"
    )

st.markdown("---")

left, right = st.columns([1, 1])

with left:
    render_panel(
        "Execution Guards",
        "Pre-trade requirements before any order leaves the system."
    )

    guard_rows = [
        {
            "Guard": key.replace("_", " ").title(),
            "Enabled": value
        }
        for key, value in guards.items()
    ]
    st.dataframe(
        pd.DataFrame(guard_rows),
        use_container_width=True,
        hide_index=True
    )

with right:
    render_panel(
        "Kill Switch",
        "System-level survival control."
    )

    kill_enabled = bool(
        risk.get("kill_switch_enabled", True)
    )
    st.markdown(
        status_pill(
            "Enabled" if kill_enabled else "Disabled",
            "green" if kill_enabled else "red"
        ),
        unsafe_allow_html=True
    )
    st.metric(
        "Current Drawdown",
        "0.00%",
        "No live positions"
    )
    st.metric(
        "Available Risk Budget",
        "100%",
        "Paper session"
    )

st.markdown("---")

render_panel(
    "Exposure Matrix",
    "Instrument, strategy, and portfolio-level risk occupancy."
)
st.dataframe(
    pd.DataFrame(
        columns=[
            "Strategy",
            "Instrument",
            "Exposure",
            "Correlation Bucket",
            "Risk Used",
            "Approval"
        ]
    ),
    use_container_width=True,
    hide_index=True
)
