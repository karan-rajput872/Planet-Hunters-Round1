"""
Component: Submission Verification Center
Planet Hunters — Scientific Intelligence Platform
Two-Stage Decoupled Validation (Artifact Integrity & Target Dataset Cross-Matching).
Accurate status labels (PASS, BLOCKED, FAIL), creamy styling, and zero unhandled exceptions.
"""

import streamlit as st
import logging
from dashboard.data_loader import run_submission_validation, SUBMISSION_FILE
from dashboard.styles import render_html

logger = logging.getLogger(__name__)

def render_validator(theme: str = "creamy"):
    """Renders Submission Verification Center with two-stage audit execution."""
    text_primary = "#292D32"
    text_secondary = "#70736F"
    primary_accent = "#647C70"
    secondary_accent = "#A58B65"
    border_col = "#E7E0D3"
    card_bg = "#FFFDF8"

    render_html(f"""
    <div style="margin-bottom: 12px;">
        <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; gap: 8px;">
            <div>
                <h2>Submission Verification Center</h2>
                <div style="color: {text_secondary}; font-size: 0.85rem;">
                    Decoupled compliance audit for official candidate: 
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.80rem; font-weight: 600; color: {primary_accent};">submissions/submission_FINAL.csv</span>
                </div>
            </div>
            <span class="badge-status badge-neutral">
                Stage A: 12 Artifact Checks • Stage B: 2 Target Checks
            </span>
        </div>
    </div>
    """)

    # Cache validation result in session state to avoid unnecessary reruns
    if "validation_result" not in st.session_state:
        try:
            st.session_state.validation_result = run_submission_validation()
        except Exception as e:
            logger.error(f"Unexpected validation error: {e}", exc_info=True)
            st.session_state.validation_result = {
                "file": "submission_FINAL.csv",
                "status": "FAILED",
                "passed_all": False,
                "artifact_checks_passed": False,
                "test_data_status": "FAILED",
                "failures": [f"Execution error: {e}"],
                "warnings": [],
                "blocked": []
            }

    col_btn, col_status = st.columns([1.1, 2.9])

    with col_btn:
        if st.button("Execute Validation Audit", use_container_width=True):
            with st.spinner("Executing compliance audit..."):
                try:
                    st.session_state.validation_result = run_submission_validation()
                    st.toast("Audit completed!", icon="✅")
                except Exception as e:
                    logger.error(f"Audit execution exception: {e}", exc_info=True)
                    st.session_state.validation_result = {
                        "file": "submission_FINAL.csv",
                        "status": "FAILED",
                        "failures": [f"Audit failed: {e}"]
                    }

    res = st.session_state.validation_result
    status = res.get("status", "FAILED")

    with col_status:
        if status == "PASSED":
            render_html(f"""
            <div style="display: flex; align-items: center; gap: 8px; height: 100%; padding: 4px 0;">
                <span class="badge-status badge-passed" style="font-size: 0.82rem;">
                    ✓ AUDIT STATUS: PASSED (14/14 CHECKS VERIFIED)
                </span>
                <span style="font-size: 0.80rem; color: {text_secondary};">
                    Bitwise-approved champion satisfies all 14 schema and test-matching criteria.
                </span>
            </div>
            """)
        elif status == "BLOCKED":
            render_html(f"""
            <div style="display: flex; align-items: center; gap: 8px; height: 100%; padding: 4px 0;">
                <span class="badge-status badge-neutral" style="font-size: 0.82rem; border-color: {secondary_accent}; color: {secondary_accent};">
                    ARTIFACT INTEGRITY VERIFIED (12/12 PASSED • 2 BLOCKED)
                </span>
                <span style="font-size: 0.78rem; color: {text_secondary};">
                    Submission structure is valid. External dataset checks are BLOCKED (test_stars.csv not present in runtime).
                </span>
            </div>
            """)
        else:
            failures_count = len(res.get("failures", []))
            render_html(f"""
            <div style="display: flex; align-items: center; gap: 8px; height: 100%; padding: 4px 0;">
                <span class="badge-status" style="background-color: #FDF2F2; border: 1px solid #F87171; color: #DC2626; font-size: 0.82rem;">
                    AUDIT FAILED ({failures_count} DEFECTS DETECTED)
                </span>
                <span style="font-size: 0.78rem; color: {text_secondary};">
                    Inspect the audit checklist table below for specific failure points.
                </span>
            </div>
            """)

    # 14 Audit Checks Table divided into Stage A & Stage B
    checklist_stage_a = [
        {"id": 1, "rule": "File Presence", "desc": "submission_FINAL.csv exists in submissions/ directory", "status": res.get("exists")},
        {"id": 2, "rule": "Readable CSV Format", "desc": "Successfully parsed as valid UTF-8 CSV without corruption", "status": res.get("readable")},
        {"id": 3, "rule": "Target Row Count", "desc": "Contains exactly 7,000 predictions (7,001 rows including header)", "status": res.get("exact_7000_rows")},
        {"id": 4, "rule": "Two-Column Schema", "desc": "File schema has exactly 2 columns", "status": res.get("exact_two_columns")},
        {"id": 5, "rule": "Header Naming", "desc": "Header strictly matches ['id', 'label']", "status": res.get("exact_column_names")},
        {"id": 6, "rule": "No Extra Index Columns", "desc": "No unformatted index or unnamed columns present", "status": res.get("no_index_column")},
        {"id": 7, "rule": "Zero Null Target IDs", "desc": "All 7,000 star IDs are strictly valid non-null integers", "status": res.get("no_null_ids")},
        {"id": 8, "rule": "Unique ID Sequence", "desc": "Zero duplicate IDs in test predictions", "status": res.get("no_duplicate_ids")},
        {"id": 9, "rule": "Zero Null Labels", "desc": "Zero null, NaN, or infinite prediction values", "status": res.get("no_null_labels")},
        {"id": 10, "rule": "Clean String Tokens", "desc": "No empty or whitespace-only prediction strings", "status": res.get("no_whitespace_labels")},
        {"id": 11, "rule": "Valid Class Vocabulary", "desc": "All predictions belong to the 8 permitted astronomical classes", "status": res.get("all_classes_valid")},
        {"id": 12, "rule": "All 8 Classes Represented", "desc": "No category dropped (astrophysically balanced predictions)", "status": res.get("all_eight_classes_represented")},
    ]

    checklist_stage_b = [
        {"id": 13, "rule": "Target Set ID Match", "desc": "Set of predicted IDs matches test_stars.csv exactly", "status": res.get("id_match_test_stars")},
        {"id": 14, "rule": "Strict Sequence Ordering", "desc": "Rows match target test star index order exactly", "status": res.get("id_order_correct")},
    ]

    def render_check_row(c):
        val = c["status"]
        if val is True:
            st_text = "PASS"
            badge_style = "background-color: #EAEFE8; border: 1px solid #C8D7C4; color: #3F6350;"
        elif val is None:
            st_text = "BLOCKED"
            badge_style = f"background-color: #F0EBDD; border: 1px solid {border_col}; color: {secondary_accent};"
        else:
            st_text = "FAIL"
            badge_style = "background-color: #FDF2F2; border: 1px solid #F87171; color: #DC2626;"

        return f'<tr style="border-bottom: 1px solid {border_col};"><td style="padding: 6px 8px; font-family: \'JetBrains Mono\'; color: {text_secondary};">{c["id"]:02d}</td><td style="padding: 6px 8px; font-weight: 600;">{c["rule"]}</td><td style="padding: 6px 8px; color: {text_secondary}; font-size: 0.76rem;">{c["desc"]}</td><td style="padding: 6px 8px; text-align: right;"><span class="badge-status" style="{badge_style}">{st_text}</span></td></tr>'

    stage_a_rows = "".join(render_check_row(c) for c in checklist_stage_a)
    stage_b_rows = "".join(render_check_row(c) for c in checklist_stage_b)

    render_html(f"""
    <div class="ph-card" style="margin-top: 14px; padding: 14px 18px;">
        <div style="font-weight: 600; font-size: 0.85rem; color: {primary_accent}; margin-bottom: 6px;">
            Stage A: Submission Artifact Integrity Checks (Self-Contained • 12 Rules)
        </div>
        <table style="width: 100%; border-collapse: collapse; font-size: 0.80rem; color: {text_primary}; margin-bottom: 16px;">
            <thead>
                <tr style="border-bottom: 2px solid {border_col}; text-align: left;">
                    <th style="padding: 6px 8px; width: 40px; color: {text_secondary};">#</th>
                    <th style="padding: 6px 8px; width: 220px; color: {text_secondary};">Rule Specification</th>
                    <th style="padding: 6px 8px; color: {text_secondary};">Verification Criteria</th>
                    <th style="padding: 6px 8px; width: 100px; text-align: right; color: {text_secondary};">Status</th>
                </tr>
            </thead>
            <tbody>
                {stage_a_rows}
            </tbody>
        </table>
        <div style="font-weight: 600; font-size: 0.85rem; color: {secondary_accent}; margin-bottom: 6px;">
            Stage B: External Target Dataset Cross-Matching Checks (Requires test_stars.csv • 2 Rules)
        </div>
        <table style="width: 100%; border-collapse: collapse; font-size: 0.80rem; color: {text_primary};">
            <thead>
                <tr style="border-bottom: 2px solid {border_col}; text-align: left;">
                    <th style="padding: 6px 8px; width: 40px; color: {text_secondary};">#</th>
                    <th style="padding: 6px 8px; width: 220px; color: {text_secondary};">Rule Specification</th>
                    <th style="padding: 6px 8px; color: {text_secondary};">Verification Criteria</th>
                    <th style="padding: 6px 8px; width: 100px; text-align: right; color: {text_secondary};">Status</th>
                </tr>
            </thead>
            <tbody>
                {stage_b_rows}
            </tbody>
        </table>
    </div>
    """)

    # Show warning notices if Stage B checks are blocked
    if res.get("warnings"):
        for w in res["warnings"]:
            render_html(f"""
            <div style="margin-top: 8px; padding: 8px 12px; background-color: #F0EBDD; border-left: 3px solid {secondary_accent}; border-radius: 4px; font-size: 0.78rem; color: {text_secondary};">
                <strong>Deployment Note:</strong> {w}
            </div>
            """)
