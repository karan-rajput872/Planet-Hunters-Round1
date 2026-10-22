"""
Component A: Mission Overview & Hero Section
Enterprise Scientific Header with 5 Full-Fidelity KPI Cards (No Truncation)
"""

import streamlit as st
from dashboard.data_loader import PROJECT_METRICS

def render_hero(theme: str = "light"):
    """Renders the top Mission Overview and Hero Header."""
    sub_color = "#94A3B8" if theme == "dark" else "#667085"
    primary_color = "#3B82F6" if theme == "dark" else "#2457D6"
    title_color = "#F1F5F9" if theme == "dark" else "#101B33"

    st.markdown(f"""
    <div style="padding: 4px 0 24px 0;">
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px; margin-bottom: 12px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span class="badge-status badge-telemetry">
                    HACK4HACK 2026 • ROUND 1
                </span>
                <span style="font-size: 0.8rem; color: {sub_color};">/</span>
                <span style="font-size: 0.8rem; font-weight: 500; color: {sub_color};">
                    ASTRONOMICAL ML BENCHMARK
                </span>
            </div>
            <div>
                <span class="badge-status badge-passed">
                    ✓ LOCAL VALIDATION PASSED (14/14 CHECKS VERIFIED)
                </span>
            </div>
        </div>
        <h1 style="color: {title_color};">
            PLANET HUNTERS
        </h1>
        <div style="font-size: 1.15rem; font-weight: 600; color: {primary_color}; margin-bottom: 10px; letter-spacing: -0.01em;">
            Find New Worlds in Starlight
        </div>
        <p style="max-width: 920px; margin: 0; color: {sub_color}; font-size: 0.95rem; line-height: 1.6;">
            An astronomical machine-learning platform designed to classify high-precision stellar lightcurves into eight astrophysical
            and instrumental categories. Engineered with domain-specific photometric variability, transit BLS search, and centroid astrometry,
            audited for zero data leakage, and stabilized through a dual 10-estimator probability ensemble.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 5 KPI telemetry cards with robust box-sizing and ZERO truncation
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Training Stars</div>
            <div class="metric-value">{PROJECT_METRICS['training_stars']:,}</div>
            <div class="metric-caption">Labelled Ground Truth</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Test Stars</div>
            <div class="metric-value">{PROJECT_METRICS['test_stars']:,}</div>
            <div class="metric-caption">Unlabelled Targets</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Cadences / Star</div>
            <div class="metric-value">{PROJECT_METRICS['flux_cadences']:,}</div>
            <div class="metric-caption">Photometric Depth</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Classes</div>
            <div class="metric-value">{PROJECT_METRICS['classes_count']}</div>
            <div class="metric-caption">Multi-Class Taxonomy</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
        <div class="metric-container" style="border-left: 3px solid {primary_color};">
            <div class="metric-label">Target Metric</div>
            <div class="metric-value" style="color: {primary_color}; font-size: 1.65rem;">Macro F1</div>
            <div class="metric-caption">Harmonic Mean</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 28px;'></div>", unsafe_allow_html=True)
