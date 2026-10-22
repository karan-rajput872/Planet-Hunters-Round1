"""
Component B: Performance Intelligence & Model Evaluation Suite
Professional ML Validation Report with Benchmark Progression & Per-Class Metrics
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from dashboard.data_loader import PROJECT_METRICS, MODEL_BENCHMARKS, CLASS_EVALUATION_METRICS
from dashboard.styles import get_plotly_layout

def render_performance(theme: str = "light"):
    """Renders Performance Intelligence cards, benchmark progression, and per-class metrics."""
    sub_color = "#94A3B8" if theme == "dark" else "#667085"
    primary_color = "#3B82F6" if theme == "dark" else "#2457D6"
    card_bg = "#131D2E" if theme == "dark" else "#FFFFFF"
    border_col = "#1E2D44" if theme == "dark" else "#E5EAF1"
    text_col = "#F1F5F9" if theme == "dark" else "#172033"

    st.markdown(f"""
    <div class="ph-card ph-card-accent">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
            <div>
                <h2>Performance Intelligence</h2>
                <p style="margin: 0; color: {sub_color}; font-size: 0.88rem;">
                    Internal cross-validation and independent holdout results.
                    <span style="font-weight: 600; color: {primary_color};">Internal offline validation metrics — not competition leaderboard scores.</span>
                </p>
            </div>
            <span class="badge-status badge-neutral">
                Stratified 5-Fold CV + 20% Holdout
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4 Verified Internal Metric Cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-container" style="border-top: 3px solid {primary_color};">
            <div class="metric-label">Champion OOF Macro F1</div>
            <div class="metric-value" style="color: {primary_color};">{PROJECT_METRICS['champion_oof_f1']:.4f}</div>
            <div class="metric-caption">18,000 Out-Of-Fold Blend</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="metric-container" style="border-top: 3px solid #0284C7;">
            <div class="metric-label">5-Fold Mean F1</div>
            <div class="metric-value">{PROJECT_METRICS['cv_mean_f1']:.4f}</div>
            <div class="metric-caption">Cross-Fold Average Score</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="metric-container" style="border-top: 3px solid #6366F1;">
            <div class="metric-label">5-Fold Stability (Std)</div>
            <div class="metric-value">±{PROJECT_METRICS['cv_std_f1']:.4f}</div>
            <div class="metric-caption">Ultra-low Variance Stability</div>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
        <div class="metric-container" style="border-top: 3px solid #059669;">
            <div class="metric-label">Champion Holdout F1</div>
            <div class="metric-value" style="color: #059669;">{PROJECT_METRICS['champion_holdout_f1']:.4f}</div>
            <div class="metric-caption">3,600 Unseen Holdout Stars</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)

    # Two column layout: Benchmark progression chart on Left, Per-Class F1 Breakdown on Right
    col_bench, col_perclass = st.columns([1.1, 1.0])

    with col_bench:
        df_bm = pd.DataFrame(MODEL_BENCHMARKS)
        if theme == "dark":
            bar_colors = ["#475569", "#D97706", "#0284C7", "#6366F1", "#38BDF8"]
        else:
            bar_colors = ["#94A3B8", "#D97706", "#0284C7", "#4F46E5", "#2457D6"]

        # 2-line clean labels to avoid collision and make naming zone crisp & readable
        formatted_labels = [
            "ExtraTrees<br>(Baseline)",
            "CatBoost",
            "HistGradient<br>Boosting",
            "LightGBM<br>(Single)",
            "Champion<br>Dual Ensemble"
        ]

        fig_bench = go.Figure()
        fig_bench.add_trace(go.Bar(
            x=formatted_labels,
            y=df_bm["macro_f1"],
            text=[f"<b>{val:.4f}</b>" for val in df_bm["macro_f1"]],
            textposition="outside",
            textfont={"family": "JetBrains Mono, monospace", "size": 11},
            marker=dict(color=bar_colors, line=dict(color="rgba(0,0,0,0.08)", width=1)),
            hovertemplate=(
                "<b>%{customdata[2]}</b><br>" +
                "Architecture: %{customdata[0]}<br>" +
                "Validation Type: %{customdata[1]}<br>" +
                "Macro F1 Score: <b>%{y:.4f}</b>" +
                "<extra></extra>"
            ),
            customdata=df_bm[["category", "type", "model"]].values
        ))

        # Baseline threshold line
        fig_bench.add_shape(
            type="line", x0=-0.5, x1=4.5, y0=0.5234, y1=0.5234,
            line=dict(color="#94A3B8", width=1, dash="dot")
        )

        bench_layout = get_plotly_layout(theme)
        bench_layout.update({
            "title": "Model Architecture Progression (Validation Macro F1)",
            "yaxis": {
                "range": [0.48, 0.63],
                "title": "Macro F1 Score",
                "gridcolor": bench_layout["yaxis"]["gridcolor"],
                "tickformat": ".3f"
            },
            "xaxis": {
                "title": None,
                "tickangle": 0,
                "tickfont": {"size": 11, "family": "Inter, sans-serif"}
            },
            "height": 390,
            "margin": {"l": 50, "r": 20, "t": 35, "b": 60}
        })
        fig_bench.update_layout(bench_layout)
        st.plotly_chart(fig_bench, use_container_width=True, config={"displayModeBar": False})

    with col_perclass:
        # Per-Class F1 Breakdown Chart (from verified documentation)
        df_cls = pd.DataFrame(CLASS_EVALUATION_METRICS).sort_values("f1", ascending=True)

        fig_cls = go.Figure()
        fig_cls.add_trace(go.Bar(
            y=df_cls["class"],
            x=df_cls["f1"],
            orientation='h',
            text=[f" <b>{val:.4f}</b>" for val in df_cls["f1"]],
            textposition='outside',
            textfont={"family": "JetBrains Mono, monospace", "size": 11},
            marker=dict(
                color=["#059669" if f > 0.65 else "#0284C7" if f > 0.50 else "#D97706" for f in df_cls["f1"]],
                line=dict(color="rgba(0,0,0,0.08)", width=1)
            ),
            hovertemplate=(
                "<b>%{y}</b><br>" +
                "OOF F1-Score: <b>%{x:.4f}</b><br>" +
                "Precision: %{customdata[0]:.4f}<br>" +
                "Recall: %{customdata[1]:.4f}<br>" +
                "True Support: %{customdata[2]:,} stars" +
                "<extra></extra>"
            ),
            customdata=df_cls[["precision", "recall", "support"]].values
        ))

        cls_layout = get_plotly_layout(theme)
        cls_layout.update({
            "title": "Per-Class Out-Of-Fold F1-Score Breakdown",
            "xaxis": {
                "range": [0, 0.88],
                "title": "OOF F1-Score",
                "gridcolor": cls_layout["xaxis"]["gridcolor"],
                "tickformat": ".2f"
            },
            "yaxis": {
                "title": None,
                "tickfont": {"family": "JetBrains Mono, monospace", "size": 11}
            },
            "height": 380,
            "margin": {"l": 140, "r": 40, "t": 35, "b": 50}
        })
        fig_cls.update_layout(cls_layout)
        st.plotly_chart(fig_cls, use_container_width=True, config={"displayModeBar": False})

    # Summary insight pill
    st.markdown("""
    <div class="ph-alert-info">
        <strong>Ensemble Architecture & Optimization Milestone:</strong> The champion solution fuses <strong>5-Fold LightGBM (75% probability weight)</strong>
        with <strong>5-Fold HistGradientBoosting (25% probability weight)</strong>, achieving <strong>+0.0722 (+13.8%) Macro F1 gain</strong> over baseline ExtraTrees
        and outperforming single LightGBM by <strong>+0.0042</strong> on holdout validation.
    </div>
    """, unsafe_allow_html=True)
