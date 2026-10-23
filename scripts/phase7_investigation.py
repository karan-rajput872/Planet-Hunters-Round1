"""
Phase 7: Final Generalization Breakthrough & Competition Optimization
Author: Senior Kaggle-level ML Competition Researcher & Independent Validation Auditor

Executes:
1. Baseline verification from saved artifacts.
2. High-Priority Investigation A: In-depth Error Analysis & Astrophysics Diagnostics.
3. High-Priority Investigation B: Ensemble Diversity & Model Complementarity.
4. High-Priority Investigation C: Feature Value, Stability & Robustness Audit.
5. High-Priority Investigation D: Detector-Channel Validation Realism & Candidate Generation.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import hashlib
import json
import numpy as np
import pandas as pd
from sklearn.metrics import f1_score, classification_report, confusion_matrix
from src import config

def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def main():
    print("=" * 80)
    print("PHASE 7: FINAL GENERALIZATION BREAKTHROUGH & OPTIMIZATION AUDIT")
    print("=" * 80)
    
    classes = sorted(config.CLASSES)
    label_to_idx = {c: i for i, c in enumerate(classes)}
    idx_to_label = {i: c for i, c in enumerate(classes)}
    
    train_stars = pd.read_csv('data/raw/train_stars.csv')
    test_stars = pd.read_csv('data/raw/test_stars.csv')
    sample_sub = pd.read_csv('data/raw/sample_submission.csv')
    y_idx = np.array([label_to_idx[lbl] for lbl in train_stars['label']])
    
    train_stars['detector'] = train_stars['camera'].astype(str) + '_' + train_stars['ccd'].astype(str)
    
    # 1. Load saved component OOFs
    oof_lgb = np.load('scratch/phase6_oof_lgb.npy')
    oof_hgb = np.load('scratch/phase6_oof_hgb.npy')
    oof_cb  = np.load('scratch/phase6_oof_cb.npy')
    
    det_oof_lgb = np.load('scratch/phase6_det_oof_lgb.npy')
    det_oof_hgb = np.load('scratch/phase6_det_oof_hgb.npy')
    det_oof_cb  = np.load('scratch/phase6_det_oof_cb.npy')
    
    test_lgb = np.load('scratch/phase6_test_lgb.npy')
    test_hgb = np.load('scratch/phase6_test_hgb.npy')
    test_cb  = np.load('scratch/phase6_test_cb.npy')
    
    fold_assign = np.load('scratch/phase6_fold_assignments.npy')
    det_fold_assign = np.load('scratch/phase6_det_fold_assignments.npy')
    
    # Baseline checks
    p5_weights = (0.50, 0.40, 0.10)
    p6_weights = (0.45, 0.45, 0.10)
    
    p5_strat_f1 = f1_score(y_idx, np.argmax(0.50*oof_lgb + 0.40*oof_hgb + 0.10*oof_cb, axis=1), average='macro')
    p5_det_f1   = f1_score(y_idx, np.argmax(0.50*det_oof_lgb + 0.40*det_oof_hgb + 0.10*det_oof_cb, axis=1), average='macro')
    p6_strat_f1 = f1_score(y_idx, np.argmax(0.45*oof_lgb + 0.45*oof_hgb + 0.10*oof_cb, axis=1), average='macro')
    p6_det_f1   = f1_score(y_idx, np.argmax(0.45*det_oof_lgb + 0.45*det_oof_hgb + 0.10*det_oof_cb, axis=1), average='macro')
    
    print(f"\n[SECTION 2: BASELINE RE-VERIFICATION FROM SAVED MATRICES]")
    print(f"  Phase 5 Tri-Ensemble (50/40/10): Stratified OOF = {p5_strat_f1:.4f} | Detector OOF = {p5_det_f1:.4f}")
    print(f"  Phase 6 Blend (45/45/10):        Stratified OOF = {p6_strat_f1:.4f} | Detector OOF = {p6_det_f1:.4f}")
    
    # -------------------------------------------------------------
    # SECTION 3: HIGH-PRIORITY INVESTIGATION A — ERROR ANALYSIS
    # -------------------------------------------------------------
    print("\n" + "=" * 60)
    print("SECTION 3: HIGH-PRIORITY INVESTIGATION A — ERROR ANALYSIS")
    print("=" * 60)
    
    p5_strat_prob = 0.50*oof_lgb + 0.40*oof_hgb + 0.10*oof_cb
    p5_preds = np.argmax(p5_strat_prob, axis=1)
    errors_mask = (p5_preds != y_idx)
    total_errors = errors_mask.sum()
    print(f"Total OOF Errors: {total_errors:,} / {len(y_idx):,} ({total_errors/len(y_idx)*100:.2f}% error rate, Accuracy: {100 - total_errors/len(y_idx)*100:.2f}%)")
    
    # Class-wise F1 and loss contribution
    rep = classification_report(y_idx, p5_preds, target_names=classes, output_dict=True)
    class_loss = []
    for c in classes:
        f1 = rep[c]['f1-score']
        # Each class carries 1/8 = 0.125 weight in Macro F1. Loss = 0.125 * (1 - F1)
        loss_contrib = 0.125 * (1.0 - f1)
        class_loss.append({'class': c, 'f1': f1, 'precision': rep[c]['precision'], 'recall': rep[c]['recall'], 'loss_contrib': loss_contrib})
    class_loss_df = pd.DataFrame(class_loss).sort_values(by='loss_contrib', ascending=False)
    
    print("\nClass-wise Macro F1 Loss Contribution Ranking:")
    for idx, r in class_loss_df.iterrows():
        print(f"  {r['class']:20s} | F1: {r['f1']:.4f} | Prec: {r['precision']:.4f} | Rec: {r['recall']:.4f} | Macro F1 Loss: {r['loss_contrib']:.4f}")
        
    # Top Confused Pairs
    cm = confusion_matrix(y_idx, p5_preds)
    conf_pairs = []
    for i in range(8):
        for j in range(8):
            if i != j:
                conf_pairs.append({
                    'true_class': classes[i],
                    'pred_class': classes[j],
                    'count': cm[i, j],
                    'pair': f"{classes[i]} -> {classes[j]}"
                })
    conf_df = pd.DataFrame(conf_pairs).sort_values(by='count', ascending=False)
    print("\nTop 10 Pairwise Misclassifications:")
    for idx, r in conf_df.head(10).iterrows():
        print(f"  {r['pair']:35s} : {r['count']:,} errors")
        
    # Error distribution across detector channels
    train_stars['is_error'] = errors_mask
    det_error_rate = train_stars.groupby('detector')['is_error'].mean().sort_values(ascending=False)
    print("\nError Rate Across Detector Channels (min vs max):")
    print(f"  Highest error detector: {det_error_rate.index[0]} ({det_error_rate.iloc[0]*100:.2f}%)")
    print(f"  Lowest error detector:  {det_error_rate.index[-1]} ({det_error_rate.iloc[-1]*100:.2f}%)")
    print(f"  Detector channel spread: {det_error_rate.std()*100:.2f}% std")
    
    # -------------------------------------------------------------
    # SECTION 4: HIGH-PRIORITY INVESTIGATION B — ENSEMBLE DIVERSITY
    # -------------------------------------------------------------
    print("\n" + "=" * 60)
    print("SECTION 4: HIGH-PRIORITY INVESTIGATION B — ENSEMBLE DIVERSITY")
    print("=" * 60)
    
    preds_lgb = np.argmax(oof_lgb, axis=1)
    preds_hgb = np.argmax(oof_hgb, axis=1)
    preds_cb  = np.argmax(oof_cb, axis=1)
    
    disagree_lh = (preds_lgb != preds_hgb).sum() / len(y_idx) * 100
    disagree_lc = (preds_lgb != preds_cb).sum() / len(y_idx) * 100
    disagree_hc = (preds_hgb != preds_cb).sum() / len(y_idx) * 100
    
    print("Pairwise Model Prediction Disagreement Rate (% of stars):")
    print(f"  LightGBM vs HistGradientBoosting: {disagree_lh:.2f}%")
    print(f"  LightGBM vs CatBoost:             {disagree_lc:.2f}%")
    print(f"  HistGradientBoosting vs CatBoost: {disagree_hc:.2f}%")
    
    # Error correlation
    err_lgb = (preds_lgb != y_idx)
    err_hgb = (preds_hgb != y_idx)
    err_cb  = (preds_cb != y_idx)
    
    corr_lh = np.corrcoef(err_lgb.astype(float), err_hgb.astype(float))[0, 1]
    corr_lc = np.corrcoef(err_lgb.astype(float), err_cb.astype(float))[0, 1]
    corr_hc = np.corrcoef(err_hgb.astype(float), err_cb.astype(float))[0, 1]
    
    print("\nPairwise Error Correlation:")
    print(f"  corr(Err_LGB, Err_HGB): {corr_lh:.4f}")
    print(f"  corr(Err_LGB, Err_CB):  {corr_lc:.4f}")
    print(f"  corr(Err_HGB, Err_CB):  {corr_hc:.4f}")
    
    # Complementarity: Instances where LGB fails but HGB or CB succeeds
    lgb_fails_hgb_wins = (err_lgb & ~err_hgb).sum()
    hgb_fails_lgb_wins = (~err_lgb & err_hgb).sum()
    all_fail = (err_lgb & err_hgb & err_cb).sum()
    print(f"\nComplementary Rescues:")
    print(f"  Stars where LGB failed but HGB got right: {lgb_fails_hgb_wins:,} stars")
    print(f"  Stars where HGB failed but LGB got right: {hgb_fails_lgb_wins:,} stars")
    print(f"  Stars where all three models failed:      {all_fail:,} stars")
    
    # Targeted candidate weights around 45/45/10 and 50/40/10
    targeted_candidates = [
        ("Phase 5 Approved (50/40/10)", (0.50, 0.40, 0.10)),
        ("Candidate (45/45/10)",         (0.45, 0.45, 0.10)),
        ("Candidate (50/45/5)",          (0.50, 0.45, 0.05)),
        ("Candidate (40/50/10)",         (0.40, 0.50, 0.10)),
        ("Candidate (48/44/8)",          (0.48, 0.44, 0.08)),
        ("Candidate (42/48/10)",         (0.42, 0.48, 0.10)),
    ]
    
    print("\nTargeted Blend Family Benchmark across Folds:")
    hdr = f"{'Blend Name':<28} | {'Strat OOF':<10} | {'Det OOF':<10} | {'Det Fold Mean':<14} | {'Det Fold Std':<12}"
    print(hdr)
    print("-" * len(hdr))
    
    targeted_evals = []
    for name, (wl, wh, wc) in targeted_candidates:
        b_strat = wl*oof_lgb + wh*oof_hgb + wc*oof_cb
        f1_strat = f1_score(y_idx, np.argmax(b_strat, axis=1), average='macro')
        
        b_det = wl*det_oof_lgb + wh*det_oof_hgb + wc*det_oof_cb
        preds_det = np.argmax(b_det, axis=1)
        f1_det = f1_score(y_idx, preds_det, average='macro')
        
        det_folds = [f1_score(y_idx[det_fold_assign == f], preds_det[det_fold_assign == f], average='macro') for f in range(5)]
        
        per_class_f1 = f1_score(y_idx, preds_det, average=None)
        
        targeted_evals.append({
            'name': name,
            'weights': (wl, wh, wc),
            'strat_f1': f1_strat,
            'det_f1': f1_det,
            'det_fold_mean': np.mean(det_folds),
            'det_fold_std': np.std(det_folds),
            'det_folds': det_folds,
            'per_class': {c: float(per_class_f1[i]) for i, c in enumerate(classes)}
        })
        print(f"{name:<28} | {f1_strat:<10.4f} | {f1_det:<10.4f} | {np.mean(det_folds):<14.4f} | {np.std(det_folds):<12.4f}")
        
    # -------------------------------------------------------------
    # SECTION 5: HIGH-PRIORITY INVESTIGATION C — FEATURE ROBUSTNESS
    # -------------------------------------------------------------
    print("\n" + "=" * 60)
    print("SECTION 5: HIGH-PRIORITY INVESTIGATION C — FEATURE VALUE & ROBUSTNESS")
    print("=" * 60)
    
    train_feat = pd.read_parquet('data/processed/train_features_v5.parquet')
    test_feat  = pd.read_parquet('data/processed/test_features_v5.parquet')
    
    print(f"Train Feature Matrix Shape: {train_feat.shape}")
    print(f"Test Feature Matrix Shape:  {test_feat.shape}")
    print(f"Identical Column Alignment: {list(train_feat.columns) == list(test_feat.columns)}")
    
    # Missing values and infinities check
    nan_train = train_feat.isna().sum().sum()
    nan_test = test_feat.isna().sum().sum()
    inf_train = np.isinf(train_feat.values).sum()
    inf_test = np.isinf(test_feat.values).sum()
    print(f"NaN check: Train={nan_train}, Test={nan_test} | Inf check: Train={inf_train}, Test={inf_test}")
    
    # Feature variance across detectors
    cam_ccd_groups = train_stars['detector']
    feature_det_spread = {}
    for col in train_feat.columns[:10]: # sample
        grp_means = train_feat[col].groupby(cam_ccd_groups).mean()
        overall_std = train_feat[col].std() + 1e-9
        det_shift_ratio = grp_means.std() / overall_std
        feature_det_spread[col] = det_shift_ratio
        
    print("\nSample Feature Shift Ratio across Detectors (det_mean_std / overall_std):")
    for col, ratio in list(feature_det_spread.items())[:5]:
        print(f"  {col:25s} : {ratio:.4f}")
        
    # -------------------------------------------------------------
    # SECTION 6: CANDIDATE GENERATION DECISION & GATE AUDIT
    # -------------------------------------------------------------
    print("\n" + "=" * 60)
    print("SECTION 6: CANDIDATE GENERATION DECISION & GATE AUDIT")
    print("=" * 60)
    
    # Phase 7 Acceptance requirement:
    # "Detector-channel OOF improvement of at least approximately 0.003 over the approved 0.6336–0.6338 range."
    best_cand = max(targeted_evals, key=lambda x: x['det_f1'])
    peak_det_f1 = best_cand['det_f1']
    peak_gain = peak_det_f1 - p5_det_f1
    print(f"Peak Detector-Channel OOF Score: {peak_det_f1:.4f} ({best_cand['name']})")
    print(f"Phase 5 Baseline:               {p5_det_f1:.4f}")
    print(f"Measured Gain:                  {peak_gain:+.4f}")
    print(f"Required Gate Threshold:        +0.0030")
    
    passes_gate_threshold = (peak_gain >= 0.0030)
    print(f"Passes +0.003 Gate Threshold:   {passes_gate_threshold}")
    
    # Serializing Phase 7 candidate file for inspection regardless of gate pass
    wl, wh, wc = best_cand['weights']
    cand_test_prob = wl*test_lgb + wh*test_hgb + wc*test_cb
    cand_preds = np.argmax(cand_test_prob, axis=1)
    cand_labels = [classes[i] for i in cand_preds]
    
    sub_df = pd.DataFrame({
        "id": sample_sub["id"],
        "label": cand_labels
    })
    
    p7_cand_path = config.SUBMISSIONS_DIR / "submission_PHASE7_candidate_01.csv"
    sub_df.to_csv(p7_cand_path, index=False)
    sha_p7 = compute_sha256(p7_cand_path)
    
    p5_sub = pd.read_csv(config.SUBMISSIONS_DIR / "submission_FINAL.csv")
    diffs = (sub_df["label"] != p5_sub["label"]).sum()
    diff_pct = (diffs / len(sub_df)) * 100.0
    
    print(f"\nGenerated Phase 7 Candidate: {p7_cand_path}")
    print(f"Rows: {len(sub_df)}")
    print(f"SHA-256: {sha_p7}")
    print(f"Disagreements vs Phase 5 Approved: {diffs} / 7,000 ({diff_pct:.2f}%)")
    
    # Save complete JSON summary for Dashboard and Reports
    p7_summary = {
        "verified_baselines": {
            "p4_strat_f1": 0.5915,
            "p4_det_f1": 0.5161,
            "p5_strat_f1": float(p5_strat_f1),
            "p5_det_f1": float(p5_det_f1),
            "p6_strat_f1": float(p6_strat_f1),
            "p6_det_f1": float(p6_det_f1),
            "p7_peak_strat_f1": float(best_cand['strat_f1']),
            "p7_peak_det_f1": float(best_cand['det_f1']),
        },
        "best_candidate": best_cand,
        "disagreement_metrics": {
            "lh": float(disagree_lh),
            "lc": float(disagree_lc),
            "hc": float(disagree_hc),
            "corr_lh": float(corr_lh),
            "corr_lc": float(corr_lc),
            "corr_hc": float(corr_hc),
        },
        "error_analysis": {
            "total_errors": int(total_errors),
            "class_loss": class_loss,
            "top_confusions": conf_df.head(10).to_dict(orient='records'),
        },
        "targeted_evals": targeted_evals,
        "passes_gate": bool(passes_gate_threshold),
        "peak_gain": float(peak_gain),
        "changed_predictions": int(diffs),
        "changed_pct": float(diff_pct),
        "p7_sha256": sha_p7,
        "p5_sha256": compute_sha256(config.SUBMISSIONS_DIR / "submission_FINAL.csv")
    }
    
    with open('scratch/phase7_experiment_summary.json', 'w') as f:
        json.dump(p7_summary, f, indent=2)
    print("\nSaved scratch/phase7_experiment_summary.json")

if __name__ == '__main__':
    main()
