"""
Planet Hunters — Scientific Intelligence Platform
ML Challenge Hack4Hack 2026 — Round 1
Enterprise Astronomical Telemetry & Machine Learning Analytics Dashboard
"""

import sys
from pathlib import Path
import streamlit as st

# Configure sys.path so dashboard can find root project modules
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dashboard.styles import get_theme_css
from dashboard.components.hero import render_hero
from dashboard.components.performance import render_performance
from dashboard.components.classification import render_classification
from dashboard.components.architecture import render_architecture
from dashboard.components.features import render_features
from dashboard.components.validator import render_validator
from dashboard.components.explorer import render_explorer
from dashboard.components.info import render_info

# Streamlit Page Setup
st.set_page_config(
    page_title="Planet Hunters — Scientific Intelligence Platform",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Theme Management: Default strictly to Light
if "theme" not in st.session_state:
    st.session_state.theme = "light"

# Inject Dynamic CSS with Complete Contrast Protection
st.markdown(get_theme_css(st.session_state.theme), unsafe_allow_html=True)

# Sidebar Navigation & Telemetry
with st.sidebar:
    border_subtle = "#E5EAF1" if st.session_state.theme == "light" else "#1E2D44"
    brand_sub = "#667085" if st.session_state.theme == "light" else "#94A3B8"
    brand_title = "#101B33" if st.session_state.theme == "light" else "#F1F5F9"
    primary_blue = "#2457D6" if st.session_state.theme == "light" else "#3B82F6"

    st.markdown(f"""
    <div style="padding: 4px 0 16px 0; border-bottom: 1px solid {border_subtle};">
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="width: 32px; height: 32px; border-radius: 6px; background-color: {primary_blue}; color: #FFFFFF; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1rem; flex-shrink: 0;">
                PH
            </div>
            <div>
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.05rem; font-weight: 700; letter-spacing: -0.02em; color: {brand_title};">
                    PLANET HUNTERS
                </div>
                <div style="font-size: 0.72rem; font-weight: 600; color: {brand_sub}; text-transform: uppercase; letter-spacing: 0.05em;">
                    Scientific Intelligence
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)

    # Clean Theme Switcher
    st.markdown(f"<div style='font-size: 0.74rem; font-weight: 600; text-transform: uppercase; color: {brand_sub}; margin-bottom: 6px; letter-spacing: 0.04em;'>Interface Appearance</div>", unsafe_allow_html=True)
    theme_choice = st.radio(
        "Interface Appearance Label Hidden",
        options=["☀️ Light Theme", "🌙 Dark Theme"],
        index=0 if st.session_state.theme == "light" else 1,
        horizontal=True,
        label_visibility="collapsed"
    )
    new_theme = "dark" if "Dark" in theme_choice else "light"
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()

    st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)

    # Station Navigation
    st.markdown(f"<div style='font-size: 0.74rem; font-weight: 600; text-transform: uppercase; color: {brand_sub}; margin-bottom: 6px; letter-spacing: 0.04em;'>Platform Navigation</div>", unsafe_allow_html=True)
    view_mode = st.radio(
        "Navigation Station Label Hidden",
        options=[
            "Complete Platform View",
            "Performance Intelligence",
            "Classification Distribution",
            "Model Architecture",
            "Scientific Features",
            "Verification Center",
            "Prediction Explorer",
            "Project Specifications & Docs"
        ],
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

    # Compact Sidebar Telemetry Card
    card_bg = "#FFFFFF" if st.session_state.theme == "light" else "#131D2E"
    border_col = "#E5EAF1" if st.session_state.theme == "light" else "#1E2D44"
    val_col = "#172033" if st.session_state.theme == "light" else "#F1F5F9"

    st.markdown(f"""
    <div style="background-color: {card_bg}; border: 1px solid {border_col}; border-radius: 8px; padding: 14px; font-size: 0.8rem; box-shadow: 0 1px 2px rgba(16, 24, 40, 0.03);">
        <div style="font-weight: 700; text-transform: uppercase; font-size: 0.72rem; color: {primary_blue}; margin-bottom: 8px; letter-spacing: 0.04em;">
            System Telemetry
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
            <span style="color: {brand_sub};">Candidate:</span>
            <span style="font-family: 'JetBrains Mono'; font-weight: 600; color: {val_col};">submission_FINAL.csv</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
            <span style="color: {brand_sub};">Local Audit:</span>
            <span style="color: #059669; font-weight: 700;">14/14 PASS</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
            <span style="color: {brand_sub};">Holdout F1:</span>
            <span style="font-family: 'JetBrains Mono'; font-weight: 600; color: #0284C7;">0.5956</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
            <span style="color: {brand_sub};">OOF Macro F1:</span>
            <span style="font-family: 'JetBrains Mono'; font-weight: 600; color: #6366F1;">0.5915</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <span style="color: {brand_sub};">Test Targets:</span>
            <span style="font-family: 'JetBrains Mono'; color: {val_col};">7,000</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="margin-top: 18px; font-size: 0.72rem; color: {brand_sub}; text-align: center; line-height: 1.4;">
        Planet Hunters • Hack4Hack 2026<br>
        Scientific Intelligence UI v3.0
    </div>
    """, unsafe_allow_html=True)

# Main Application Routing
theme = st.session_state.theme

if view_mode == "Complete Platform View":
    render_hero(theme)
    render_performance(theme)
    st.markdown("<div style='margin-bottom: 28px;'></div>", unsafe_allow_html=True)
    render_classification(theme)
    st.markdown("<div style='margin-bottom: 28px;'></div>", unsafe_allow_html=True)
    render_architecture(theme)
    st.markdown("<div style='margin-bottom: 28px;'></div>", unsafe_allow_html=True)
    render_features(theme)
    st.markdown("<div style='margin-bottom: 28px;'></div>", unsafe_allow_html=True)
    render_validator(theme)
    st.markdown("<div style='margin-bottom: 28px;'></div>", unsafe_allow_html=True)
    render_explorer(theme)
    st.markdown("<div style='margin-bottom: 28px;'></div>", unsafe_allow_html=True)
    render_info(theme)

elif view_mode == "Performance Intelligence":
    render_hero(theme)
    render_performance(theme)

elif view_mode == "Classification Distribution":
    render_hero(theme)
    render_classification(theme)

elif view_mode == "Model Architecture":
    render_hero(theme)
    render_architecture(theme)

elif view_mode == "Scientific Features":
    render_hero(theme)
    render_features(theme)

elif view_mode == "Verification Center":
    render_hero(theme)
    render_validator(theme)

elif view_mode == "Prediction Explorer":
    render_hero(theme)
    render_explorer(theme)

elif view_mode == "Project Specifications & Docs":
    render_hero(theme)
    render_info(theme)

# Clean Editorial Footer
footer_border = "#E5EAF1" if theme == "light" else "#1E2D44"
footer_text = "#667085" if theme == "light" else "#94A3B8"

st.markdown(f"""
<div style="margin-top: 45px; padding: 22px 0 15px 0; border-top: 1px solid {footer_border}; text-align: center; font-size: 0.78rem; color: {footer_text};">
    Planet Hunters — Find New Worlds in Starlight • ML Challenge Hack4Hack 2026 (Round 1)<br>
    Engineered with Python 3.11, Streamlit, Plotly, LightGBM, and Scikit-Learn • Fully Deterministic & Audited Pipeline
</div>
""", unsafe_allow_html=True)
