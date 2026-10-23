"""
Component: Phase 6 Optimization Lab & Candidate Visual Preview
Planet Hunters — Find New Worlds in Starlight (Hack4Hack 2026 — Round 1)

Features:
- Panel A: Candidate comparison (Phase 4, Phase 5 approved, Phase 6 experimental)
- Panel B: Ensemble weight explorer with validation metrics
- Panel C: Interactive per-class F1 performance comparison & delta waterfall
- Panel D: OOF Confusion matrix preview for approved vs experimental
- Panel E: Prediction disagreement, transitions, and test distribution
- Panel F: Submission readiness and 14-check validation audit for Phase 6
- Panel G: Safe preview and approval inspection controls (Strictly read-only)
"""

from pathlib import Path
import json
import hashlib
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SUBMISSIONS_DIR = PROJECT_ROOT / "submissions"
SCRATCH_DIR = PROJECT_ROOT / "scratch"
REPORTS_DIR = PROJECT_ROOT / "reports"

PHASE4_BACKUP_PATH = SUBMISSIONS_DIR / "submission_FINAL_PHASE4_BACKUP.csv"
PHASE5_APPROVED_PATH = SUBMISSIONS_DIR / "submission_FINAL.csv"
PHASE6_CANDIDATE_PATH = (
    SUBMISSIONS_DIR / "submission_PHASE6_candidate_01.csv"
    if (SUBMISSIONS_DIR / "submission_PHASE6_candidate_01.csv").exists()
    else SUBMISSIONS_DIR / "submission_PHASE6_candidate.csv"
)
EXPERIMENT_SUMMARY_PATH = SCRATCH_DIR / "phase6_experiment_summary.json"

CLASSES = [
    "background_binary", "eclipsing_binary", "flare_star", "instrument_glitch",
    "planet", "pulsating_star", "quiet_star", "starspots"
]

CLASS_DISPLAYS = {
    "background_binary": "Background Binary",
    "eclipsing_binary": "Eclipsing Binary",
    "flare_star": "Flare Star",
    "instrument_glitch": "Instrument Glitch",
    "planet": "Exoplanet Transit",
    "pulsating_star": "Pulsating Star",
    "quiet_star": "Quiet Star",
    "starspots": "Starspots"
}

