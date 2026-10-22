"""
Component E: Scientific Feature Exploration
Explanatory Astrophysical Domain Features & Physics Lightcurve Simulation
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from dashboard.styles import get_plotly_layout, get_class_colors

def render_features(theme: str = "light"):
    """Renders scientific feature extraction concepts and illustrative physical profiles."""
    sub_color = "#94A3B8" if theme == "dark" else "#667085"
    card_bg = "#131D2E" if theme == "dark" else "#FFFFFF"
    border_col = "#1E2D44" if theme == "dark" else "#E5EAF1"
    text_col = "#F1F5F9" if theme == "dark" else "#172033"
    class_colors = get_class_colors(theme)

    st.markdown(f"""
    <div class="ph-card ph-card-accent">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
            <div>
                <h2>Scientific Feature Exploration</h2>
                <p style="margin: 0; color: {sub_color}; font-size: 0.88rem;">
                    Physics-informed feature engineering: Translating raw photometric timeseries and centroids into diagnostic features.
                </p>
            </div>
            <span class="badge-status badge-neutral">
                Domain-Specific Inductive Biases
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Core Feature Pillar Cards
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="metric-container" style="min-height: 180px; border-top: 3px solid #0284C7;">
            <div style="color: #0284C7; font-weight: 700; text-transform: uppercase; font-size: 0.74rem;">Pillar 1 • Photometry</div>
            <div style="font-family: 'Space Grotesk'; font-size: 1.05rem; font-weight: 700; color: {text_col}; margin: 4px 0 6px 0;">
                Variability & Moments
            </div>
            <div style="font-size: 0.78rem; color: {sub_color}; line-height: 1.5;">
                • <strong>MAD (Median Absolute Deviation)</strong>: Robust variance scale immune to cosmic ray spikes.<br>
                • <strong>Robust Skew & Kurtosis</strong>: Asymmetry flags separating sudden dips from eruptive flares.<br>
                • <strong>Von Neumann Ratio (η)</strong>: Successive variance ratio identifying smooth non-random trends.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-container" style="min-height: 180px; border-top: 3px solid #6366F1;">
            <div style="color: #6366F1; font-weight: 700; text-transform: uppercase; font-size: 0.74rem;">Pillar 2 • Morphology</div>
            <div style="font-family: 'Space Grotesk'; font-size: 1.05rem; font-weight: 700; color: {text_col}; margin: 4px 0 6px 0;">
                Transit & Periodic Search
            </div>
            <div style="font-size: 0.78rem; color: {sub_color}; line-height: 1.5;">
                • <strong>Box Least Squares (BLS) SNR</strong>: Statistical peak significance of periodic square dips.<br>
                • <strong>Transit Depth & Duration</strong>: Differentiates gas giant transits from deep stellar eclipses.<br>
                • <strong>Fourier Peak Power</strong>: Dominant harmonics isolating pulsating stars (Cepheids, RR Lyrae).
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-container" style="min-height: 180px; border-top: 3px solid #059669;">
            <div style="color: #059669; font-weight: 700; text-transform: uppercase; font-size: 0.74rem;">Pillar 3 • Astrometry</div>
            <div style="font-family: 'Space Grotesk'; font-size: 1.05rem; font-weight: 700; color: {text_col}; margin: 4px 0 6px 0;">
                Centroid Astrometry
            </div>
            <div style="font-size: 0.78rem; color: {sub_color}; line-height: 1.5;">
                • <strong>In-Dip vs Out-Of-Dip Centroid Offset</strong>: Vector drift of light center during flux minimum.<br>
                • <strong>Background Binary Rejection</strong>: Genuine planets show Δcentroid ≈ 0; blended background binaries exhibit Δcentroid > 3σ.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)

    # Interactive Illustrative Physical Signature Visualizer
    st.markdown(f"""
    <div style="background-color: {card_bg}; border: 1px solid {border_col}; border-radius: 8px; padding: 20px; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 14px;">
            <h4 style="margin: 0; color: {text_col}; font-size: 1.05rem;">Interactive Phenomenological Lightcurve Explorer</h4>
            <span class="badge-status badge-neutral" style="font-size: 0.74rem;">
                ILLUSTRATIVE SIMULATION — Used for Feature Validation
            </span>
        </div>
    """, unsafe_allow_html=True)

    selected_phenomenon = st.selectbox(
        "Select an astrophysical or instrumental phenomenon to inspect its lightcurve and extracted diagnostic features:",
        [
            "Planetary Transit (U-Shaped Dip, Zero Centroid Shift)",
            "Pulsating Star (Multi-Periodic Sinusoidal Stellar Oscillation)",
            "Background Eclipsing Binary (V-Shaped Dip + Significant Centroid Offset)",
            "Stellar Flare (Fast Rise, Exponential Decay Asymmetry)",
            "Starspot Modulation (Quasi-Sinusoidal Rotational Variability)",
            "Instrument Glitch (Instantaneous Sharp Anomaly)"
        ],
        index=0
    )

    t = np.linspace(0, 30, 600)
    np.random.seed(42)
    noise = np.random.normal(0, 0.0012, len(t))

    if "Planetary Transit" in selected_phenomenon:
        flux = np.ones_like(t)
        for dip_center in [6, 16, 26]:
            in_transit = np.abs(t - dip_center) < 0.35
            flux[in_transit] -= 0.015
        flux += noise
        feature_focus = (
            "• <strong>Transit Depth:</strong> 0.0150 (1.5%)<br>"
            "• <strong>Box SNR:</strong> 18.42σ (High Significance Periodicity)<br>"
            "• <strong>Centroid Shift:</strong> 0.0021 px (Negligible → On-Target Planet Candidate)"
        )
        accent_color = class_colors["planet"]
        title_text = "Simulated Lightcurve: Planetary Transit (Exoplanet Signature)"

    elif "Pulsating Star" in selected_phenomenon:
        # Multi-periodic acoustic pulsation modes (Cepheid / Delta Scuti pattern)
        flux = 1.0 + 0.035 * np.sin(2 * np.pi * t / 2.4) + 0.015 * np.sin(4 * np.pi * t / 2.4) + 0.008 * np.sin(2 * np.pi * t / 0.8) + noise
        feature_focus = (
            "• <strong>Dominant Period:</strong> 2.40 days (Fundamental Acoustic Mode)<br>"
            "• <strong>Fourier Power Ratio (f2/f1):</strong> 0.428 (Harmonic Overtone)<br>"
            "• <strong>Centroid In-Dip Offset:</strong> 0.0015 px (Intrinsic Stellar Pulsation)"
        )
        accent_color = class_colors["pulsating_star"]
        title_text = "Simulated Lightcurve: Pulsating Star (Multi-Harmonic Stellar Oscillation)"

    elif "Background Eclipsing Binary" in selected_phenomenon:
        flux = np.ones_like(t)
        for dip_center in [7, 19]:
            dist = np.abs(t - dip_center)
            in_transit = dist < 0.6
            flux[in_transit] -= 0.045 * (1 - dist[in_transit]/0.6)
        flux += noise
        feature_focus = (
            "• <strong>Eclipse Depth:</strong> 0.0450 (Deep V-Shape)<br>"
            "• <strong>In-Dip Centroid Offset:</strong> 0.065 px (Heavy Astrometric Shift)<br>"
            "• <strong>Diagnostic Verdict:</strong> Background False Positive (Blended neighboring binary)"
        )
        accent_color = class_colors["background_binary"]
        title_text = "Simulated Lightcurve: Background Eclipsing Binary (Centroid Shift False Positive)"

    elif "Stellar Flare" in selected_phenomenon:
        flux = np.ones_like(t)
        flare_time = 12.0
        decay_mask = t >= flare_time
        flux[decay_mask] += 0.055 * np.exp(-(t[decay_mask] - flare_time) / 1.1)
        flux += noise
        feature_focus = (
            "• <strong>Peak Flare Amplitude:</strong> +0.0550 (+5.5% Flux Rise)<br>"
            "• <strong>Decay Half-Life:</strong> 0.76 days (Magnetic Reconnection Decay)<br>"
            "• <strong>Robust Skewness:</strong> +3.85 (Strong Positive Asymmetry)"
        )
        accent_color = class_colors["flare_star"]
        title_text = "Simulated Lightcurve: Stellar Flare (Magnetic Eruption)"

    elif "Starspot" in selected_phenomenon:
        flux = 1.0 + 0.02 * np.sin(2 * np.pi * t / 7.2) + 0.006 * np.sin(4 * np.pi * t / 7.2) + noise
        feature_focus = (
            "• <strong>Rotation Period:</strong> 7.20 days (Lomb-Scargle Peak)<br>"
            "• <strong>Modulation Amplitude:</strong> 2.0% Peak-to-Peak<br>"
            "• <strong>Von Neumann Ratio (η):</strong> 0.042 (Strong Smooth Autocorrelation)"
        )
        accent_color = class_colors["starspots"]
        title_text = "Simulated Lightcurve: Starspot Modulation (Stellar Rotation)"

    else:
        flux = np.ones_like(t) + noise
        flux[240] -= 0.075
        flux[241:245] += 0.035
        feature_focus = (
            "• <strong>Point Discontinuity Score:</strong> 12.8 (Single Cadence Delta)<br>"
            "• <strong>Duration:</strong> 1 cadence (Non-astrophysical impulse)<br>"
            "• <strong>Glitch Flag:</strong> Positive (Detector anomaly / cosmic ray hit)"
        )
        accent_color = class_colors["instrument_glitch"]
        title_text = "Simulated Lightcurve: Instrument Glitch (Pixel Desync)"

    # Plotly Figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=t,
        y=flux,
        mode='lines',
        name='Relative Flux',
        line=dict(color=accent_color, width=1.8),
        hovertemplate="Time: %{x:.2f} d<br>Flux: %{y:.4f}<extra></extra>"
    ))

    chart_layout = get_plotly_layout(theme)
    chart_layout.update({
        "title": title_text,
        "xaxis": {"title": "Observation Time (Days)", "gridcolor": chart_layout["xaxis"]["gridcolor"]},
        "yaxis": {"title": "Normalized Relative Flux", "gridcolor": chart_layout["yaxis"]["gridcolor"]},
        "height": 330,
        "margin": {"l": 55, "r": 20, "t": 35, "b": 40}
    })
    fig.update_layout(chart_layout)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Extracted feature diagnostic panel
    st.markdown(f"""
    <div style="background-color: {'#0F172A' if theme=='dark' else '#F8FAFC'}; border-left: 3px solid {accent_color}; border-radius: 6px; padding: 12px 16px; margin-top: 10px; font-size: 0.84rem; color: {text_col};">
        <span style="font-weight: 700; color: {accent_color}; text-transform: uppercase; font-size: 0.74rem;">Extracted Pipeline Features for this Signature:</span>
        <div style="margin-top: 6px; line-height: 1.6;">
            {feature_focus}
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)
