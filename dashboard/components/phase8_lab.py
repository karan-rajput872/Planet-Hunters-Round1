"""
Phase 8: Top 30 Optimization Lab Component for Streamlit Dashboard
"""
import streamlit as st
import pandas as pd
import numpy as np

def render_phase8_lab(theme: str = "light"):
    is_light = (theme == "light")
    card_bg = "#FFFFFF" if is_light else "#131D2E"
    border_col = "#E5EAF1" if is_light else "#1E2D44"
    text_primary = "#101B33" if is_light else "#F1F5F9"
    text_muted = "#667085" if is_light else "#94A3B8"
    accent_blue = "#2457D6" if is_light else "#3B82F6"
    accent_green = "#059669" if is_light else "#10B981"
    accent_purple = "#7C3AED" if is_light else "#8B5CF6"
    accent_amber = "#D97706" if is_light else "#F59E0B"
    accent_red = "#DC2626" if is_light else "#EF4444"

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(36, 87, 214, 0.08) 0%, rgba(124, 58, 237, 0.08) 100%);
                border: 1px solid {border_col}; border-radius: 12px; padding: 24px; margin-bottom: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
            <div>
                <span style="background-color: {accent_purple}; color: #FFFFFF; font-size: 0.72rem; font-weight: 700;
                             padding: 4px 10px; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.05em;">
                    PHASE 8 LAB — TOP 30 STRATEGY
                </span>
                <h2 style="font-family: 'Space Grotesk', sans-serif; font-size: 1.6rem; font-weight: 700; color: {text_primary}; margin: 8px 0 4px 0;">
                    Competitive Intelligence & Targeted Model Optimization
                </h2>
                <div style="color: {text_muted}; font-size: 0.88rem; max-width: 850px;">
                    Rigorous empirical investigation into bridging the gap from Rank 60 toward Top 30 via error diagnostics,
                    leakage-free stacking meta-learners, power ensembling, and detector-channel cross-validation.
                </div>
            </div>
            <div style="text-align: right;">
                <span style="background-color: rgba(5, 150, 105, 0.15); color: {accent_green}; font-size: 0.76rem; font-weight: 700;
                             padding: 6px 14px; border-radius: 20px; border: 1px solid rgba(5, 150, 105, 0.3);">
                    APPROVED FINAL UNTOUCHED
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Panel 1: Competitive Intelligence & Score Gap
    st.markdown(f"<h3 style='font-size: 1.15rem; font-weight: 700; color: {text_primary}; margin-bottom: 12px;'>1. Leaderboard Competitive Intelligence (Rank 60 $\\rightarrow$ Top 30)</h3>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Current Rank", "60", "Phase 4 Upload Active")
    with c2:
        st.metric("Current Portal Score", "0.4214", "Uncotrended Baseline")
    with c3:
        st.metric("Champion CV Score", "0.6336", "+0.2122 Potential Leap")
    with c4:
        st.metric("Target Top 30 Threshold", "~0.60 – 0.62", "Pending Final Upload")

    st.info("""
    **Crucial Strategic Finding:** The user's current Rank 60 on the public leaderboard reflects the Phase 4 baseline (0.4214),
    which suffered from uncotrended spacecraft pointing jitter and thermal breathing. The approved Phase 5/6 Champion
    (`submission_FINAL.csv`), achieving **0.6336 Detector OOF Macro F1** (+0.2122 higher), has **NOT YET BEEN UPLOADED**.
    Uploading `submission_FINAL.csv` is the direct, scientifically validated path to jumping into the Top 30.
    """)

    # Panel 2: Model Architecture Benchmark Comparison
    st.markdown(f"<h3 style='font-size: 1.15rem; font-weight: 700; color: {text_primary}; margin-top: 24px; margin-bottom: 12px;'>2. Experimental Benchmark Matrix (Detector-Channel 5-Fold CV)</h3>", unsafe_allow_html=True)
    
    benchmark_data = [
        {"Model / Experiment": "Phase 4 Baseline (Uncotrended)", "Architecture": "LGB 75% + HGB 25%", "Detector OOF F1": "0.51610", "Fold Std (σ)": "0.0215", "Delta vs P5": "-0.11752", "Status": "LEGACY (LB 0.4214)"},
        {"Model / Experiment": "Phase 5 Champion (Approved Final)", "Architecture": "LGB 50% + HGB 40% + CB 10%", "Detector OOF F1": "0.63362", "Fold Std (σ)": "0.01371", "Delta vs P5": "Baseline", "Status": "APPROVED FINAL"},
        {"Model / Experiment": "Phase 8 Power Ensembling (p=1.5)", "Architecture": "Power scaled 45/45/10", "Detector OOF F1": "0.63408", "Fold Std (σ)": "0.01355", "Delta vs P5": "+0.00046", "Status": "EXPERIMENTAL (Below Gate)"},
        {"Model / Experiment": "Phase 6/7 Alternative Blend", "Architecture": "LGB 45% + HGB 45% + CB 10%", "Detector OOF F1": "0.63381", "Fold Std (σ)": "0.01389", "Delta vs P5": "+0.00019", "Status": "REJECTED (Below Gate)"},
        {"Model / Experiment": "Phase 8 Nested Threshold Multipliers", "Architecture": "Nelder-Mead Nested CV", "Detector OOF F1": "0.63353", "Fold Std (σ)": "0.01384", "Delta vs P5": "-0.00009", "Status": "REJECTED"},
        {"Model / Experiment": "Phase 8 Stacking Meta-Learner", "Architecture": "LogReg on 24 OOF probs", "Detector OOF F1": "0.63225", "Fold Std (σ)": "0.01415", "Delta vs P5": "-0.00136", "Status": "REJECTED (Regression)"},
        {"Model / Experiment": "Phase 8 Stacking + Top Astro Feats", "Architecture": "LogReg on OOF + 5 Feats", "Detector OOF F1": "0.63171", "Fold Std (σ)": "0.01377", "Delta vs P5": "-0.00191", "Status": "REJECTED (Regression)"},
        {"Model / Experiment": "Phase 8 Probabilistic Rank Averaging", "Architecture": "Percentile Rank Averaging", "Detector OOF F1": "0.59734", "Fold Std (σ)": "0.01704", "Delta vs P5": "-0.03628", "Status": "REJECTED (Severe Drop)"},
    ]
    st.dataframe(pd.DataFrame(benchmark_data), use_container_width=True, hide_index=True)

    # Panel 3: Error Diagnostics & Confusion Hotspots
    st.markdown(f"<h3 style='font-size: 1.15rem; font-weight: 700; color: {text_primary}; margin-top: 24px; margin-bottom: 12px;'>3. Out-Of-Fold Error Diagnostics (18,000 Training Stars)</h3>", unsafe_allow_html=True)
    e1, e2 = st.columns(2)
    with e1:
        st.markdown(f"""
        <div style="background-color: {card_bg}; border: 1px solid {border_col}; border-radius: 8px; padding: 16px;">
            <div style="font-weight: 700; color: {text_primary}; margin-bottom: 8px;">Top Macro F1 Loss Contributors</div>
            <div style="font-size: 0.85rem; color: {text_muted}; line-height: 1.6;">
                • <b>planet (F1 0.4571)</b>: Loss contribution = <b>0.0679</b> (Highest in dataset)<br>
                • <b>starspots (F1 0.5338)</b>: Loss contribution = <b>0.0583</b> (Second highest)<br>
                • <b>background_binary (F1 0.5660)</b>: Loss contribution = <b>0.0543</b><br>
                • <b>quiet_star (F1 0.6047)</b>: Loss contribution = <b>0.0494</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with e2:
        st.markdown(f"""
        <div style="background-color: {card_bg}; border: 1px solid {border_col}; border-radius: 8px; padding: 16px;">
            <div style="font-weight: 700; color: {text_primary}; margin-bottom: 8px;">Physical Confusion Hotspots</div>
            <div style="font-size: 0.85rem; color: {text_muted}; line-height: 1.6;">
                • <b>starspots → quiet_star</b>: 898 errors (Rotational amplitude below photon noise)<br>
                • <b>planet → quiet_star</b>: 669 errors (Shallow transits &lt; 0.15% depth)<br>
                • <b>quiet_star → starspots</b>: 257 errors (Residual jitter mimicking modulation)<br>
                • <b>background_binary → eclipsing_binary</b>: 217 errors (Sub-pixel centroid offset)
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Panel 4: Test Prediction Shifts (Phase 8 Candidate vs Approved Final)
    st.markdown(f"<h3 style='font-size: 1.15rem; font-weight: 700; color: {text_primary}; margin-top: 24px; margin-bottom: 12px;'>4. Test Prediction Shift Audit (7,000 Predictions)</h3>", unsafe_allow_html=True)
    t1, t2, t3 = st.columns(3)
    with t1:
        st.metric("Total Test Predictions", "7,000", "Schema Compliant")
    with t2:
        st.metric("Changed Predictions", "31 / 7,000", "0.44% Disagreement")
    with t3:
        st.metric("Prediction Agreement", "99.56%", "High Stability")

    st.markdown(f"""
    <div style="background-color: {card_bg}; border: 1px solid {border_col}; border-radius: 8px; padding: 14px; margin-top: 8px;">
        <div style="font-family: 'JetBrains Mono'; font-size: 0.8rem; color: {text_muted};">
            <b>Approved Final Checksum:</b> 6A378EAE06765A28A39D41A322F47FF25512A43A47827FF4576940282B74330E (VERIFIED PRESERVED)<br>
            <b>Phase 8 Candidate Checksum:</b> 7597C8E9130502595537C3F3F3B5265348403FC0EFF81680DBE9D996EC79F181 (14/14 PASS)<br>
            <b>Gate Evaluation:</b> Best CV gain (+0.00046) &lt; +0.0030 Threshold $\rightarrow$ <b>RETAIN APPROVED FINAL</b>
        </div>
    </div>
    """, unsafe_allow_html=True)
