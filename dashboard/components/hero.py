"""
Component A & B: Project Header & Scientific Overview
Planet Hunters — Find New Worlds in Starlight
Clean, compact, warm creamy header with zero excessive top whitespace.
"""

import streamlit as st

def render_hero(theme: str = "creamy"):
    """Renders Project Header and Concise Scientific Overview."""
    text_primary = "#292D32"
    text_secondary = "#70736F"
    primary_accent = "#647C70"
    secondary_accent = "#A58B65"
    border_col = "#E7E0D3"
    card_bg = "#FFFDF8"

    st.markdown(f"""
    <div style="padding: 2px 0 16px 0;">
        <!-- Metadata Badges Row -->
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px; margin-bottom: 10px;">
            <div style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
                <span class="badge-status badge-telemetry">
                    Hack4Hack 2026 • Round 1 Completed
                </span>
                <span style="font-size: 0.75rem; color: {text_secondary};">•</span>
                <span style="font-size: 0.78rem; font-weight: 500; color: {text_secondary};">
                    Machine Learning / Astronomy
                </span>
                <span style="font-size: 0.75rem; color: {text_secondary};">•</span>
                <span style="font-size: 0.78rem; font-weight: 500; color: {secondary_accent};">
                    Time-Series Classification
                </span>
            </div>
            <div>
                <span class="badge-status badge-passed">
                    Audited 14/14 Schema & Physics Passed
                </span>
            </div>
        </div>

        <!-- Main Title & Subtitle -->
        <h1 style="color: {text_primary}; margin-bottom: 4px;">
            Planet Hunters
        </h1>
        <div style="font-size: 1.05rem; font-weight: 600; color: {primary_accent}; margin-bottom: 12px; letter-spacing: -0.01em;">
            Find New Worlds in Starlight
        </div>

        <!-- Section B: Project Overview Card -->
        <div class="ph-card ph-card-accent" style="margin-bottom: 18px; padding: 18px 20px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 16px; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 280px;">
                    <div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: {primary_accent}; margin-bottom: 4px;">
                        Project Overview & Problem Formulation
                    </div>
                    <p style="margin: 0; color: {text_secondary}; font-size: 0.92rem; line-height: 1.6;">
                        High-precision space telescopes collect continuous photometric time-series of distant stars. 
                        When an exoplanet passes directly in front of its host star, it produces a periodic, shallow transit dip in measured flux 
                        (&Delta;F/F &asymp; 0.01% to 1%). However, authentic exoplanet transit signatures are easily confounded by intrinsic stellar variability 
                        (rotating starspots, pulsations, eruptive flares), blended background eclipsing binaries, and discrete spacecraft instrument glitches.
                    </p>
                    <p style="margin: 8px 0 0 0; color: {text_secondary}; font-size: 0.90rem; line-height: 1.55;">
                        This platform implements an end-to-end machine-learning solution to classify stellar observations into eight distinct astronomical 
                        and instrumental categories. The pipeline combines camera/CCD common-mode cotrending, 88 domain-informed features, 
                        and a tri-architecture gradient-boosted ensemble evaluated across both standard and hardware-held-out cross-validation splits.
                    </p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