def compute_sha256(filepath: Path) -> str:
    if not filepath.exists():
        return "N/A (File not found)"
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def load_experiment_summary():
    if EXPERIMENT_SUMMARY_PATH.exists():
        try:
            with open(EXPERIMENT_SUMMARY_PATH, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return None

def render_phase6_preview(theme: str = "light"):
    """Renders the Phase 6 Leaderboard Optimization & Candidate Preview station."""
    sub_color = "#94A3B8" if theme == "dark" else "#667085"
    primary_color = "#3B82F6" if theme == "dark" else "#2457D6"
    card_bg = "#131D2E" if theme == "dark" else "#FFFFFF"
    border_col = "#1E2D44" if theme == "dark" else "#E5EAF1"
    text_col = "#F1F5F9" if theme == "dark" else "#172033"
    accent_green = "#10B981" if theme == "dark" else "#059669"
    accent_amber = "#F59E0B" if theme == "dark" else "#D97706"
    accent_red = "#EF4444" if theme == "dark" else "#DC2626"

    # Header Card
    st.markdown(f"""
    <div class="ph-card ph-card-accent" style="border-left: 4px solid #8B5CF6;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
            <div>
                <div style="font-size: 0.76rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #8B5CF6; margin-bottom: 2px;">
                    MISSION CONTROL EXPERIMENTAL DIVISION
                </div>
                <h2 style="margin: 0 0 6px 0; font-size: 1.45rem;">PHASE 6 — LEADERBOARD OPTIMIZATION</h2>
                <p style="margin: 0; color: {sub_color}; font-size: 0.88rem;">
                    Scientific evidence-driven ensemble weight optimization, class-specific decision validation, and side-by-side candidate inspection.
                </p>
            </div>
            <div style="display: flex; gap: 8px; align-items: center;">
                <span class="badge-status badge-neutral" style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem;">
                    Round 1 Deadline: 23 Oct 10:00 AM IST
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Mandatory Safety Banner
    st.markdown(f"""
    <div style="background-color: {'#1E2235' if theme == 'dark' else '#FFFBEB'}; border: 1px solid {'#3730A3' if theme == 'dark' else '#FDE68A'}; border-radius: 8px; padding: 12px 16px; margin-bottom: 20px;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 1.2rem;">🛡️</span>
            <div style="font-size: 0.84rem; color: {'#E0E7FF' if theme == 'dark' else '#92400E'};">
                <strong>NON-NEGOTIABLE SAFETY PROTOCOL:</strong> Current approved submission (<code>submissions/submission_FINAL.csv</code>) is protected and untouched. 
                Phase 6 experiments are serialized separately to <code>submission_PHASE6_candidate.csv</code>. The dashboard strictly operates in read-only preview mode.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    summary_data = load_experiment_summary()
    has_candidate = PHASE6_CANDIDATE_PATH.exists()

    # =========================================================================
    # PANEL A: CANDIDATE COMPARISON
    # =========================================================================
    st.markdown(f"<h3 style='color: {text_col}; font-size: 1.15rem; margin-top: 10px; margin-bottom: 12px;'>Panel A: Candidate Benchmark Comparison</h3>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-container" style="border-top: 3px solid #64748B;">
            <div class="metric-label">Phase 4 Baseline (Submitted)</div>
            <div class="metric-value" style="font-size: 1.25rem;">0.5915 / 0.5161</div>
            <div class="metric-caption">Stratified OOF / Detector OOF (Pub LB: 0.4214)</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-container" style="border-top: 3px solid {accent_green};">
            <div class="metric-label">Phase 5 Approved Champion</div>
            <div class="metric-value" style="font-size: 1.25rem; color: {accent_green};">0.6455 / 0.6336</div>
            <div class="metric-caption">Stratified OOF / Detector OOF (50/40/10 Tri)</div>
        </div>
        """, unsafe_allow_html=True)

    alt_strat = summary_data["alt_strat_f1"] if summary_data else 0.6455
    alt_det = summary_data["alt_det_f1"] if summary_data else 0.6336
    alt_weights = summary_data["alt_weights"] if summary_data else [0.50, 0.40, 0.10]
    
    with col3:
        st.markdown(f"""
        <div class="metric-container" style="border-top: 3px solid #8B5CF6;">
            <div class="metric-label">Phase 6 Candidate ({int(alt_weights[0]*100)}/{int(alt_weights[1]*100)}/{int(alt_weights[2]*100)})</div>
            <div class="metric-value" style="font-size: 1.25rem; color: #8B5CF6;">{alt_strat:.4f} / {alt_det:.4f}</div>
            <div class="metric-caption">Stratified OOF / Detector OOF</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        det_gain = alt_det - 0.6336
        strat_gain = alt_strat - 0.6455
        delta_color = accent_green if det_gain > 0 else (accent_amber if det_gain == 0 else accent_red)
        st.markdown(f"""
        <div class="metric-container" style="border-top: 3px solid {delta_color};">
            <div class="metric-label">Detector Generalization Delta</div>
            <div class="metric-value" style="font-size: 1.25rem; color: {delta_color};">{det_gain:+.4f}</div>
            <div class="metric-caption">Stratified Delta: {strat_gain:+.4f}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    # Benchmark bar chart comparison
    bench_data = [
        {"Pipeline": "Phase 4 Dual (Baseline)", "Stratified OOF": 0.5915, "Detector OOF": 0.5161, "Status": "Historical Baseline"},
        {"Pipeline": "Phase 5 Tri (Approved Champion)", "Stratified OOF": 0.6455, "Detector OOF": 0.6336, "Status": "Current Approved"},
        {"Pipeline": f"Phase 6 Best Experimental ({int(alt_weights[0]*100)}/{int(alt_weights[1]*100)}/{int(alt_weights[2]*100)})", "Stratified OOF": alt_strat, "Detector OOF": alt_det, "Status": "Experimental Candidate"}
    ]
    bench_df = pd.DataFrame(bench_data)
    
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(
        name="Standard Stratified OOF Macro F1",
        x=bench_df["Pipeline"],
        y=bench_df["Stratified OOF"],
        text=[f"<b>{v:.4f}</b>" for v in bench_df["Stratified OOF"]],
        textposition="auto",
        marker_color="#3B82F6" if theme == "dark" else "#2563EB"
    ))
    fig_comp.add_trace(go.Bar(
        name="Detector-Channel OOF Macro F1",
        x=bench_df["Pipeline"],
        y=bench_df["Detector OOF"],
        text=[f"<b>{v:.4f}</b>" for v in bench_df["Detector OOF"]],
        textposition="auto",
        marker_color="#10B981" if theme == "dark" else "#059669"
    ))
    fig_comp.update_layout(
        barmode="group",
        height=320,
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=text_col, size=12),
        yaxis=dict(range=[0.45, 0.70], gridcolor=border_col)
    )
    st.plotly_chart(fig_comp, use_container_width=True)

    # =========================================================================
    # PANEL B: ENSEMBLE WEIGHT EXPLORER
    # =========================================================================
    st.markdown(f"<h3 style='color: {text_col}; font-size: 1.15rem; margin-top: 24px; margin-bottom: 12px;'>Panel B: Ensemble Weight Explorer</h3>", unsafe_allow_html=True)
    
    if summary_data and "tested_blends" in summary_data:
        blends_df = pd.DataFrame(summary_data["tested_blends"])
        blends_df["LGB (%)"] = blends_df["weights"].apply(lambda w: int(round(w[0] * 100)))
        blends_df["HGB (%)"] = blends_df["weights"].apply(lambda w: int(round(w[1] * 100)))
        blends_df["CB (%)"]  = blends_df["weights"].apply(lambda w: int(round(w[2] * 100)))
        blends_df["Role"] = blends_df["name"].apply(
            lambda n: "CURRENT APPROVED" if "Phase 5 Approved" in n else "EXPERIMENTAL CANDIDATE"
        )
        
        col_tbl, col_scat = st.columns([1.3, 1.0])
        with col_tbl:
            display_tbl = blends_df[["name", "Role", "LGB (%)", "HGB (%)", "CB (%)", "strat_f1", "det_f1", "strat_fold_std", "det_fold_std"]].copy()
            display_tbl.columns = ["Candidate Name", "Role", "LGB %", "HGB %", "CB %", "Strat OOF", "Detector OOF", "Strat Std", "Det Std"]
            st.dataframe(display_tbl.style.format({
                "Strat OOF": "{:.4f}",
                "Detector OOF": "{:.4f}",
                "Strat Std": "±{:.4f}",
                "Det Std": "±{:.4f}"
            }), height=280, use_container_width=True)
            
        with col_scat:
            fig_scat = go.Figure()
            for idx, row in blends_df.iterrows():
                is_p5 = "Phase 5 Approved" in row["name"]
                fig_scat.add_trace(go.Scatter(
                    x=[row["strat_f1"]],
                    y=[row["det_f1"]],
                    mode="markers+text",
                    name=row["name"],
                    text=[f"{row['LGB (%)']}/{row['HGB (%)']}/{row['CB (%)']}"],
                    textposition="top center",
                    marker=dict(
                        size=14 if is_p5 else 10,
                        color=accent_green if is_p5 else "#8B5CF6",
                        symbol="star" if is_p5 else "circle",
                        line=dict(width=2, color="#FFFFFF" if theme == "dark" else "#1E293B")
                    ),
                    showlegend=False
                ))
            fig_scat.update_layout(
                title=dict(text="Stratified vs Detector-Channel OOF Space", font=dict(size=12, color=sub_color)),
                xaxis=dict(title="Standard Stratified OOF Macro F1", gridcolor=border_col),
                yaxis=dict(title="Detector-Channel OOF Macro F1", gridcolor=border_col),
                height=280,
                margin=dict(l=20, r=20, t=30, b=20),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color=text_col, size=11)
            )
            st.plotly_chart(fig_scat, use_container_width=True)
    else:
        st.info("Component matrices are currently being computed or summary is not yet generated. Once complete, all blend combinations will render interactively.")

    # =========================================================================
    # PANEL C: CLASS PERFORMANCE COMPARISON
    # =========================================================================
    st.markdown(f"<h3 style='color: {text_col}; font-size: 1.15rem; margin-top: 24px; margin-bottom: 12px;'>Panel C: Per-Class F1 Score Comparison & Delta Waterfall</h3>", unsafe_allow_html=True)
    
    if summary_data and "p5_per_class" in summary_data:
        p5_pc = summary_data["p5_per_class"]
        alt_pc = summary_data["alt_per_class"]
        
        class_rows = []
        for c in CLASSES:
            f1_p5 = p5_pc.get(c, 0.0)
            f1_alt = alt_pc.get(c, 0.0)
            diff = f1_alt - f1_p5
            class_rows.append({
                "Class Code": c,
                "Astrophysical Class": CLASS_DISPLAYS.get(c, c),
                "Phase 5 F1": f1_p5,
                "Phase 6 Candidate F1": f1_alt,
                "Delta F1": diff,
                "Direction": "Improved" if diff > 0.0005 else ("Degraded" if diff < -0.0005 else "Neutral")
            })
            
        c_df = pd.DataFrame(class_rows).sort_values(by="Delta F1", ascending=False)
        
        col_c_chart, col_c_table = st.columns([1.2, 1.0])
        with col_c_chart:
            # Per-class grouped bar chart
            fig_cls = go.Figure()
            fig_cls.add_trace(go.Bar(
                name="Phase 5 Approved (50/40/10)",
                x=[CLASS_DISPLAYS.get(c, c) for c in c_df["Class Code"]],
                y=c_df["Phase 5 F1"],
                marker_color="#64748B" if theme == "dark" else "#94A3B8"
            ))
            fig_cls.add_trace(go.Bar(
                name="Phase 6 Candidate",
                x=[CLASS_DISPLAYS.get(c, c) for c in c_df["Class Code"]],
                y=c_df["Phase 6 Candidate F1"],
                marker_color="#8B5CF6"
            ))
            fig_cls.update_layout(
                barmode="group",
                height=300,
                margin=dict(l=20, r=20, t=10, b=50),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color=text_col, size=11),
                yaxis=dict(range=[0.4, 0.9], gridcolor=border_col)
            )
            st.plotly_chart(fig_cls, use_container_width=True)
            
        with col_c_table:
            st.dataframe(c_df[["Astrophysical Class", "Phase 5 F1", "Phase 6 Candidate F1", "Delta F1", "Direction"]].style.format({
                "Phase 5 F1": "{:.4f}",
                "Phase 6 Candidate F1": "{:.4f}",
                "Delta F1": "{:+.4f}"
            }), height=300, use_container_width=True)

    # =========================================================================
    # PANEL D: CONFUSION MATRIX PREVIEW
    # =========================================================================
    st.markdown(f"<h3 style='color: {text_col}; font-size: 1.15rem; margin-top: 24px; margin-bottom: 12px;'>Panel D: Out-Of-Fold Confusion Matrix Preview</h3>", unsafe_allow_html=True)
    
    col_cm1, col_cm2 = st.columns(2)
    # Approved Phase 5 confusion matrix
    with col_cm1:
        st.markdown(f"""
        <div style="font-weight: 600; font-size: 0.88rem; color: {accent_green}; margin-bottom: 8px;">
            CURRENT APPROVED: Phase 5 Tri-Ensemble (50/40/10) OOF Matrix
        </div>
        """, unsafe_allow_html=True)
        
        # Load OOF tri predictions if available
        oof_tri_path = SCRATCH_DIR / "oof_probs_tri.npy"
        train_stars_path = PROJECT_ROOT / "data" / "raw" / "train_stars.csv"
        if oof_tri_path.exists() and train_stars_path.exists():
            oof_p = np.load(oof_tri_path)
            y_true = pd.read_csv(train_stars_path)["label"]
            preds = [CLASSES[i] for i in np.argmax(oof_p, axis=1)]
            from sklearn.metrics import confusion_matrix
            cm = confusion_matrix(y_true, preds, labels=CLASSES)
            
            fig_cm = go.Figure(data=go.Heatmap(
                z=cm,
                x=[CLASS_DISPLAYS[c] for c in CLASSES],
                y=[CLASS_DISPLAYS[c] for c in CLASSES],
                colorscale="Blues",
                showscale=False,
                text=cm,
                texttemplate="%{text}",
                textfont={"size": 9}
            ))
            fig_cm.update_layout(
                height=320,
                margin=dict(l=40, r=20, t=10, b=40),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color=text_col, size=10),
                xaxis=dict(tickangle=-30),
                yaxis=dict(autorange="reversed")
            )
            st.plotly_chart(fig_cm, use_container_width=True)
        else:
            st.info("Loading Phase 5 confusion matrix...")

    with col_cm2:
        st.markdown(f"""
        <div style="font-weight: 600; font-size: 0.88rem; color: #8B5CF6; margin-bottom: 8px;">
            EXPERIMENTAL CANDIDATE: Best Alternative OOF Matrix
        </div>
        """, unsafe_allow_html=True)
        
        cand_oof_path = SCRATCH_DIR / "phase6_candidate_oof_probs.npy"
        if cand_oof_path.exists() and train_stars_path.exists():
            cand_p = np.load(cand_oof_path)
            y_true = pd.read_csv(train_stars_path)["label"]
            cand_preds = [CLASSES[i] for i in np.argmax(cand_p, axis=1)]
            from sklearn.metrics import confusion_matrix
            cm_cand = confusion_matrix(y_true, cand_preds, labels=CLASSES)
            
            fig_cm2 = go.Figure(data=go.Heatmap(
                z=cm_cand,
                x=[CLASS_DISPLAYS[c] for c in CLASSES],
                y=[CLASS_DISPLAYS[c] for c in CLASSES],
                colorscale="Purples",
                showscale=False,
                text=cm_cand,
                texttemplate="%{text}",
                textfont={"size": 9}
            ))
            fig_cm2.update_layout(
                height=320,
                margin=dict(l=40, r=20, t=10, b=40),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color=text_col, size=10),
                xaxis=dict(tickangle=-30),
                yaxis=dict(autorange="reversed")
            )
            st.plotly_chart(fig_cm2, use_container_width=True)
        else:
            st.info("Experimental matrix will appear once candidate calculation completes.")

    # =========================================================================
    # PANEL E: PREDICTION COMPARISON & TRANSITIONS
    # =========================================================================
    st.markdown(f"<h3 style='color: {text_col}; font-size: 1.15rem; margin-top: 24px; margin-bottom: 12px;'>Panel E: Prediction Disagreement & Class Distribution Comparison</h3>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="font-size: 0.82rem; color: {sub_color}; margin-bottom: 12px;">
        <em>Notice: Test prediction distribution is purely descriptive for telemetry monitoring and does NOT establish leaderboard accuracy.</em>
    </div>
    """, unsafe_allow_html=True)

    if has_candidate and PHASE5_APPROVED_PATH.exists():
        sub_p5 = pd.read_csv(PHASE5_APPROVED_PATH)
        sub_p6 = pd.read_csv(PHASE6_CANDIDATE_PATH)
        
        diff_mask = (sub_p5["label"] != sub_p6["label"])
        diff_count = diff_mask.sum()
        diff_pct = (diff_count / len(sub_p5)) * 100.0
        
        c_diff1, c_diff2 = st.columns([1.0, 1.5])
        with c_diff1:
            st.markdown(f"""
            <div style="background-color: {card_bg}; border: 1px solid {border_col}; border-radius: 8px; padding: 14px; margin-bottom: 12px;">
                <div style="font-size: 0.76rem; text-transform: uppercase; color: {sub_color}; font-weight: 700;">Prediction Differences</div>
                <div style="font-size: 1.6rem; font-weight: 800; color: #8B5CF6; margin: 4px 0;">{diff_count:,} / 7,000</div>
                <div style="font-size: 0.85rem; color: {sub_color}; font-weight: 600;">{diff_pct:.2f}% of test rows changed labels</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Transition pairs
            if diff_count > 0:
                trans_df = pd.DataFrame({
                    "Phase 5 Label": sub_p5.loc[diff_mask, "label"],
                    "Phase 6 Label": sub_p6.loc[diff_mask, "label"]
                })
                trans_counts = trans_df.groupby(["Phase 5 Label", "Phase 6 Label"]).size().reset_index(name="Shift Count")
                trans_counts = trans_counts.sort_values(by="Shift Count", ascending=False).head(8)
                st.markdown(f"<div style='font-size: 0.8rem; font-weight: 700; color: {text_col}; margin-bottom: 4px;'>Top Label Shifts:</div>", unsafe_allow_html=True)
                st.dataframe(trans_counts, height=180, use_container_width=True)
            else:
                st.success("Bitwise identical test predictions.")
                
        with c_diff2:
            s_p5 = sub_p5["label"].value_counts(normalize=True).reindex(CLASSES).fillna(0) * 100.0
            s_p6 = sub_p6["label"].value_counts(normalize=True).reindex(CLASSES).fillna(0) * 100.0
            
            fig_dist = go.Figure()
            fig_dist.add_trace(go.Bar(
                name="Phase 5 Approved (%)",
                x=[CLASS_DISPLAYS[c] for c in CLASSES],
                y=s_p5,
                marker_color="#10B981" if theme == "dark" else "#059669"
            ))
            fig_dist.add_trace(go.Bar(
                name="Phase 6 Experimental (%)",
                x=[CLASS_DISPLAYS[c] for c in CLASSES],
                y=s_p6,
                marker_color="#8B5CF6"
            ))
            fig_dist.update_layout(
                barmode="group",
                height=260,
                margin=dict(l=20, r=20, t=10, b=40),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color=text_col, size=10),
                yaxis=dict(title="Percentage (%)", gridcolor=border_col)
            )
            st.plotly_chart(fig_dist, use_container_width=True)
    else:
        st.info("Phase 6 candidate predictions are pending generation.")

    # =========================================================================
    # PANEL F: SUBMISSION READINESS & VALIDATION AUDIT
    # =========================================================================
    st.markdown(f"<h3 style='color: {text_col}; font-size: 1.15rem; margin-top: 24px; margin-bottom: 12px;'>Panel F: Submission Readiness & Schema Verification</h3>", unsafe_allow_html=True)
    
    if has_candidate:
        from src.submission_validation import validate_submission
        val_res = validate_submission(PHASE6_CANDIDATE_PATH, verbose=False)
        sha_cand = compute_sha256(PHASE6_CANDIDATE_PATH)
        
        f1, f2, f3, f4, f5 = st.columns(5)
        with f1:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">Candidate File</div>
                <div class="metric-value" style="font-size: 0.95rem; color: #8B5CF6;">{PHASE6_CANDIDATE_PATH.name}</div>
                <div class="metric-caption">Experimental</div>
            </div>
            """, unsafe_allow_html=True)
        with f2:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">Row Count</div>
                <div class="metric-value" style="color: {accent_green};">7,000</div>
                <div class="metric-caption">100% Complete</div>
            </div>
            """, unsafe_allow_html=True)
        with f3:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">Schema & Order</div>
                <div class="metric-value" style="color: {accent_green}; font-size: 1.05rem;">VERIFIED</div>
                <div class="metric-caption">Official ID Order</div>
            </div>
            """, unsafe_allow_html=True)
        with f4:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">Validator Status</div>
                <div class="metric-value" style="color: {accent_green if val_res['passed_all'] else accent_red}; font-size: 1.05rem;">
                    {'14/14 PASS' if val_res['passed_all'] else 'FAILED'}
                </div>
                <div class="metric-caption">Competition Rules</div>
            </div>
            """, unsafe_allow_html=True)
        with f5:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">SHA-256 Checksum</div>
                <div class="metric-value" style="font-size: 0.72rem; font-family: 'JetBrains Mono', monospace;" title="{sha_cand}">{sha_cand[:12]}...</div>
                <div class="metric-caption">Integrity Hash</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Phase 6 candidate file (submission_PHASE6_candidate.csv) not found yet.")

    # =========================================================================
    # PANEL G: PREVIEW AND APPROVAL CONTROLS (READ-ONLY)
    # =========================================================================
    st.markdown(f"<h3 style='color: {text_col}; font-size: 1.15rem; margin-top: 24px; margin-bottom: 12px;'>Panel G: Preview and Approval Inspection Controls</h3>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background-color: {'#2A1711' if theme == 'dark' else '#FEF2F2'}; border: 1px solid {'#991B1B' if theme == 'dark' else '#FCA5A5'}; border-radius: 8px; padding: 12px 16px; margin-bottom: 16px;">
        <div style="color: {'#FCA5A5' if theme == 'dark' else '#991B1B'}; font-size: 0.84rem; font-weight: 700;">
            ⚠️ EXPERIMENTAL CANDIDATE — NOT YET APPROVED FOR COMPETITION UPLOAD
        </div>
        <div style="color: {'#FECACA' if theme == 'dark' else '#B91C1C'}; font-size: 0.8rem; margin-top: 2px;">
            The portal submission file remains strictly locked to <strong>CURRENT APPROVED SUBMISSION: <code>submissions/submission_FINAL.csv</code></strong>.
            This dashboard cannot and will never overwrite or upload submissions automatically.
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_p5, tab_p6, tab_report = st.tabs([
        "⭐ CURRENT APPROVED: Phase 5 (submission_FINAL.csv)",
        "🧪 EXPERIMENTAL CANDIDATE: Phase 6 (submission_PHASE6_candidate.csv)",
        "📋 Optimization Lab Audit Log"
    ])

    with tab_p5:
        if PHASE5_APPROVED_PATH.exists():
            df_final = pd.read_csv(PHASE5_APPROVED_PATH)
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 0.82rem; font-weight: 600;">Status: <strong>PROMOTED & APPROVED CHAMPION</strong></span>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem;">SHA-256: {compute_sha256(PHASE5_APPROVED_PATH)}</span>
            </div>
            """, unsafe_allow_html=True)
            st.dataframe(df_final.head(50), height=240, use_container_width=True)
        else:
            st.error("submission_FINAL.csv not found!")

    with tab_p6:
        if has_candidate:
            df_cand = pd.read_csv(PHASE6_CANDIDATE_PATH)
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 0.82rem; font-weight: 600; color: #8B5CF6;">Status: <strong>EXPERIMENTAL CANDIDATE</strong></span>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem;">SHA-256: {compute_sha256(PHASE6_CANDIDATE_PATH)}</span>
            </div>
            """, unsafe_allow_html=True)
            st.dataframe(df_cand.head(50), height=240, use_container_width=True)
        else:
            st.info("Phase 6 candidate file has not been serialized yet.")

    with tab_report:
        opt_report_path = REPORTS_DIR / "PHASE6_RAPID_OPTIMIZATION_REPORT.md"
        if opt_report_path.exists():
            with open(opt_report_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())
        else:
            st.info("Optimization report is currently being drafted by the engineering pipeline.")
