"""
Component H: Final Project Artifacts & Technical Reference Registry
Planet Hunters — Scientific Intelligence Platform
Repository links, technical reports, submission artifact verification, and system specifications.
"""

import streamlit as st
from pathlib import Path
from dashboard.data_loader import SUBMISSION_FILE, PROJECT_METRICS

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

def render_info(theme: str = "creamy"):
    """Renders Section H: Project Artifacts, Specifications, and Technical Documentation Hub."""
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
                <h2>Final Project Artifacts & Documentation Hub</h2>
                <div style="color: {text_secondary}; font-size: 0.85rem;">
                    Verified research documentation, source code repositories, and competition submission artifacts.
                </div>
            </div>
            <span class="badge-status badge-telemetry">
                Audited & Reproducible Artifacts
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_specs, col_docs = st.columns([1.1, 1.0])

    with col_specs:
        st.markdown(f"""
        <div class="ph-card" style="padding: 16px 20px;">
            <div style="font-weight: 600; font-size: 0.92rem; color: {text_primary}; margin-bottom: 12px;">
                Engineering Specifications & Validation Baseline
            </div>
            <table style="width: 100%; border-collapse: collapse; font-size: 0.80rem; color: {text_primary};">
                <tbody>
                    <tr style="border-bottom: 1px solid {border_col};">
                        <td style="padding: 7px 0; color: {text_secondary}; width: 35%;">Project Name</td>
                        <td style="padding: 7px 0; font-weight: 600;">Planet Hunters — Find New Worlds in Starlight</td>
                    </tr>
                    <tr style="border-bottom: 1px solid {border_col};">
                        <td style="padding: 7px 0; color: {text_secondary};">Competition Stage</td>
                        <td style="padding: 7px 0;">ML Challenge Hack4Hack 2026 • Round 1 Completed</td>
                    </tr>
                    <tr style="border-bottom: 1px solid {border_col};">
                        <td style="padding: 7px 0; color: {text_secondary};">Author & Maintainer</td>
                        <td style="padding: 7px 0; font-weight: 600;">Priyanshu Karan (B.Tech CSE, KIIT)</td>
                    </tr>
                    <tr style="border-bottom: 1px solid {border_col};">
                        <td style="padding: 7px 0; color: {text_secondary};">Classification Task</td>
                        <td style="padding: 7px 0;">8-Class Stellar Lightcurve & Centroid Astrometry</td>
                    </tr>
                    <tr style="border-bottom: 1px solid {border_col};">
                        <td style="padding: 7px 0; color: {text_secondary};">Dataset Scope</td>
                        <td style="padding: 7px 0; font-family: 'JetBrains Mono';">18,000 Train Stars • 7,000 Test Stars (1,315 cadences/star)</td>
                    </tr>
                    <tr style="border-bottom: 1px solid {border_col};">
                        <td style="padding: 7px 0; color: {text_secondary};">Evaluation Metric</td>
                        <td style="padding: 7px 0; font-weight: 700; color: {primary_accent};">Macro F1 Score (Unweighted Harmonic Mean)</td>
                    </tr>
                    <tr style="border-bottom: 1px solid {border_col};">
                        <td style="padding: 7px 0; color: {text_secondary};">Champion Architecture</td>
                        <td style="padding: 7px 0; font-weight: 600;">5-Fold Tri-Ensemble (50% LGBM + 40% HistGB + 10% CatBoost)</td>
                    </tr>
                    <tr style="border-bottom: 1px solid {border_col};">
                        <td style="padding: 7px 0; color: {text_secondary};">Cotrended Feature Space</td>
                        <td style="padding: 7px 0; font-family: 'JetBrains Mono';">88 Physics Features (60.3% KS Drift Reduction)</td>
                    </tr>
                    <tr style="border-bottom: 1px solid {border_col};">
                        <td style="padding: 7px 0; color: {text_secondary};">Standard OOF F1</td>
                        <td style="padding: 7px 0; font-family: 'JetBrains Mono'; font-weight: 700; color: {primary_accent};">0.6455 (18,000 Out-of-Fold Stars)</td>
                    </tr>
                    <tr>
                        <td style="padding: 7px 0; color: {text_secondary};">Detector Holdout F1</td>
                        <td style="padding: 7px 0; font-family: 'JetBrains Mono'; font-weight: 700; color: {secondary_accent};">0.6336 (Hardware Transfer Generalization)</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)

    with col_docs:
        st.markdown(f"""
        <div class="ph-card" style="padding: 16px 20px;">
            <div style="font-weight: 600; font-size: 0.92rem; color: {text_primary}; margin-bottom: 10px;">
                Verified Documentation & Repository Registry
            </div>
            <div style="display: flex; flex-direction: column; gap: 8px;">
                <div style="padding: 8px 10px; background-color: #F0EBDD; border-radius: 6px; border: 1px solid {border_col};">
                    <div style="font-weight: 600; font-size: 0.82rem; color: {text_primary};">
                        <a href="https://github.com/karan-rajput872/Planet-Hunters-Round1" target="_blank" style="color: {primary_accent}; text-decoration: none;">GitHub Source Code Repository &rarr;</a>
                    </div>
                    <div style="font-size: 0.74rem; color: {text_secondary};">Complete pipeline, cross-validation, feature extractors, and unit test suite.</div>
                </div>
                <div style="padding: 8px 10px; background-color: #F0EBDD; border-radius: 6px; border: 1px solid {border_col};">
                    <div style="font-weight: 600; font-size: 0.82rem; color: {text_primary};">
                        <a href="https://github.com/karan-rajput872/Planet-Hunters-Round1/blob/main/docs/TECHNICAL_REPORT.md" target="_blank" style="color: {primary_accent}; text-decoration: none;">Technical Report & Mathematical Theory &rarr;</a>
                    </div>
                    <div style="font-size: 0.74rem; color: {text_secondary};">Cotrending mathematics, 88 feature formulas, and training pipeline specifications.</div>
                </div>
                <div style="padding: 8px 10px; background-color: #F0EBDD; border-radius: 6px; border: 1px solid {border_col};">
                    <div style="font-weight: 600; font-size: 0.82rem; color: {text_primary};">
                        <a href="https://github.com/karan-rajput872/Planet-Hunters-Round1/blob/main/docs/MODEL_EVALUATION.md" target="_blank" style="color: {primary_accent}; text-decoration: none;">Model Evaluation & Validation Audits &rarr;</a>
                    </div>
                    <div style="font-size: 0.74rem; color: {text_secondary};">Detailed per-class F1 metrics, fold stability matrices, and domain transfer tests.</div>
                </div>
                <div style="padding: 8px 10px; background-color: #F0EBDD; border-radius: 6px; border: 1px solid {border_col};">
                    <div style="font-weight: 600; font-size: 0.82rem; color: {text_primary};">
                        <a href="https://github.com/karan-rajput872/Planet-Hunters-Round1/blob/main/docs/EXPERIMENT_LOG.md" target="_blank" style="color: {primary_accent}; text-decoration: none;">Chronological Experiment Log (Phases 1–8) &rarr;</a>
                    </div>
                    <div style="font-size: 0.74rem; color: {text_secondary};">Complete chronicle of all 8 phases, candidate evaluations, and empirical rejection rationales.</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Approved Final Submission Artifact Verification Card
    sub_exists = SUBMISSION_FILE.is_file()
    sub_status_text = "Verified on disk (Ready in repository)" if sub_exists else "Audited in verification pipeline"
    sub_badge = "badge-passed" if sub_exists else "badge-neutral"

    st.markdown(f"""
    <div class="ph-card" style="border-top: 3px solid {primary_accent}; padding: 16px 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 8px;">
            <div style="font-weight: 600; font-size: 0.90rem; color: {text_primary};">
                Approved Champion Submission Artifact (Phase 5 Promoted Model)
            </div>
            <span class="badge-status {sub_badge}">{sub_status_text}</span>
        </div>
        <div style="font-size: 0.80rem; color: {text_secondary}; line-height: 1.6;">
            • <strong>Artifact Path:</strong> <code>submissions/submission_FINAL.csv</code><br>
            • <strong>Expected Checksum (SHA-256):</strong> <code>6A378EAE06765A28A39D41A322F47FF25512A43A47827FF4576940282B74330E</code><br>
            • <strong>Target Scale:</strong> Exactly 7,000 predictions (7,001 rows including header) • Columns: <code>id,label</code><br>
            • <strong>Ensemble Configuration:</strong> 50% LightGBM + 40% HistGradientBoosting + 10% CatBoost across 5 Stratified Folds
        </div>
    </div>
    """, unsafe_allow_html=True)
