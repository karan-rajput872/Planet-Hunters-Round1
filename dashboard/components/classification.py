"""
Component D: Astronomical Classification Overview & Taxonomy
Planet Hunters — Scientific Intelligence Platform
Horizontal distribution chart, donut proportions, and equal-height 8-class taxonomy grid.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from dashboard.data_loader import get_class_summary
from dashboard.styles import get_class_colors, get_plotly_layout

def render_classification(theme: str = "creamy"):
    """Renders Section D: 8-Class Distribution Visualizations and Equal-Height Taxonomy Grid."""
    summary_df = get_class_summary()
    total_preds = summary_df["count"].sum()
    class_colors = get_class_colors(theme)
    text_primary = "#292D32"
    text_secondary = "#70736F"
    primary_accent = "#647C70"
    border_col = "#E7E0D3"
    card_bg = "#FFFDF8"

    st.markdown(f"""
    <div style="margin-bottom: 12px;">
        <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; gap: 8px;">
            <div>
                <h2>Classification Overview & Taxonomy</h2>
                <div style="color: {text_secondary}; font-size: 0.85rem;">
                    Full population breakdown across the eight astronomical and instrumental categories.
                </div>
            </div>
            <span class="badge-status badge-telemetry">
                Target Set: {total_preds:,} Predictions
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 1. Distribution Visualizations: Horizontal Bar Chart & Donut Chart
    col_bar, col_donut = st.columns([1.25, 0.95])

    with col_bar:
        df_sorted = summary_df.sort_values("count", ascending=True)
        colors = [class_colors.get(c, primary_accent) for c in df_sorted["class"]]

        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            y=df_sorted["class"],
            x=df_sorted["count"],
            orientation='h',
            text=[f" <b>{cnt:,}</b> ({pct:.1f}%)" for cnt, pct in zip(df_sorted["count"], df_sorted["percentage"])],
            textposition='outside',
            textfont={"family": "Inter, sans-serif", "size": 11, "color": text_primary},
            marker=dict(color=colors, line=dict(color="#E7E0D3", width=1)),
            hovertemplate="<b>%{y}</b><br>Predicted Stars: <b>%{x:,}</b><br>Share: <b>%{customdata:.2f}%</b><extra></extra>",
            customdata=df_sorted["percentage"].values
        ))

        bar_layout = get_plotly_layout(theme)
        bar_layout.update({
            "title": "Predicted Class Distribution (Test Star Counts)",
            "xaxis": {
                "title": "Target Star Count",
                "range": [0, 2400],
                "gridcolor": bar_layout["xaxis"]["gridcolor"]
            },
            "yaxis": {"title": None, "tickfont": {"family": "JetBrains Mono, monospace", "size": 11}},
            "height": 380,
            "margin": {"l": 140, "r": 60, "t": 35, "b": 40}
        })
        fig_bar.update_layout(bar_layout)
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    with col_donut:
        donut_colors = [class_colors.get(c, primary_accent) for c in summary_df["class"]]

        fig_donut = go.Figure()
        fig_donut.add_trace(go.Pie(
            labels=summary_df["class"],
            values=summary_df["count"],
            hole=0.58,
            marker=dict(colors=donut_colors, line=dict(color="#FFFDF8", width=1.5)),
            textinfo='percent',
            textfont={"family": "Inter, sans-serif", "size": 11, "color": text_primary},
            hovertemplate="<b>%{label}</b><br>Count: <b>%{value:,}</b><br>Share: <b>%{percent}</b><extra></extra>",
            rotation=45
        ))

        donut_layout = get_plotly_layout(theme)
        donut_layout.update({
            "title": "Astrophysical Proportions",
            "showlegend": True,
            "legend": {"orientation": "h", "yanchor": "bottom", "y": -0.3, "xanchor": "center", "x": 0.5, "font": {"size": 10}},
            "annotations": [{
                "font": {"family": "Inter, sans-serif", "size": 14, "color": text_primary, "weight": "bold"},
                "showarrow": False,
                "text": f"<b>{total_preds:,}</b><br><span style='font-size:10px;color:{text_secondary};font-weight:normal;'>TARGETS</span>",
                "x": 0.5, "y": 0.5
            }],
            "height": 380,
            "margin": {"l": 20, "r": 20, "t": 35, "b": 60}
        })
        fig_donut.update_layout(donut_layout)
        st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

    # 2. Equal-Sized 8-Class Reference Cards (2 rows of 4 columns)
    st.markdown("<h3 style='margin-top: 14px; margin-bottom: 12px;'>Astrophysical Class Directory & Diagnostic Markers</h3>", unsafe_allow_html=True)

    def render_class_card(row, col_container):
        c_color = class_colors.get(row["class"], primary_accent)
        with col_container:
            st.markdown(f"""
            <div style="background-color: {card_bg}; border: 1px solid {border_col}; border-top: 3px solid {c_color}; border-radius: 8px; padding: 14px 16px; margin-bottom: 16px; min-height: 185px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 1px 2px rgba(41, 45, 50, 0.02);">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: center; gap: 6px; margin-bottom: 4px;">
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.80rem; font-weight: 700; color: {c_color};">
                            {row['class']}
                        </span>
                        <span style="background: #F0EBDD; padding: 1px 6px; border-radius: 4px; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; font-weight: 600; color: {text_secondary};">
                            {row['percentage']:.1f}%
                        </span>
                    </div>
                    <div style="font-size: 0.88rem; font-weight: 600; color: {text_primary}; margin-bottom: 4px;">
                        {row['display']}
                    </div>
                    <p style="margin: 0; font-size: 0.78rem; color: {text_secondary}; line-height: 1.45;">
                        {row['description']}
                    </p>
                </div>
                <div style="margin-top: 8px; padding-top: 6px; border-top: 1px solid {border_col}; font-size: 0.73rem; color: {text_secondary};">
                    <span style="font-weight: 600; color: {c_color};">Key Marker:</span> {row.get('diagnostic_marker', row['signal_shape'])}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # First row: 4 cards
    r1_cols = st.columns(4)
    for i in range(4):
        render_class_card(summary_df.iloc[i], r1_cols[i])

    # Second row: 4 cards
    r2_cols = st.columns(4)
    for i in range(4, 8):
        render_class_card(summary_df.iloc[i], r2_cols[i-4])
