"""
Component E: Model Architecture & Inference Pipeline
Planet Hunters — Scientific Intelligence Platform
Tri-architecture ensemble (50% LGB + 40% HGB + 10% CB), 4-stage flow, and architecture visual.
"""

import streamlit as st
from pathlib import Path
from dashboard.styles import render_html

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ARCH_IMAGE_PORTFOLIO = PROJECT_ROOT / "assets" / "portfolio" / "architecture_diagram.png"
ARCH_IMAGE_MAIN = PROJECT_ROOT / "assets" / "architecture" / "project_architecture.png"

def render_architecture(theme: str = "creamy"):
    """Renders Section E: Model Architecture & Tri-Ensemble Pipeline."""
    text_primary = "#292D32"
    text_secondary = "#70736F"
    primary_accent = "#647C70"
    secondary_accent = "#A58B65"
    border_col = "#E7E0D3"
    card_bg = "#FFFDF8"

    st.markdown(f"""
    <div style="margin-bottom: 12px;">
        <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; gap: 8px;">
            <div>
                <h2>Model Architecture & Ensemble Pipeline</h2>
                <div style="color: {text_secondary}; font-size: 0.85rem;">
                    Tri-architecture gradient-boosted ensemble with camera/CCD cotrending and 5-fold cross-validation.
                </div>
            </div>
            <div style="display: flex; gap: 6px; flex-wrap: wrap;">
                <span class="badge-status badge-telemetry">5-Fold Stratified Split</span>
                <span class="badge-status badge-passed">50% LGB • 40% HGB • 10% CB</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4-Stage Pipeline Flow (Equal-Height Cards)
    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.markdown(f"""
        <div class="ph-card" style="height: 100%; min-height: 200px; border-top: 3px solid #5B7C99;">
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.70rem; font-weight: 700; color: #5B7C99; margin-bottom: 4px;">
                STAGE 01
            </div>
            <div style="font-weight: 600; font-size: 0.92rem; color: {text_primary}; margin-bottom: 6px;">
                Ingestion & Cotrending
            </div>
            <p style="margin: 0; font-size: 0.78rem; color: {text_secondary}; line-height: 1.5;">
                Ingests 1,315 flux cadences and centroid astrometry. Computes camera-epoch common-mode baselines 
                to eliminate systematic instrumental drift across detector channels.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with s2:
        st.markdown(f"""
        <div class="ph-card" style="height: 100%; min-height: 200px; border-top: 3px solid {primary_accent};">
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.70rem; font-weight: 700; color: {primary_accent}; margin-bottom: 4px;">
                STAGE 02
            </div>
            <div style="font-weight: 600; font-size: 0.92rem; color: {text_primary}; margin-bottom: 6px;">
                88-D Feature Extraction
            </div>
            <p style="margin: 0; font-size: 0.78rem; color: {text_secondary}; line-height: 1.5;">
                Extracts 32 cotrended summary stats, 24 flux distribution moments, 16 temporal transit BLS & autocorrelation descriptors, 
                and 16 CCD centroid motion variance vectors.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with s3:
        st.markdown(f"""
        <div class="ph-card" style="height: 100%; min-height: 200px; border-top: 3px solid {secondary_accent};">
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.70rem; font-weight: 700; color: {secondary_accent}; margin-bottom: 4px;">
                STAGE 03
            </div>
            <div style="font-weight: 600; font-size: 0.92rem; color: {text_primary}; margin-bottom: 6px;">
                5-Fold Cross-Validation
            </div>
            <p style="margin: 0; font-size: 0.78rem; color: {text_secondary}; line-height: 1.5;">
                Stratified 5-fold cross-validation across 18,000 training stars ensures zero data leakage. 
                Dual validation holds out entire detector channels to verify cross-hardware transferability.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with s4:
        st.markdown(f"""
        <div class="ph-card" style="height: 100%; min-height: 200px; border-top: 3px solid #738A58;">
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.70rem; font-weight: 700; color: #738A58; margin-bottom: 4px;">
                STAGE 04
            </div>
            <div style="font-weight: 600; font-size: 0.92rem; color: {text_primary}; margin-bottom: 6px;">
                Tri-Ensemble Soft Voting
            </div>
            <p style="margin: 0; font-size: 0.78rem; color: {text_secondary}; line-height: 1.5;">
                Weighted probability aggregation: 50% LightGBM + 40% HistGradientBoosting + 10% CatBoost. 
                Combines leaf-wise, depth-wise, and symmetric trees to suppress individual model variance.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)

    # Architecture Visual Asset
    arch_image = ARCH_IMAGE_PORTFOLIO if ARCH_IMAGE_PORTFOLIO.is_file() else ARCH_IMAGE_MAIN
    if arch_image.is_file():
        render_html(f"""
        <div style="font-weight: 600; font-size: 0.88rem; color: {text_primary}; margin-bottom: 8px;">
            System Architecture Flowchart
        </div>
        """)
        st.image(str(arch_image), use_container_width=True, caption="Figure 1: Planet Hunters End-to-End Machine Learning Architecture & Prediction Pipeline")
        st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)

    # Tri-Ensemble Models Breakdown (3 Equal Columns)
    m1, m2, m3 = st.columns(3)

    with m1:
        st.markdown(f"""
        <div class="ph-card" style="height: 100%; min-height: 165px; border-top: 3px solid {primary_accent};">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span style="font-weight: 600; font-size: 0.90rem; color: {text_primary};">LightGBM (Leaf-Wise)</span>
                <span style="font-family: 'JetBrains Mono', monospace; font-weight: 700; color: {primary_accent};">50% Weight</span>
            </div>
            <p style="margin: 0; font-size: 0.78rem; color: {text_secondary}; line-height: 1.5;">
                Gradient-based one-side sampling (GOSS) and exclusive feature bundling. Specializes in rapid, highly non-linear decision splits across transit signal metrics.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="ph-card" style="height: 100%; min-height: 165px; border-top: 3px solid {secondary_accent};">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span style="font-weight: 600; font-size: 0.90rem; color: {text_primary};">HistGradientBoosting</span>
                <span style="font-family: 'JetBrains Mono', monospace; font-weight: 700; color: {secondary_accent};">40% Weight</span>
            </div>
            <p style="margin: 0; font-size: 0.78rem; color: {text_secondary}; line-height: 1.5;">
                Scikit-learn native depth-wise histogram binning. Acts as an architectural regularizer, dampening individual deep leaf overfitting on subtle quiet-star noise.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="ph-card" style="height: 100%; min-height: 165px; border-top: 3px solid #738A58;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span style="font-weight: 600; font-size: 0.90rem; color: {text_primary};">CatBoost (Symmetric)</span>
                <span style="font-family: 'JetBrains Mono', monospace; font-weight: 700; color: #738A58;">10% Weight</span>
            </div>
            <p style="margin: 0; font-size: 0.78rem; color: {text_secondary}; line-height: 1.5;">
                Oblivious decision trees with ordered boosting. Provides structural architectural diversity, preventing prediction over-confidence in minority classes.
            </p>
        </div>
        """, unsafe_allow_html=True)
