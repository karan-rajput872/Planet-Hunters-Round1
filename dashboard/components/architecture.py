"""
Component D: Model Architecture & Prediction Pipeline Flow
Planet Hunters — Scientific Intelligence Platform
ML Challenge Hack4Hack 2026 — Round 1

End-to-End Pipeline Engineering, 4-Stage Flow, Dual Weighted Ensemble & Ablation Study
"""

import streamlit as st
from pathlib import Path
from dashboard.data_loader import FEATURE_GROUP_ABLATIONS

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ARCH_IMAGE = PROJECT_ROOT / "assets" / "architecture" / "project_architecture.png"


def render_architecture(theme: str = "light"):
    """Renders the comprehensive Model Architecture section with connected pipeline,

    ensemble matrix, mathematical execution formula, and empirical ablation table.
    """
    is_dark = (theme == "dark")

    # Theme color tokens
    sub_color = "#94A3B8" if is_dark else "#667085"
    card_bg = "#131D2E" if is_dark else "#FFFFFF"
    border_col = "#1E2D44" if is_dark else "#E5EAF1"
    text_col = "#F1F5F9" if is_dark else "#172033"
    primary_blue = "#3B82F6" if is_dark else "#2457D6"
    teal_accent = "#14B8A6" if is_dark else "#0F9D91"
    table_th_bg = "#182438" if is_dark else "#F8FAFC"
    code_bg = "#0A101D" if is_dark else "#F8FAFC"
    highlight_row_bg = "rgba(20, 184, 166, 0.12)" if is_dark else "rgba(15, 157, 145, 0.07)"

    # =========================================================================
    # 1. SECTION HEADER
    # =========================================================================
    st.markdown(f"""
    <div class="ph-card ph-card-accent" style="margin-bottom: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
            <div>
                <div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: {primary_blue}; margin-bottom: 4px;">
                    MODEL ENGINEERING / INFERENCE DESIGN
                </div>
                <h2 style="margin: 0 0 6px 0; font-size: 1.65rem; font-family: 'Space Grotesk', sans-serif; font-weight: 700; color: {text_col}; letter-spacing: -0.02em;">
                    MODEL ARCHITECTURE
                </h2>
                <p style="margin: 0; color: {sub_color}; font-size: 0.9rem; line-height: 1.45;">
                    An interpretable view of the feature engineering, cross-validation and ensemble inference pipeline.
                </p>
            </div>
            <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                <span class="badge-status badge-neutral" style="font-size: 0.78rem; padding: 4px 10px;">
                    15 Estimators • 5-Fold Stratified & Detector CV
                </span>
                <span class="badge-status badge-passed" style="font-size: 0.78rem; padding: 4px 10px;">
                    50:40:10 Tri-Ensemble Blend
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # =========================================================================
    # 2. FOUR-STAGE CONNECTED PIPELINE DIAGRAM
    # =========================================================================
    stage1_col, stage2_col, stage3_col, stage4_col = st.columns(4)

    # Stage 01: Data Ingestion & Preprocessing
    with stage1_col:
        st.markdown(f"""
        <div style="background-color: {card_bg}; border: 1px solid {border_col}; border-top: 3px solid #0284C7; border-radius: 8px; padding: 16px 18px; min-height: 235px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between; position: relative;">
            <div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; font-weight: 700; color: #0284C7; letter-spacing: 0.05em;">
                        STAGE 01
                    </span>
                    <span style="font-size: 0.75rem; color: #0284C7; font-weight: 600;">Data Ingestion</span>
                </div>
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.05rem; font-weight: 700; color: {text_col}; margin-bottom: 6px; line-height: 1.3;">
                    Ingestion & Cotrending
                </div>
                <div style="font-size: 0.78rem; color: {sub_color}; line-height: 1.4; margin-bottom: 10px;">
                    Raw time-series ingestion and Camera/CCD systematic cotrending.
                </div>
                <div style="font-size: 0.75rem; color: {text_col}; line-height: 1.5; font-family: 'Inter', sans-serif;">
                    • <strong>Stellar lightcurve input</strong><br>
                    • 1,315 flux cadences per star<br>
                    • <strong>Camera/CCD Median Cotrending</strong><br>
                    • Spatial (x, y) centroid series<br>
                    • 1-day rolling median detrending
                </div>
            </div>
            <div style="border-top: 1px solid {border_col}; margin-top: 10px; padding-top: 6px; font-size: 0.7rem; color: {sub_color}; text-align: right;">
                Feed to Feature Extractor →
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Stage 02: Physics-Informed Feature Engineering
    with stage2_col:
        st.markdown(f"""
        <div style="background-color: {card_bg}; border: 1px solid {border_col}; border-top: 3px solid #6366F1; border-radius: 8px; padding: 16px 18px; min-height: 235px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between; position: relative;">
            <div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; font-weight: 700; color: #6366F1; letter-spacing: 0.05em;">
                        STAGE 02
                    </span>
                    <span style="font-size: 0.75rem; color: #6366F1; font-weight: 600;">Domain Signals</span>
                </div>
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.05rem; font-weight: 700; color: {text_col}; margin-bottom: 6px; line-height: 1.3;">
                    Physics-Informed Features
                </div>
                <div style="font-size: 0.78rem; color: {sub_color}; line-height: 1.4; margin-bottom: 10px;">
                    Domain-grounded extraction across 8 astronomical modules.
                </div>
                <div style="font-size: 0.75rem; color: {text_col}; line-height: 1.5; font-family: 'Inter', sans-serif;">
                    • <strong>88 Verified Features</strong> (Vectorized)<br>
                    • Photometric moments (MAD, skew)<br>
                    • Lomb-Scargle & FFT power peaks<br>
                    • Transit SNR & Odd-Even depth ratio<br>
                    • Centroid shift & flare asymmetry
                </div>
            </div>
            <div style="border-top: 1px solid {border_col}; margin-top: 10px; padding-top: 6px; font-size: 0.7rem; color: {sub_color}; text-align: right;">
                Feed to 5-Fold Training →
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Stage 03: Stratified Five-Fold Training
    with stage3_col:
        st.markdown(f"""
        <div style="background-color: {card_bg}; border: 1px solid {border_col}; border-top: 3px solid {primary_blue}; border-radius: 8px; padding: 16px 18px; min-height: 235px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between; position: relative;">
            <div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; font-weight: 700; color: {primary_blue}; letter-spacing: 0.05em;">
                        STAGE 03
                    </span>
                    <span style="font-size: 0.75rem; color: {primary_blue}; font-weight: 600;">Cross-Validation</span>
                </div>
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.05rem; font-weight: 700; color: {text_col}; margin-bottom: 6px; line-height: 1.3;">
                    Multi-Model Five-Fold Training
                </div>
                <div style="font-size: 0.78rem; color: {sub_color}; line-height: 1.4; margin-bottom: 10px;">
                    Tri-architecture cross-validation with zero out-of-fold leakage.
                </div>
                <div style="font-size: 0.75rem; color: {text_col}; line-height: 1.5; font-family: 'Inter', sans-serif;">
                    • <strong>5-Fold Stratified & Detector Splits</strong><br>
                    • 5 × LightGBM Estimators<br>
                    • 5 × HistGradientBoosting Estimators<br>
                    • 5 × CatBoost Oblivious Estimators<br>
                    • Out-of-detector generalization: 0.6336
                </div>
            </div>
            <div style="border-top: 1px solid {border_col}; margin-top: 10px; padding-top: 6px; font-size: 0.7rem; color: {sub_color}; text-align: right;">
                Feed to Soft Fusion →
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Stage 04: Soft-Voting Ensemble (Teal Accent for Final Stage)
    with stage4_col:
        st.markdown(f"""
        <div style="background-color: {card_bg}; border: 1px solid {border_col}; border-top: 3px solid {teal_accent}; border-radius: 8px; padding: 16px 18px; min-height: 235px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between; position: relative;">
            <div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; font-weight: 700; color: {teal_accent}; letter-spacing: 0.05em;">
                        STAGE 04
                    </span>
                    <span style="font-size: 0.75rem; color: {teal_accent}; font-weight: 600;">Final Decision</span>
                </div>
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.05rem; font-weight: 700; color: {text_col}; margin-bottom: 6px; line-height: 1.3;">
                    Soft-Voting Ensemble
                </div>
                <div style="font-size: 0.78rem; color: {sub_color}; line-height: 1.4; margin-bottom: 10px;">
                    Optimal fusion yielding discrete 8-class assignments.
                </div>
                <div style="font-size: 0.75rem; color: {text_col}; line-height: 1.5; font-family: 'Inter', sans-serif;">
                    • <strong>LightGBM: 50% | HistGB: 40% | CatBoost: 10%</strong><br>
                    • Probability-level soft voting<br>
                    • Eight-class argmax prediction<br>
                    • <strong>OOF Macro F1: 0.6455</strong><br>
                    • Exactly 7,000 verified rows
                </div>
            </div>
            <div style="border-top: 1px solid {border_col}; margin-top: 10px; padding-top: 6px; font-size: 0.7rem; color: {teal_accent}; font-weight: 600; text-align: right;">
                ✓ Validated Submission
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)

    # =========================================================================
    # 3. ENSEMBLE SPECIFICATION MATRIX & INFERENCE EXECUTION FORMULA
    # Balanced 50% / 50% Desktop Layout with Exactly Aligned Heights
    # =========================================================================
    col_table, col_diag = st.columns([1.1, 1.0])

    with col_table:
        st.markdown(f"""
        <div style="background-color: {card_bg}; border: 1px solid {border_col}; border-radius: 8px; padding: 20px 22px; min-height: 290px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <h4 style="margin: 0; font-size: 0.98rem; font-family: 'Space Grotesk', sans-serif; color: {text_col};">
                        Promoted Phase 5 Ensemble Specification Matrix
                    </h4>
                    <span style="font-size: 0.72rem; color: {sub_color}; font-family: 'JetBrains Mono';">15 Estimators</span>
                </div>
                <table style="width: 100%; border-collapse: collapse; font-size: 0.81rem; color: {text_col};">
                    <thead>
                        <tr style="background-color: {table_th_bg}; border-bottom: 1px solid {border_col}; text-align: left;">
                            <th style="padding: 9px 8px; color: {sub_color}; font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.04em;">Model Family</th>
                            <th style="padding: 9px 8px; color: {sub_color}; font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.04em; text-align: center;">Folds</th>
                            <th style="padding: 9px 8px; color: {sub_color}; font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.04em; text-align: right;">Weight</th>
                            <th style="padding: 9px 8px; color: {sub_color}; font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.04em;">Structural Role</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="border-bottom: 1px solid {border_col};">
                            <td style="padding: 8px 8px; font-weight: 600; color: #0284C7;">LightGBM</td>
                            <td style="padding: 8px 8px; font-family: 'JetBrains Mono'; color: {text_col}; text-align: center;">5</td>
                            <td style="padding: 8px 8px; font-family: 'JetBrains Mono'; font-weight: 700; color: {primary_blue}; text-align: right;">50.0% (0.50)</td>
                            <td style="padding: 8px 8px; color: {sub_color}; line-height: 1.35;">Leaf-wise splitting; captures sharp transit boundaries.</td>
                        </tr>
                        <tr style="border-bottom: 1px solid {border_col};">
                            <td style="padding: 8px 8px; font-weight: 600; color: #6366F1;">HistGradientBoosting</td>
                            <td style="padding: 8px 8px; font-family: 'JetBrains Mono'; color: {text_col}; text-align: center;">5</td>
                            <td style="padding: 8px 8px; font-family: 'JetBrains Mono'; font-weight: 700; color: #6366F1; text-align: right;">40.0% (0.40)</td>
                            <td style="padding: 8px 8px; color: {sub_color}; line-height: 1.35;">Binned histogram trees; regularizes probability overconfidence.</td>
                        </tr>
                        <tr style="border-bottom: 1px solid {border_col};">
                            <td style="padding: 8px 8px; font-weight: 600; color: #10B981;">CatBoost</td>
                            <td style="padding: 8px 8px; font-family: 'JetBrains Mono'; color: {text_col}; text-align: center;">5</td>
                            <td style="padding: 8px 8px; font-family: 'JetBrains Mono'; font-weight: 700; color: #10B981; text-align: right;">10.0% (0.10)</td>
                            <td style="padding: 8px 8px; color: {sub_color}; line-height: 1.35;">Symmetric oblivious trees; stabilizes rare class precision.</td>
                        </tr>
                        <tr style="background-color: {highlight_row_bg}; border-left: 3px solid {teal_accent};">
                            <td style="padding: 8px 8px; font-weight: 700; color: {teal_accent};">Phase 5 Tri-Ensemble</td>
                            <td style="padding: 8px 8px; font-family: 'JetBrains Mono'; color: {text_col}; text-align: center;">15</td>
                            <td style="padding: 8px 8px; font-family: 'JetBrains Mono'; font-weight: 700; color: {teal_accent}; text-align: right;">100.0% (1.00)</td>
                            <td style="padding: 8px 8px; color: {teal_accent}; font-weight: 600; line-height: 1.35;">OOF Macro F1: 0.6455 | Detector F1: 0.6336</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div style="font-size: 0.74rem; color: {sub_color}; margin-top: 10px; line-height: 1.35;">
                Optimal weighted soft-voting calibrated on 5-fold out-of-fold and detector-channel splits.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_diag:
        st.markdown(f"""
        <div style="background-color: {card_bg}; border: 1px solid {border_col}; border-radius: 8px; padding: 20px 22px; min-height: 290px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <h4 style="margin: 0; font-size: 0.98rem; font-family: 'Space Grotesk', sans-serif; color: {text_col};">
                        Inference Pipeline Execution Formula
                    </h4>
                    <span style="font-size: 0.72rem; color: {sub_color}; font-family: 'JetBrains Mono';">3-Step Math</span>
                </div>
                <div style="background-color: {code_bg}; border: 1px solid {border_col}; border-radius: 6px; padding: 10px 14px; font-family: 'JetBrains Mono', Consolas, monospace; line-height: 1.5; color: {text_col}; overflow-x: auto;">

                    <!-- Step 01 -->
                    <div style="margin-bottom: 8px;">
                        <div style="color: {sub_color}; font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 2px;">
                            STEP 01 — MULTI-MODEL FIVE-FOLD PROBABILITY AVERAGING
                        </div>
                        <div style="font-size: 0.74rem; color: #0284C7;">P_lgb = (1/5) × Σ predict_proba(LightGBM_i)</div>
                        <div style="font-size: 0.74rem; color: #6366F1;">P_hgb = (1/5) × Σ predict_proba(HistGradientBoosting_i)</div>
                        <div style="font-size: 0.74rem; color: #10B981;">P_cb  = (1/5) × Σ predict_proba(CatBoost_i)</div>
                    </div>

                    <!-- Step 02 -->
                    <div style="margin-bottom: 8px;">
                        <div style="color: {sub_color}; font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 2px;">
                            STEP 02 — OPTIMAL PROBABILITY FUSION (50:40:10)
                        </div>
                        <div style="font-size: 0.76rem; font-weight: 700; color: {primary_blue};">
                            P_final = 0.50 × P_lgb + 0.40 × P_hgb + 0.10 × P_cb
                        </div>
                        <div style="font-size: 0.68rem; color: {sub_color}; font-family: 'Inter', sans-serif; margin-top: 1px;">
                            Combines probability distributions from all three heterogeneous model families.
                        </div>
                    </div>

                    <!-- Step 03 -->
                    <div>
                        <div style="color: {sub_color}; font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 2px;">
                            STEP 03 — EIGHT-CLASS DISCRETE LABEL ASSIGNMENT
                        </div>
                        <div style="font-size: 0.76rem; font-weight: 700; color: {teal_accent};">
                            final_labels = CLASSES[argmax(P_final, axis=1)]
                        </div>
                        <div style="font-size: 0.68rem; color: {sub_color}; font-family: 'Inter', sans-serif; margin-top: 1px;">
                            Selects the class with the highest ensemble probability for each test star.
                        </div>
                    </div>

                </div>
            </div>
            <div style="font-size: 0.74rem; color: {sub_color}; margin-top: 10px; line-height: 1.35;">
                Stabilizes out-of-fold variance and eliminates model-specific single-tree bias across all 7,000 test predictions.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)

    # =========================================================================
    # 4. EMPIRICAL FEATURE GROUP ABLATION EVIDENCE
    # Full-width unified table with baseline highlight and clear typography
    # =========================================================================
    rows_html = []
    for ab in FEATURE_GROUP_ABLATIONS:
        is_baseline = (ab["delta"] == "+0.0000")
        row_bg = highlight_row_bg if is_baseline else "transparent"
        delta_color = "#10B981" if is_baseline else ("#F87171" if is_dark else "#DC2626")
        delta_pill_bg = "rgba(16, 185, 129, 0.14)" if is_baseline else "rgba(239, 68, 68, 0.14)"
        left_border = f"border-left: 3px solid {teal_accent};" if is_baseline else "border-left: 3px solid transparent;"

        rows_html.append(f"""
        <tr style="background-color: {row_bg}; {left_border} border-bottom: 1px solid {border_col};">
            <td style="padding: 10px 10px; font-weight: 600; color: {text_col};">{ab['group']}</td>
            <td style="padding: 10px 10px; font-family: 'JetBrains Mono'; color: {text_col}; text-align: center;">{ab['features']}</td>
            <td style="padding: 10px 10px; font-family: 'JetBrains Mono'; font-weight: 700; color: {text_col}; text-align: right;">{ab['oof_f1']:.4f}</td>
            <td style="padding: 10px 10px; text-align: right;">
                <span style="display: inline-block; padding: 2px 8px; border-radius: 4px; background-color: {delta_pill_bg}; color: {delta_color}; font-family: 'JetBrains Mono'; font-weight: 700; font-size: 0.8rem;">
                    {ab['delta']}
                </span>
            </td>
            <td style="padding: 10px 10px; color: {sub_color}; font-size: 0.8rem; line-height: 1.4;">{ab['note']}</td>
        </tr>
        """)

    table_html = f"""
    <div style="background-color: {card_bg}; border: 1px solid {border_col}; border-radius: 8px; padding: 20px 22px; overflow-x: auto;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 8px;">
            <h4 style="margin: 0; font-size: 0.98rem; font-family: 'Space Grotesk', sans-serif; color: {text_col};">
                Empirical Feature Group Ablation Evidence (from Model Evaluation Audit)
            </h4>
            <span style="font-size: 0.72rem; color: {sub_color}; font-family: 'JetBrains Mono';">
                Baseline: 85 Features • OOF F1: 0.5915
            </span>
        </div>
        <table style="width: 100%; border-collapse: collapse; font-size: 0.82rem; color: {text_col};">
            <thead>
                <tr style="background-color: {table_th_bg}; border-bottom: 1px solid {border_col}; text-align: left;">
                    <th style="padding: 9px 10px; color: {sub_color}; font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.04em;">Feature Group Removed</th>
                    <th style="padding: 9px 10px; color: {sub_color}; font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.04em; text-align: center;">Remaining Features</th>
                    <th style="padding: 9px 10px; color: {sub_color}; font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.04em; text-align: right;">OOF Macro F1</th>
                    <th style="padding: 9px 10px; color: {sub_color}; font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.04em; text-align: right;">F1 Impact (Δ)</th>
                    <th style="padding: 9px 10px; color: {sub_color}; font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.04em;">Key Impacted Archetypes</th>
                </tr>
            </thead>
            <tbody>
                {"".join(rows_html)}
            </tbody>
        </table>
        <div style="margin-top: 12px; padding-top: 8px; border-top: 1px solid {border_col}; font-size: 0.74rem; color: {sub_color}; line-height: 1.45;">
            • <em>Feature ablation experiments measure the effect of removing feature groups while retaining the rest of the pipeline.</em><br>
            • <em>Feature space note: Production pipeline extracts 85 domain-informed features verified in <code>data/processed/train_features.parquet</code> (18,000 × 85).</em>
        </div>
    </div>
    """
    st.markdown(table_html, unsafe_allow_html=True)

    # Optional Architectural Schematic Expander
    if ARCH_IMAGE.exists():
        st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
        with st.expander("🔍 View Complete Pipeline Architecture Schematic"):
            st.image(str(ARCH_IMAGE), caption="Full Pipeline Architecture: Raw Flux & Centroids to Submission", use_container_width=True)
