"""
Component C: Classification Intelligence & Class Distribution Suite
Pixel-Aligned Grid with Strict Information Hierarchy & Dual Distribution Visualizations
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from dashboard.data_loader import get_class_summary
from dashboard.styles import get_class_colors, get_plotly_layout

def render_classification(theme: str = "light"):
    """Renders population distribution charts and perfectly aligned 8-class reference cards."""
    summary_df = get_class_summary()
    total_preds = summary_df["count"].sum()
    class_colors = get_class_colors(theme)
    sub_color = "#94A3B8" if theme == "dark" else "#667085"
    card_bg = "#131D2E" if theme == "dark" else "#FFFFFF"
    border_col = "#1E2D44" if theme == "dark" else "#E5EAF1"
    text_col = "#F1F5F9" if theme == "dark" else "#172033"
    badge_bg_col = "#1E293B" if theme == "dark" else "#F1F5F9"

    st.markdown(f"""
    <div class="ph-card ph-card-accent">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
            <div>
                <h2>Classification Intelligence</h2>
                <p style="margin: 0; color: {sub_color}; font-size: 0.88rem;">
                    Full population breakdown across the 8 astrophysical and instrumental categories in official test predictions.
                    <span style="font-weight: 500;">(Submission test targets — not training ground truth)</span>
                </p>
            </div>
            <span class="badge-status badge-telemetry">
                Total Predictions: {total_preds:,} Stars
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 1. Distribution Visualizations: Horizontal Bar on Left, Donut Chart on Right
    col_bar, col_donut = st.columns([1.25, 0.95])

    with col_bar:
        # Sort from lowest count to highest for clean horizontal bar chart presentation
        df_sorted = summary_df.sort_values("count", ascending=True)
        colors = [class_colors[c] for c in df_sorted["class"]]

        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            y=df_sorted["class"],
            x=df_sorted["count"],
            orientation='h',
            text=[f" <b>{cnt:,}</b> ({pct:.1f}%)" for cnt, pct in zip(df_sorted["count"], df_sorted["percentage"])],
            textposition='outside',
            textfont={"family": "Inter, sans-serif", "size": 11},
            marker=dict(color=colors, line=dict(color="rgba(0,0,0,0.08)", width=1)),
            hovertemplate=(
                "<b>%{y}</b><br>" +
                "Predicted Stars: <b>%{x:,}</b><br>" +
                "Share of Test Set: <b>%{customdata[0]:.2f}%</b><br>" +
                "Taxonomy: %{customdata[1]}" +
                "<extra></extra>"
            ),
            customdata=df_sorted[["percentage", "type"]].values
        ))

        bar_layout = get_plotly_layout(theme)
        bar_layout.update({
            "title": "Predicted Class Distribution (Test Star Counts)",
            "xaxis": {
                "title": "Number of Target Stars",
                "range": [0, 2450],
                "gridcolor": bar_layout["xaxis"]["gridcolor"]
            },
            "yaxis": {
                "title": None,
                "tickfont": {"family": "JetBrains Mono, monospace", "size": 11}
            },
            "height": 400,
            "margin": {"l": 150, "r": 60, "t": 35, "b": 40}
        })
        fig_bar.update_layout(bar_layout)
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    with col_donut:
        donut_colors = [class_colors[c] for c in summary_df["class"]]

        fig_donut = go.Figure()
        fig_donut.add_trace(go.Pie(
            labels=summary_df["class"],
            values=summary_df["count"],
            hole=0.58,
            marker=dict(
                colors=donut_colors,
                line=dict(color="#131D2E" if theme=="dark" else "#FFFFFF", width=1.5)
            ),
            textinfo='percent',
            textfont={"family": "Inter, sans-serif", "size": 11},
            hovertemplate=(
                "<b>%{label}</b><br>" +
                "Count: <b>%{value:,}</b><br>" +
                "Proportion: <b>%{percent}</b>" +
                "<extra></extra>"
            ),
            rotation=60
        ))

        donut_layout = get_plotly_layout(theme)
        center_color = "#F1F5F9" if theme=="dark" else "#101B33"
        donut_layout.update({
            "title": "Astrophysical Proportions",
            "showlegend": True,
            "legend": {
                "orientation": "h",
                "yanchor": "bottom",
                "y": -0.3,
                "xanchor": "center",
                "x": 0.5,
                "font": {"size": 10}
            },
            "annotations": [
                {
                    "font": {"family": "Space Grotesk, sans-serif", "size": 15, "color": center_color},
                    "showarrow": False,
                    "text": f"<b>7,000</b><br><span style='font-size:10px;color:{sub_color};'>TARGETS</span>",
                    "x": 0.5,
                    "y": 0.5
                }
            ],
            "height": 400,
            "margin": {"l": 20, "r": 20, "t": 35, "b": 70}
        })
        fig_donut.update_layout(donut_layout)
        st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

    # 2. Pixel-Aligned 8-Class Reference Grid (Rendered in 2 strict rows of 4 columns)
    st.markdown("<h3 style='margin-top: 10px; margin-bottom: 14px;'>Astrophysical Class Reference & Population Statistics</h3>", unsafe_allow_html=True)

    # Function to render a single card with uniform layout
    def render_card(row, col_container):
        c_color = class_colors[row["class"]]
        with col_container:
            st.markdown(f"""
            <div style="background-color: {card_bg}; border: 1px solid {border_col}; border-top: 3px solid {c_color}; border-radius: 8px; padding: 16px 18px; margin-bottom: 16px; height: 185px; display: flex; flex-direction: column; justify-content: space-between; overflow: hidden; min-width: 0; box-shadow: 0 1px 2px rgba(16, 24, 40, 0.03);">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: center; gap: 6px; margin-bottom: 6px;">
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; font-weight: 700; color: {c_color}; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="{row['class']}">
                            {row['class']}
                        </span>
                        <span style="background: {badge_bg_col}; padding: 2px 7px; border-radius: 4px; font-family: 'JetBrains Mono', monospace; font-size: 0.74rem; font-weight: 600; color: {sub_color}; white-space: nowrap;">
                            {row['percentage']:.1f}%
                        </span>
                    </div>
                    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.45rem; font-weight: 700; color: {text_col}; margin-bottom: 6px; line-height: 1.1;">
                        {row['count']:,} <span style="font-size: 0.75rem; font-weight: 500; color: {sub_color};">stars</span>
                    </div>
                </div>
                <div style="font-size: 0.76rem; color: {sub_color}; line-height: 1.4; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;" title="{row['description']}">
                    {row['description']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Row 1: Cards 0, 1, 2, 3 (pulsating_star, instrument_glitch, quiet_star, starspots)
    row1_cols = st.columns(4)
    for i in range(4):
        render_card(summary_df.iloc[i], row1_cols[i])

    # Row 2: Cards 4, 5, 6, 7 (eclipsing_binary, planet, flare_star, background_binary)
    row2_cols = st.columns(4)
    for i in range(4, 8):
        render_card(summary_df.iloc[i], row2_cols[i - 4])
