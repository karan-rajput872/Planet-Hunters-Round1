"""
Component H: Project Information & Documentation Hub
Enterprise Editorial Specification & Technical Reference Registry
"""

import streamlit as st
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

def render_info(theme: str = "light"):
    """Renders Project Information, Tech Stack, and Documentation Directory."""
    sub_color = "#94A3B8" if theme == "dark" else "#667085"
    card_bg = "#FFFFFF" if theme == "light" else "#131D2E"
    border_col = "#E5EAF1" if theme == "light" else "#1E2D44"
    text_col = "#172033" if theme == "light" else "#F1F5F9"
    primary_color = "#3B82F6" if theme == "dark" else "#2457D6"
    doc_item_bg = "#F8FAFC" if theme == "light" else "#0F172A"

    st.markdown(f"""
    <div class="ph-card ph-card-accent">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
            <div>
                <h2 style="margin: 0 0 4px 0; font-size: 1.35rem;">Project Specifications & Documentation Hub</h2>
                <p style="margin: 0; color: {sub_color}; font-size: 0.88rem;">
                    Official competition specifications, technical stack, and verified documentation registry.
                </p>
            </div>
            <span class="badge-status badge-neutral">
                Hack4Hack 2026 • Round 1
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_specs, col_docs = st.columns([1.15, 1.0])

    with col_specs:
        st.markdown(f"""
        <div style="background-color: {card_bg}; border: 1px solid {border_col}; border-radius: 8px; padding: 20px;">
            <h4 style="margin: 0 0 14px 0; font-size: 0.95rem; color: {text_col};">Competition & Engineering Specifications</h4>
            <table style="width: 100%; border-collapse: collapse; font-size: 0.82rem; color: {text_col};">
                <tbody>
                    <tr style="border-bottom: 1px solid {border_col};">
                        <td style="padding: 9px 0; color: {sub_color}; width: 35%;">Challenge Name</td>
                        <td style="padding: 9px 0; font-weight: 600; color: {text_col};">ML Challenge Hack4Hack 2026 — Round 1</td>
                    </tr>
                    <tr style="border-bottom: 1px solid {border_col};">
                        <td style="padding: 9px 0; color: {sub_color};">Task Objective</td>
                        <td style="padding: 9px 0; color: {text_col};">8-Class Stellar Lightcurve & Centroid Classification</td>
                    </tr>
                    <tr style="border-bottom: 1px solid {border_col};">
                        <td style="padding: 9px 0; color: {sub_color};">Dataset Scale</td>
                        <td style="padding: 9px 0; font-family: 'JetBrains Mono'; font-size: 0.8rem; color: {text_col};">18,000 Train Stars • 7,000 Test Stars</td>
                    </tr>
                    <tr style="border-bottom: 1px solid {border_col};">
                        <td style="padding: 9px 0; color: {sub_color};">Temporal Resolution</td>
                        <td style="padding: 9px 0; font-family: 'JetBrains Mono'; font-size: 0.8rem; color: {text_col};">1,315 Flux & Centroid Measurements per Star</td>
                    </tr>
                    <tr style="border-bottom: 1px solid {border_col};">
                        <td style="padding: 9px 0; color: {sub_color};">Evaluation Metric</td>
                        <td style="padding: 9px 0; font-weight: 700; color: {primary_color};">Macro-Averaged F1 Score (Unweighted)</td>
                    </tr>
                    <tr style="border-bottom: 1px solid {border_col};">
                        <td style="padding: 9px 0; color: {sub_color};">Champion Strategy</td>
                        <td style="padding: 9px 0; color: {text_col};">Dual 5-Fold Ensemble (75% LightGBM + 25% HistGB)</td>
                    </tr>
                    <tr style="border-bottom: 1px solid {border_col};">
                        <td style="padding: 9px 0; color: {sub_color};">Technologies</td>
                        <td style="padding: 9px 0; font-family: 'JetBrains Mono'; font-size: 0.78rem; color: {sub_color};">
                            Python 3.11 • LightGBM • Scikit-learn • CatBoost • SciPy • Pandas • NumPy • Plotly • Streamlit
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 9px 0; color: {sub_color};">Data Protection</td>
                        <td style="padding: 9px 0; color: #059669; font-weight: 600;">100% Zero-Leakage • Read-Only Submission Pipeline</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)

    with col_docs:
        st.markdown(f"""
        <div style="background-color: {card_bg}; border: 1px solid {border_col}; border-radius: 8px; padding: 20px;">
            <h4 style="margin: 0 0 10px 0; font-size: 0.95rem; color: {text_col};">Project Technical Documentation</h4>
            <p style="font-size: 0.78rem; color: {sub_color}; margin-bottom: 12px;">
                Verified technical documentation files available in the project repository:
            </p>
        """, unsafe_allow_html=True)

        doc_items = [
            ("docs/PROJECT_OVERVIEW.md", "Executive Project Overview", "High-level summary of architecture, data, and design choices."),
            ("docs/COMPETITION_SUBMISSION_GUIDE.md", "Competition Submission Guide", "Strict formatting rules and upload instructions."),
            ("docs/TECHNICAL_REPORT.md", "Complete Technical Report", "In-depth scientific feature formulation and model theory."),
            ("docs/MODEL_EVALUATION.md", "Model Evaluation & Benchmarks", "Detailed per-class F1 metrics and fold variances."),
            ("docs/REPRODUCIBILITY.md", "Reproducibility Protocol", "Bitwise verification and seed controls."),
            ("docs/FINAL_HANDOVER.md", "Final Engineering Handover", "Complete system status and verification checklist."),
            ("CHANGELOG.md", "Development Changelog", "Chronological record of phases 1 through 5."),
        ]

        for rel_path, doc_title, doc_desc in doc_items:
            file_exists = (PROJECT_ROOT / rel_path).exists()
            status_icon = "✓" if file_exists else "•"
            st.markdown(f"""
            <div style="padding: 8px 10px; margin-bottom: 6px; background-color: {doc_item_bg}; border-radius: 6px; border-left: 2px solid {primary_color};">
                <div style="display: flex; justify-content: space-between; align-items: baseline; gap: 4px;">
                    <span style="font-size: 0.82rem; font-weight: 600; color: {text_col};">
                        {status_icon} {doc_title}
                    </span>
                    <span style="font-family: 'JetBrains Mono'; font-size: 0.7rem; color: {sub_color}; white-space: nowrap;">
                        {rel_path}
                    </span>
                </div>
                <div style="font-size: 0.74rem; color: {sub_color}; margin-top: 2px;">
                    {doc_desc}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
