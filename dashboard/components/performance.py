"""
Component C & G: Key Model Performance & Error Analysis
Planet Hunters — Scientific Intelligence Platform
Compact KPI cards with equal heights, benchmark progression, and verified error insights.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from dashboard.data_loader import PROJECT_METRICS, MODEL_BENCHMARKS, CLASS_EVALUATION_METRICS
from dashboard.styles import get_plotly_layout, render_html

def render_performance(theme: str = "creamy"):
    """Renders Key Model Performance (Section C) and Model Evaluation & Error Analysis (Section G)."""
    text_primary = "#292D32"
    text_secondary = "#70736F"
    primary_accent = "#647C70"
    secondary_accent = "#A58B65"
    border_col = "#E7E0D3"
    card_bg = "#FFFDF8"

    # =========================================================================
    # SECTION C: KEY MODEL PERFORMANCE (COMPACT KPI CARDS)
    # =========================================================================
    render_html(f"""
    <div style="margin-bottom: 8px;">
        <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; gap: 8px; margin-bottom: 8px;">
            <div>
                <h2>Key Model Performance</h2>
                <div style="color: {text_secondary}; font-size: 0.85rem;">
                    Verified cross-validation metrics across 18,000 training stars.
                    <span style="font-weight: 600; color: {primary_accent};">(Internal offline validation results — not official competition leaderboard scores)</span>
                </div>
            </div>
            <span class="badge-status badge-neutral">
                5-Fold Stratified + Detector-Channel Holdout
            </span>
        </div>
    </div>
    """)

    # 5 Compact, Equal-Height KPI Cards
    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:
        render_html(f"""
        <div class="metric-container" style="border-top: 3px solid {primary_accent};">
            <div class="metric-label">Standard OOF F1</div>
            <div class="metric-value" style="color: {primary_accent};">{PROJECT_METRICS['champion_oof_f1']:.4f}</div>
            <div class="metric-caption">18,000 Out-Of-Fold Stars</div>
        </div>
        """)

    with k2:
        render_html(f"""
        <div class="metric-container" style="border-top: 3px solid {secondary_accent};">
            <div class="metric-label">Detector OOF F1</div>
            <div class="metric-value" style="color: {secondary_accent};">{PROJECT_METRICS['detector_oof_f1']:.4f}</div>
            <div class="metric-caption">Hardware Holdout Transfer</div>
        </div>
        """)

    with k3:
        render_html(f"""
        <div class="metric-container">
            <div class="metric-label">Training Dataset</div>
            <div class="metric-value">{PROJECT_METRICS['training_stars']:,}</div>
            <div class="metric-caption">8 Balanced Classes</div>
        </div>
        """)

    with k4:
        render_html(f"""
        <div class="metric-container">
            <div class="metric-label">Test Predictions</div>
            <div class="metric-value">{PROJECT_METRICS['test_stars']:,}</div>
            <div class="metric-caption">Deterministic Outputs</div>
        </div>
        """)

    with k5:
        render_html(f"""
        <div class="metric-container">
            <div class="metric-label">Target Taxonomy</div>
            <div class="metric-value">{PROJECT_METRICS['classes_count']} Classes</div>
            <div class="metric-caption">Macro F1 Metric</div>
        </div>
        """)

    render_html("<div style='margin-bottom: 24px;'></div>")

    # =========================================================================
    # SECTION G: MODEL EVALUATION & ERROR ANALYSIS
    # =========================================================================
    render_html(f"""
    <div style="margin-bottom: 12px;">
        <h2>Model Evaluation & Error Analysis</h2>
        <div style="color: {text_secondary}; font-size: 0.85rem;">
            Empirical benchmark progression, class-wise F1 distribution, and astrophysical decision boundary analysis.
        </div>
    </div>
    """)

    col_bench, col_perclass = st.columns([1.1, 1.0])

    with col_bench:
        df_bm = pd.DataFrame(MODEL_BENCHMARKS)
        bar_colors = ["#A58B65", "#8A939E", "#5B7C99", "#738A58", "#647C70"]
        labels = [
            "ExtraTrees<br>(Baseline)",
            "CatBoost",
            "HistGradient<br>Boosting",
            "LightGBM<br>(Single)",
            "Phase 5<br>Champion"
        ]

        fig_bench = go.Figure()
        fig_bench.add_trace(go.Bar(
            x=labels,
            y=df_bm["macro_f1"].iloc[:5],
            text=[f"<b>{val:.4f}</b>" for val in df_bm["macro_f1"].iloc[:5]],
            textposition="outside",
            textfont={"family": "JetBrains Mono, monospace", "size": 11, "color": text_primary},
            marker=dict(color=bar_colors, line=dict(color="#E7E0D3", width=1)),
            hovertemplate="<b>%{x}</b><br>Macro F1: <b>%{y:.4f}</b><extra></extra>"
        ))

        bench_layout = get_plotly_layout(theme)
        bench_layout.update({
            "title": "Model Architecture Progression (Macro F1)",
            "yaxis": {
                "range": [0.48, 0.68],
                "title": "Macro F1 Score",
                "gridcolor": bench_layout["yaxis"]["gridcolor"],
                "tickformat": ".3f"
            },
            "xaxis": {"title": None, "tickfont": {"size": 11, "family": "Inter, sans-serif"}},
            "height": 380,
            "margin": {"l": 50, "r": 20, "t": 35, "b": 50}
        })
        fig_bench.update_layout(bench_layout)
        st.plotly_chart(fig_bench, use_container_width=True, config={"displayModeBar": False})

    with col_perclass:
        df_cls = pd.DataFrame(CLASS_EVALUATION_METRICS).sort_values("f1", ascending=True)

        fig_cls = go.Figure()
        fig_cls.add_trace(go.Bar(
            y=df_cls["class"],
            x=df_cls["f1"],
            orientation='h',
            text=[f" <b>{val:.4f}</b>" for val in df_cls["f1"]],
            textposition='outside',
            textfont={"family": "JetBrains Mono, monospace", "size": 10, "color": text_primary},
            marker=dict(color="#647C70", line=dict(color="#E7E0D3", width=1)),
            hovertemplate="Class: <b>%{y}</b><br>Validation F1: <b>%{x:.4f}</b><extra></extra>"
        ))

        cls_layout = get_plotly_layout(theme)
        cls_layout.update({
            "title": "Class-Wise Out-of-Fold F1 Score (18,000 Stars)",
            "xaxis": {
                "range": [0, 0.95],
                "title": "Macro F1",
                "gridcolor": cls_layout["xaxis"]["gridcolor"]
            },
            "yaxis": {"title": None, "tickfont": {"family": "JetBrains Mono, monospace", "size": 10}},
            "height": 380,
            "margin": {"l": 135, "r": 45, "t": 35, "b": 50}
        })
        fig_cls.update_layout(cls_layout)
        st.plotly_chart(fig_cls, use_container_width=True, config={"displayModeBar": False})

    # Error Analysis Insights Cards (3 equal columns)
    err1, err2, err3 = st.columns(3)

    with err1:
        render_html(f"""
        <div class="ph-card" style="height: 100%; min-height: 175px;">
            <div style="font-weight: 600; font-size: 0.90rem; color: {primary_accent}; margin-bottom: 6px;">
                Planet vs. Quiet Star Boundary
            </div>
            <p style="margin: 0; font-size: 0.82rem; color: {text_secondary}; line-height: 1.55;">
                Shallow exoplanetary transit depths (&Delta;F/F &asymp; 0.05%) closely approach the photon shot-noise floor of quiet stars. 
                Transit-search BLS signal-to-noise ratio and in-dip variance clustering provide the primary statistical discriminator.
            </p>
        </div>
        """)

    with err2:
        render_html(f"""
        <div class="ph-card" style="height: 100%; min-height: 175px;">
            <div style="font-weight: 600; font-size: 0.90rem; color: {secondary_accent}; margin-bottom: 6px;">
                Starspots vs. Quiet Star Modulation
            </div>
            <p style="margin: 0; font-size: 0.82rem; color: {text_secondary}; line-height: 1.55;">
                Long-period, low-amplitude starspot modulation can be confused with stationary quiet stars. 
                Autocorrelation lag analysis and Von Neumann variability ratios isolate coherent rotational trends from random white noise.
            </p>
        </div>
        """)

    with err3:
        render_html(f"""
        <div class="ph-card" style="height: 100%; min-height: 175px;">
            <div style="font-weight: 600; font-size: 0.90rem; color: #5B7C99; margin-bottom: 6px;">
                Detector Domain Shift Mitigation
            </div>
            <p style="margin: 0; font-size: 0.82rem; color: {text_secondary}; line-height: 1.55;">
                Different telescope CCD cameras induce channel-specific photometric drifts. 
                Camera/epoch common-mode cotrending reduced Kolmogorov-Smirnov train-to-test drift by 60.3%, lifting detector OOF F1 from 0.42 to 0.6336.
            </p>
        </div>
        """)
