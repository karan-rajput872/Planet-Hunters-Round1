"""
Planet Hunters — Scientific Intelligence Platform
ML Challenge Hack4Hack 2026 — Round 1
Enterprise Astronomical Telemetry & Machine Learning Analytics Dashboard
Warm Creamy Theme • Polished Typography • Equal-Sized Cards • Zero Raw Tracebacks
"""

import sys
from pathlib import Path
import streamlit as st

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dashboard.styles import get_theme_css, render_html
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

# Apply Professional Warm Creamy CSS
render_html(get_theme_css("creamy"))

# Sidebar Navigation & Telemetry
with st.sidebar:
    text_primary = "#292D32"
    text_secondary = "#70736F"
    primary_accent = "#647C70"
    border_col = "#E7E0D3"

    render_html(f"""
    <div style="padding: 2px 0 14px 0; border-bottom: 1px solid {border_col};">
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="width: 32px; height: 32px; border-radius: 6px; background-color: {primary_accent}; color: #FFFDF8; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.95rem; flex-shrink: 0;">
                PH
            </div>
            <div>
                <div style="font-family: 'Inter', sans-serif; font-size: 0.98rem; font-weight: 700; letter-spacing: -0.02em; color: {text_primary};">
                    PLANET HUNTERS
                </div>
                <div style="font-size: 0.70rem; font-weight: 600; color: {text_secondary}; text-transform: uppercase; letter-spacing: 0.05em;">
                    Scientific Intelligence
                </div>
            </div>
        </div>
    </div>
    """)

    render_html("<div style='margin-top: 14px;'></div>")

    # Simplified Public Navigation (Phase 6, 7, 8 completely removed from public UI)
    render_html(f"<div style='font-size: 0.72rem; font-weight: 600; text-transform: uppercase; color: {text_secondary}; margin-bottom: 6px; letter-spacing: 0.04em;'>Platform Navigation</div>")
    view_mode = st.radio(
        "Navigation Station Label Hidden",
        options=[
            "Complete Platform View",
            "Overview & Performance",
            "Classification Taxonomy",
            "Model Architecture",
            "Feature Engineering",
            "Verification Center",
            "Prediction Explorer",
            "Artifacts & Documentation"
        ],
        index=0,
        label_visibility="collapsed"
    )

    render_html("<div style='margin-top: 20px;'></div>")

    # Compact Sidebar Telemetry Card
    render_html(f"""
    <div style="background-color: #FFFDF8; border: 1px solid {border_col}; border-radius: 8px; padding: 12px; font-size: 0.78rem; box-shadow: 0 1px 2px rgba(41, 45, 50, 0.02);">
        <div style="font-weight: 700; text-transform: uppercase; font-size: 0.70rem; color: {primary_accent}; margin-bottom: 8px; letter-spacing: 0.04em;">
            System Telemetry
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
            <span style="color: {text_secondary};">Model:</span>
            <span style="font-family: 'JetBrains Mono'; font-weight: 600; color: {text_primary};">Tri-Ensemble (P5)</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
            <span style="color: {text_secondary};">Audit Status:</span>
            <span style="color: #3F6350; font-weight: 700;">14/14 PASS</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
            <span style="color: {text_secondary};">OOF Macro F1:</span>
            <span style="font-family: 'JetBrains Mono'; font-weight: 600; color: {primary_accent};">0.6455</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
            <span style="color: {text_secondary};">Detector OOF:</span>
            <span style="font-family: 'JetBrains Mono'; font-weight: 600; color: #A58B65;">0.6336</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <span style="color: {text_secondary};">Test Targets:</span>
            <span style="font-family: 'JetBrains Mono'; color: {text_primary};">7,000 Stars</span>
        </div>
    </div>
    """)

    render_html(f"""
    <div style="margin-top: 16px; font-size: 0.70rem; color: {text_secondary}; text-align: center; line-height: 1.45;">
        Planet Hunters • Hack4Hack 2026<br>
        Warm Creamy Scientific UI
    </div>
    """)

# Main Application Routing
theme = "creamy"

if view_mode == "Complete Platform View":
    render_hero(theme)
    render_performance(theme)
    render_html("<div style='margin-bottom: 24px;'></div>")
    render_classification(theme)
    render_html("<div style='margin-bottom: 24px;'></div>")
    render_architecture(theme)
    render_html("<div style='margin-bottom: 24px;'></div>")
    render_features(theme)
    render_html("<div style='margin-bottom: 24px;'></div>")
    render_validator(theme)
    render_html("<div style='margin-bottom: 24px;'></div>")
    render_explorer(theme)
    render_html("<div style='margin-bottom: 24px;'></div>")
    render_info(theme)

elif view_mode == "Overview & Performance":
    render_hero(theme)
    render_performance(theme)

elif view_mode == "Classification Taxonomy":
    render_hero(theme)
    render_classification(theme)

elif view_mode == "Model Architecture":
    render_hero(theme)
    render_architecture(theme)

elif view_mode == "Feature Engineering":
    render_hero(theme)
    render_features(theme)

elif view_mode == "Verification Center":
    render_hero(theme)
    render_validator(theme)

elif view_mode == "Prediction Explorer":
    render_hero(theme)
    render_explorer(theme)

elif view_mode == "Artifacts & Documentation":
    render_hero(theme)
    render_info(theme)

# Editorial Footer
render_html(f"""
<div style="margin-top: 40px; padding: 18px 0 10px 0; border-top: 1px solid {border_col}; text-align: center; font-size: 0.76rem; color: {text_secondary};">
    Planet Hunters — Find New Worlds in Starlight • ML Challenge Hack4Hack 2026 (Round 1)<br>
    Engineered with Python 3.11, Streamlit, Plotly, LightGBM, HistGradientBoosting, and CatBoost • Audited & Reproducible Pipeline
</div>
""")
