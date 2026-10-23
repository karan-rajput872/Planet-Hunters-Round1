"""
Component F: Feature Engineering & Astrophysical Inductive Biases
Planet Hunters — Scientific Intelligence Platform
88 domain-informed features across 4 pillars, ablation evidence, and interactive signature visualizer.
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dashboard.data_loader import FEATURE_GROUP_ABLATIONS
from dashboard.styles import get_plotly_layout, get_class_colors

def render_features(theme: str = "creamy"):
    """Renders Section F: Feature Engineering Pillars, Ablation Evidence, and Phenomenon Explorer."""
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
                <h2>Feature Engineering & Astrophysical Biases</h2>
                <div style="color: {text_secondary}; font-size: 0.85rem;">
                    Physics-informed feature extraction: Transforming 1,315 flux cadences into 88 diagnostic descriptors.
                </div>
            </div>
            <span class="badge-status badge-telemetry">
                88 Engineered Features • 4 Pillars
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4 Feature Pillar Cards (Equal Height Grid)
    p1, p2, p3, p4 = st.columns(4)

    with p1:
        st.markdown(f"""
        <div class="ph-card" style="height: 100%; min-height: 220px; border-top: 3px solid #5B7C99;">
            <div style="color: #5B7C99; font-weight: 700; text-transform: uppercase; font-size: 0.70rem; margin-bottom: 2px;">
                Pillar 1 • 32 Features
            </div>
            <div style="font-weight: 600; font-size: 0.92rem; color: {text_primary}; margin-bottom: 6px;">
                Cotrended Summary Stats
            </div>
            <div style="font-size: 0.78rem; color: {text_secondary}; line-height: 1.5;">
                • <strong>MAD Variance</strong>: Scale estimator immune to single-epoch cosmic rays.<br>
                • <strong>Percentile Spreads</strong>: P95-P5 and P99-P1 robust dynamic ranges.<br>
                • <strong>Common-Mode Residuals</strong>: Normalized baseline deviations.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with p2:
        st.markdown(f"""
        <div class="ph-card" style="height: 100%; min-height: 220px; border-top: 3px solid {primary_accent};">
            <div style="color: {primary_accent}; font-weight: 700; text-transform: uppercase; font-size: 0.70rem; margin-bottom: 2px;">
                Pillar 2 • 24 Features
            </div>
            <div style="font-weight: 600; font-size: 0.92rem; color: {text_primary}; margin-bottom: 6px;">
                Flux Distribution Moments
            </div>
            <div style="font-size: 0.78rem; color: {text_secondary}; line-height: 1.5;">
                • <strong>Robust Skewness</strong>: Negative skew isolates dips; positive skew flags flares.<br>
                • <strong>Kurtosis & Heavy Tails</strong>: Distinguishes impulses from Gaussian noise.<br>
                • <strong>Binned Histogram Moments</strong>: Quantifies multimodal flux states.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with p3:
        st.markdown(f"""
        <div class="ph-card" style="height: 100%; min-height: 220px; border-top: 3px solid {secondary_accent};">
            <div style="color: {secondary_accent}; font-weight: 700; text-transform: uppercase; font-size: 0.70rem; margin-bottom: 2px;">
                Pillar 3 • 16 Features
            </div>
            <div style="font-weight: 600; font-size: 0.92rem; color: {text_primary}; margin-bottom: 6px;">
                Transit BLS & Morphology
            </div>
            <div style="font-size: 0.78rem; color: {text_secondary}; line-height: 1.5;">
                • <strong>BLS Transit SNR</strong>: Significance of periodic square-well dips.<br>
                • <strong>Transit Duration & Depth</strong>: Separates planetary dips from binary eclipses.<br>
                • <strong>Fourier Harmonics</strong>: Peaks isolating pulsating stars (Cepheids, RR Lyrae).
            </div>
        </div>
        """, unsafe_allow_html=True)

    with p4:
        st.markdown(f"""
        <div class="ph-card" style="height: 100%; min-height: 220px; border-top: 3px solid #738A58;">
            <div style="color: #738A58; font-weight: 700; text-transform: uppercase; font-size: 0.70rem; margin-bottom: 2px;">
                Pillar 4 • 16 Features
            </div>
            <div style="font-weight: 600; font-size: 0.92rem; color: {text_primary}; margin-bottom: 6px;">
                Centroid Astrometry
            </div>
            <div style="font-size: 0.78rem; color: {text_secondary}; line-height: 1.5;">
                • <strong>In-Dip vs. Out-of-Dip Drift</strong>: Center-of-light spatial shift during transit.<br>
                • <strong>Background Binary Rejection</strong>: Genuine planets show &Delta;centroid &asymp; 0.<br>
                • <strong>2D Centroid Variance</strong>: Flags optical spacecraft pointing jitter.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    # Interactive Phenomenon Lightcurve Explorer
    st.markdown(f"""
    <div class="ph-card">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 12px;">
            <div style="font-weight: 600; font-size: 0.95rem; color: {text_primary};">
                Interactive Phenomenological Lightcurve Explorer
            </div>
            <span class="badge-status badge-neutral" style="font-size: 0.72rem;">
                Scientific Simulation • Diagnostic Profiles
            </span>
        </div>
    """, unsafe_allow_html=True)

    phenomenon_choice = st.selectbox(
        "Select an astronomical phenomenon to inspect its characteristic photometric profile and extracted features:",
        [
            "Planetary Transit (Periodic Flat-Bottomed U-Dip, Zero Centroid Shift)",
            "Eclipsing Binary (Deep Alternating Primary & Secondary V-Eclipses)",
            "Pulsating Star (Coherent Multi-Periodic Sinusoidal Stellar Oscillation)",
            "Stellar Flare (Instantaneous Positive Spike with Exponential Cooling)",
            "Background Binary (Transit-Like Dip with Significant In-Dip Centroid Offset)",
            "Instrument Glitch (Single-Point Discontinuity / Cosmic Ray Hit)"
        ]
    )

    # Generate synthetic illustrative lightcurves
    np.random.seed(42)
    time = np.linspace(0, 30, 600)
    base_flux = np.ones_like(time) + np.random.normal(0, 0.003, size=len(time))
    plot_color = primary_accent

    if "Planetary Transit" in phenomenon_choice:
        # Periodic flat-bottomed U-dip
        period = 7.5
        phase = (time % period) / period
        in_transit = np.abs(phase - 0.5) < 0.04
        base_flux[in_transit] -= 0.025
        plot_color = "#4E7A68"
        desc = "Authentic exoplanet transit: Periodic, flat-bottomed U-dip with 2.5% depth. The centroid astrometry remains strictly centered (&Delta;centroid &asymp; 0) throughout the dip."

    elif "Eclipsing Binary" in phenomenon_choice:
        period = 6.0
        phase = (time % period) / period
        primary = np.abs(phase - 0.25) < 0.05
        secondary = np.abs(phase - 0.75) < 0.04
        base_flux[primary] -= 0.15
        base_flux[secondary] -= 0.06
        plot_color = "#5B7C99"
        desc = "Eclipsing binary: Alternating deep primary (15%) and secondary (6%) V-shaped eclipses representing mutual occultation of two gravitationally bound stars."

    elif "Pulsating Star" in phenomenon_choice:
        base_flux += 0.04 * np.sin(2 * np.pi * time / 1.8) + 0.015 * np.sin(2 * np.pi * time / 3.4)
        plot_color = "#738A58"
        desc = "Pulsating variable star: Coherent multi-periodic sinusoidal oscillation driving high Fourier harmonic peak power across characteristic pulsation modes."

    elif "Stellar Flare" in phenomenon_choice:
        flare_mask = (time > 12.0) & (time < 18.0)
        base_flux[flare_mask] += 0.18 * np.exp(-(time[flare_mask] - 12.0) / 1.2)
        plot_color = "#B85D43"
        desc = "Stellar magnetic flare: Violent magnetic reconnection triggering a rapid, near-instantaneous flux eruption followed by exponential radiative cooling."

    elif "Background Binary" in phenomenon_choice:
        period = 9.0
        phase = (time % period) / period
        in_transit = np.abs(phase - 0.5) < 0.03
        base_flux[in_transit] -= 0.035
        plot_color = "#8B7A9E"
        desc = "Background false-positive binary: The light curve exhibits a transit-like 3.5% dip, but centroid astrometry reveals a simultaneous >4&sigma; center-of-light spatial offset."

    else:
        # Instrument glitch
        base_flux[280] -= 0.22
        plot_color = "#8A939E"
        desc = "Instrument glitch: Single-cadence unphysical drop caused by spacecraft thruster fire, cosmic ray hit, or readout anomaly. Flagged by extreme Von Neumann variability ratio."

    fig_sim = go.Figure()
    fig_sim.add_trace(go.Scatter(
        x=time,
        y=base_flux,
        mode='lines',
        line=dict(color=plot_color, width=1.5),
        name='Relative Flux',
        hovertemplate='Time: %{x:.2f} d<br>Relative Flux: %{y:.4f}<extra></extra>'
    ))

    layout_sim = get_plotly_layout(theme)
    layout_sim.update({
        "title": f"Simulated Profile: {phenomenon_choice.split('(')[0].strip()}",
        "xaxis": {"title": "Observational Epoch (Days)", "gridcolor": layout_sim["xaxis"]["gridcolor"]},
        "yaxis": {"title": "Normalized Relative Flux", "gridcolor": layout_sim["yaxis"]["gridcolor"]},
        "height": 300,
        "margin": {"l": 55, "r": 20, "t": 35, "b": 35}
    })
    fig_sim.update_layout(layout_sim)
    st.plotly_chart(fig_sim, use_container_width=True, config={"displayModeBar": False})

    st.markdown(f"""
    <div style="font-size: 0.82rem; color: {text_secondary}; line-height: 1.5; padding-top: 4px;">
        <strong>Astrophysical Interpretation:</strong> {desc}
    </div>
    </div>
    """, unsafe_allow_html=True)

    # Feature Group Ablation Table
    st.markdown("<h3 style='margin-top: 20px; margin-bottom: 10px;'>Empirical Feature Group Ablation Evidence</h3>", unsafe_allow_html=True)
    df_ablation = pd.DataFrame(FEATURE_GROUP_ABLATIONS)

    st.markdown(f"""
    <div class="ph-card" style="padding: 14px 18px;">
        <table style="width: 100%; border-collapse: collapse; font-size: 0.82rem; color: {text_primary};">
            <thead>
                <tr style="border-bottom: 2px solid {border_col}; text-align: left;">
                    <th style="padding: 8px 6px; color: {text_secondary};">Feature Pipeline Configuration</th>
                    <th style="padding: 8px 6px; color: {text_secondary};">Count</th>
                    <th style="padding: 8px 6px; color: {text_secondary};">OOF Macro F1</th>
                    <th style="padding: 8px 6px; color: {text_secondary};">&Delta; F1</th>
                    <th style="padding: 8px 6px; color: {text_secondary};">Empirical Impact</th>
                </tr>
            </thead>
            <tbody>
    """, unsafe_allow_html=True)

    table_rows = ""
    for idx, row in df_ablation.iterrows():
        is_champion = (idx == 0)
        bg = "background-color: #EAEFE8;" if is_champion else ""
        font_weight = "font-weight: 700;" if is_champion else ""
        delta_color = primary_accent if is_champion else "#B85D43"
        table_rows += f"""
        <tr style="border-bottom: 1px solid {border_col}; {bg}">
            <td style="padding: 8px 6px; {font_weight}">{row['group']}</td>
            <td style="padding: 8px 6px; font-family: 'JetBrains Mono';">{row['features']}</td>
            <td style="padding: 8px 6px; font-family: 'JetBrains Mono'; {font_weight}">{row['oof_f1']:.4f}</td>
            <td style="padding: 8px 6px; font-family: 'JetBrains Mono'; color: {delta_color}; font-weight: 600;">{row['delta']}</td>
            <td style="padding: 8px 6px; color: {text_secondary}; font-size: 0.78rem;">{row['note']}</td>
        </tr>
        """

    st.markdown(f"{table_rows}</tbody></table></div>", unsafe_allow_html=True)
