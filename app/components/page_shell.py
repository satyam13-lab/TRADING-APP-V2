import sys
from pathlib import Path

import streamlit as st


ROOT_DIR = Path(__file__).resolve().parent.parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from app.components.sidebar import render_sidebar
from app.styles.global_css import load_css


def setup_page(title: str):

    st.set_page_config(
        page_title=f"{title} | TRADING-APP-V2",
        page_icon=":chart_with_upwards_trend:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown(
        load_css(),
        unsafe_allow_html=True
    )

    render_sidebar()


def render_workspace_header(title: str, subtitle: str):

    st.markdown(
        f"""
        <div class="workspace-header">
            <div class="workspace-title">{title}</div>
            <div class="workspace-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_panel(title: str, subtitle: str = ""):

    st.markdown(
        f"""
        <div class="panel-title">{title}</div>
        <div class="panel-subtitle">{subtitle}</div>
        """,
        unsafe_allow_html=True
    )


def status_pill(label: str, state: str = "neutral") -> str:

    class_name = {
        "green": "status-green",
        "amber": "status-amber",
        "red": "status-red"
    }.get(
        state,
        ""
    )

    return f'<span class="status-pill {class_name}">{label}</span>'
