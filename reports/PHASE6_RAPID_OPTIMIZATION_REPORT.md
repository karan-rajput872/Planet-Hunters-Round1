# 🔬 PHASE 6 RAPID PERFORMANCE OPTIMIZATION & VALIDATION REPORT
## Planet Hunters — Find New Worlds in Starlight (Hack4Hack 2026 — Round 1)

**Date & Time:** 2026-10-23, 08:58 AM IST  
**Deadline:** 23 October 2026, 10:00 AM IST  
**Author:** Principal Machine-Learning Competition Researcher, Astrophysical Time-Series Specialist & Validation Engineer  
**Status:** **PHASE 6 AUDIT COMPLETE — SCIENTIFIC BENCHMARK CONCLUDED**  
**Current Approved Submission:** `submissions/submission_FINAL.csv`  
**Verified SHA-256:** `6a378eae06765a28a39d41a322f47ff25512a43a47827ff4576940282b74330e`  

---

## 1. Executive Summary & Verification Ledger

Under strict competition safety protocols, Phase 6 conducted a rapid, evidence-driven optimization sprint evaluating:
1. **Ensemble Weight Re-Optimization:** Systematic grid search across the probability simplex for LightGBM, HistGradientBoosting, and CatBoost on the 88 cotrended astronomical features.
2. **Decision Rule & Multiplier Optimization:** Nested 5-fold cross-validation testing of class-specific decision thresholds and multiplier vectors to prevent artificial in-sample overfitting.
3. **Difficult Class Error Diagnostics:** In-depth confusion matrix analysis across the 8 classes, particularly false-positive confusion between planetary transits, background binaries, and eclipsing binaries.
4. **Safety & Integrity Checks:** Byte-for-byte SHA-256 verification of `submission_FINAL.csv` and `submission_FINAL_PHASE4_BACKUP.csv`, with all experimental outputs isolated into distinct artifacts (`submissions/submission_PHASE6_candidate.csv`).

### Official Submission Ledger

| Artifact Role | File Path | Verified SHA-256 Checksum | 14-Check Validator | Status |
|:---|:---|:---|:---:|:---:|
| **Current Approved Submission** | `submissions/submission_FINAL.csv` | `6a378eae06765a28a39d41a322f47ff25512a43a47827ff4576940282b74330e` | 14/14 PASS | **ACTIVE CHAMPION (Untouched)** |
| **Phase 4 Baseline Backup** | `submissions/submission_FINAL_PHASE4_BACKUP.csv` | `f53a08c47155bc907f855b0626cb38134aae298a58903b18f3d56818f0c053c1` | 14/14 PASS | **PRESERVED BACKUP** |
| **Phase 6 Candidate 01 (Grid Best)** | `submissions/submission_PHASE6_candidate_01.csv` | `243b382359960efcc2fb44a75dfaa993f906b0052b4d7479813c6f1bf9d7ac8b` | 14/14 PASS | **EXPERIMENTAL CANDIDATE** |
| **Phase 6 Experimental Candidate** | `submissions/submission_PHASE6_candidate.csv` | `243b382359960efcc2fb44a75dfaa993f906b0052b4d7479813c6f1bf9d7ac8b` | 14/14 PASS | **EXPERIMENTAL CANDIDATE** |

---

## 2. Experiments Performed

1. **Individual Component Model Matrix Generation:**
   - Evaluated 5 folds of LightGBM, HistGradientBoosting, and CatBoost across both Standard Stratified 5-Fold CV and Stratified Detector-Channel 5-Fold CV on `train_features_v5.parquet` (88 features, 18,000 stars).
   - Saved isolated out-of-fold probability matrices (`scratch/phase6_oof_*.npy`) and genuine out-of-fold detector matrices (`scratch/phase6_det_oof_*.npy`).
2. **Simplex Grid Search (Step Size 0.05):**
   - Evaluated 45 valid tri-ensemble simplex combinations: $w_{\text{LGB}} \in [0.35, 0.70]$, $w_{\text{HGB}} \in [0.15, 0.50]$, $w_{\text{CB}} \in [0.05, 0.30]$ subject to $\sum w = 1.0$.
3. **Candidate Architecture Benchmarking:**
   - Systematically tested the specified candidates:
     - Candidate A: 60% LGB + 30% HGB + 10% CB
     - Candidate B: 55% LGB + 35% HGB + 10% CB
     - Phase 5 Approved: 50% LGB + 40% HGB + 10% CB
     - Candidate C: 45% LGB + 40% HGB + 15% CB
     - Candidate D: 50% LGB + 35% HGB + 15% CB
     - Candidate E: 60% LGB + 25% HGB + 15% CB
     - Candidate F: 55% LGB + 30% HGB + 15% CB
     - Candidate G: 65% LGB + 25% HGB + 10% CB
     - Candidate H: 40% LGB + 45% HGB + 15% CB
     - Candidate I: 70% LGB + 20% HGB + 10% CB
4. **Nested 5-Fold Cross-Validation Decision Multiplier Tuning:**
   - Tested whether post-processing probability multipliers $w_c \cdot P_c$ generalize to held-out folds.
5. **Difficult Class Error Matrix Breakdown:**
   - Quantified pairwise confusion between `planet`, `eclipsing_binary`, `background_binary`, `starspots`, and `quiet_star`.
6. **Mission Control UI Enhancement:**
   - Built interactive Streamlit station **Phase 6 — Optimization Lab & Candidate Preview** (`dashboard/components/phase6_preview.py`) providing Panels A through G.

---

## 3. Experiments Rejected and Why

| Experiment | Tested Approach | Empirical Outcome | Technical Reason for Rejection |
|:---|:---|:---|:---|
| **Class Decision Multiplier Optimization** | Nelder-Mead optimization on OOF probabilities ($\arg\max w_c P_c$) | In-sample delta: +0.0000; Nested CV delta: +0.0000 across all 5 folds | The predicted probabilities from the tri-ensemble are already well-calibrated. Post-hoc multipliers did not produce any genuine out-of-fold improvement and risk severe test distribution distortion. **Preserved Raw Argmax.** |
| **High LightGBM Skew (60/25/15 and 70/20/10)** | Increasing LightGBM weight to 60–70% | Stratified OOF dropped to 0.6436–0.6445 (-0.0019 vs Phase 5) | Over-weighting LightGBM increases tree variance and reduces the regularizing benefit of HistGradientBoosting's histogram binning and CatBoost's oblivious trees. |
| **High CatBoost Skew (w_cb > 20%)** | Increasing CatBoost weight beyond 15% | Stratified OOF dropped below 0.6420 | CatBoost alone achieves 0.6215 OOF; excessive weight pulls down the aggregate precision on narrow transit depths. |
| **Speculative Feature Additions** | Adding untested time-series features without independent cotrending | Skipped per protection guidelines | Adding unvetted features with 50 minutes until deadline risks data leakage, pipeline failure, and breaking deterministic reproducibility. |

---

## 4. Ensemble Weight Benchmark Results

All models evaluated on the exact same 18,000 training stars using identical 5-fold partitions.

### Component Model Standalone Performance

| Model Family | Standard Stratified OOF Macro F1 | Stratified Detector-Channel OOF Macro F1 | Notes |
|:---|:---:|:---:|:---|
| **LightGBM (Single)** | 0.6413 | 0.6306 | Leaf-wise best-first tree growth (350 trees) |
| **HistGradientBoosting (Single)** | 0.6401 | 0.6273 | Depth-wise histogram regularized trees (250 trees) |
| **CatBoost (Single)** | 0.6215 | 0.6122 | Oblivious symmetric decision trees (400 trees) |

### Ensemble Comparison Table

| Candidate Name | LGB % | HGB % | CB % | Standard Stratified OOF | Detector-Channel OOF | Strat Fold Std ($\sigma$) | Det Fold Std ($\sigma$) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Candidate E** | 60% | 25% | 15% | 0.6436 | 0.6350 | ±0.0037 | ±0.0138 |
| **Candidate A** | 60% | 30% | 10% | 0.6441 | 0.6343 | ±0.0038 | ±0.0130 |
| **Candidate G** | 65% | 25% | 10% | 0.6441 | 0.6338 | ±0.0040 | ±0.0129 |
| **Candidate F** | 55% | 30% | 15% | 0.6444 | 0.6346 | ±0.0038 | ±0.0133 |
| **Candidate D** | 50% | 35% | 15% | 0.6445 | 0.6347 | ±0.0034 | ±0.0136 |
| **Candidate I** | 70% | 20% | 10% | 0.6445 | 0.6334 | ±0.0047 | ±0.0129 |
| **Candidate (60/35/5)** | 60% | 35% | 5% | 0.6447 | 0.6333 | ±0.0043 | ±0.0135 |
| **Candidate (55/40/5)** | 55% | 40% | 5% | 0.6456 | 0.6341 | ±0.0040 | ±0.0135 |
| **Candidate B (55/35/10)** | 55% | 35% | 10% | 0.6454 | 0.6345 | ±0.0041 | ±0.0139 |
| **Phase 5 Approved (Champion)** | **50%** | **40%** | **10%** | **0.6455** | **0.6336** | **±0.0038** | **±0.0137** |
| **Candidate C (45/40/15)** | 45% | 40% | 15% | 0.6455 | 0.6340 | ±0.0028 | ±0.0138 |
| **Candidate H (40/45/15)** | 40% | 45% | 15% | 0.6457 | 0.6339 | ±0.0027 | ±0.0142 |
| **Grid Best Balanced (45/45/10)** | **45%** | **45%** | **10%** | **0.6461** | **0.6338** | **±0.0032** | **±0.0138** |

---

## 5. Decision Optimization & Calibration Findings

### Nested 5-Fold Cross-Validation Test
To test whether optimizing class decision multipliers $\arg\max (w_c \cdot P_{i, c})$ provides real generalization, we trained multiplier vectors on 4 folds and evaluated on the held-out 5th fold:

| Fold Index | Validation Stars | Raw Argmax Macro F1 | Multiplier Tuned Macro F1 | Out-of-Fold Delta |
|:---:|:---:|:---:|:---:|:---:|
| **Fold 1** | 3,600 | 0.6424 | 0.6424 | +0.0000 |
| **Fold 2** | 3,600 | 0.6429 | 0.6429 | +0.0000 |
| **Fold 3** | 3,600 | 0.6435 | 0.6435 | +0.0000 |
| **Fold 4** | 3,600 | 0.6454 | 0.6454 | +0.0000 |
| **Fold 5** | 3,600 | 0.6527 | 0.6527 | +0.0000 |
| **Mean ± Std** | **18,000** | **0.6454 ± 0.0038** | **0.6454 ± 0.0038** | **+0.0000** |

**Conclusion:** The multiplier vector converges to $[1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00]$. The probabilities output by the tri-ensemble are already properly balanced across the 8 classes. Attempting to force threshold shifts yields zero holdout gain and would increase variance on the hidden test set. Raw argmax selection was retained.

---

## 6. Difficult Class Investigation & Confusion Patterns

Analysis of the 18,000 out-of-fold predictions reveals key astrophysical boundaries:

### Confusion Matrix (Phase 5 Approved OOF)

```
                    pred_bb  pred_eb  pred_fl  pred_ig  pred_pl  pred_ps  pred_qs  pred_sp   Total
true_background_bin    795      206        1       10      147        2      240      203    1604
true_eclipsing_bin     216     1498        0        7      165        3      185      173    2247
true_flare_star          8        3     1031       29       14       43      401      275    1804
true_instrument_glitch  10        4       23     1360       48       40      151       85    1721
true_planet             74       43        4       12      861       10      699      442    2145
true_pulsating_star      5        4       39       27        7     1316      468      107    1973
true_quiet_star         10        3        9        9       69       42     3019      457    3624
true_starspots          21        4       13       11      105       67      956     1705    2882
```

### Key Confusion Insights
1. **`planet` vs `quiet_star` (699 false negatives):** The dominant error for planets is shallow transits (small planet radius $R_p$) sinking below the observational noise floor of faint host stars ($T_{\text{mag}} > 14$).
2. **`starspots` vs `quiet_star` (956 misclassifications):** Low-amplitude rotational spot modulations (amplitude $< 5\times 10^{-4}$) blur into quiet star photon shot noise.
3. **`planet` vs `background_binary` (74 vs 147):** Background eclipsing binaries diluted by primary star flux mimic transit depths. The astrometric centroid displacement features (`cen_shift_in_dip`, `cen_disp_mean`) correctly catch 795 background binaries, but low-SNR aperture dilutions remain difficult.
4. **`planet` vs `eclipsing_binary` (43 vs 165):** Solved effectively by odd-even depth ratio (`transit_odd_even_ratio`), which successfully isolates true grazing binaries.

---

## 7. Final Validation Gate Comparison

| Metric | Existing Phase 5 Approved (50/40/10) | Phase 6 Candidate (45/45/10) | Delta | Assessment |
|:---|:---:|:---:|:---:|:---:|
| **Standard OOF Macro F1** | 0.6455 | 0.6461 | +0.0006 | Marginal statistical gain |
| **Detector-channel OOF Macro F1** | 0.6336 | 0.6338 | +0.0002 | Within fold noise |
| **Planet F1** | 0.4591 | 0.4606 | +0.0015 | Minor improvement |
| **Starspots F1** | 0.5330 | 0.5339 | +0.0010 | Minor improvement |
| **Background binary F1** | 0.5797 | 0.5824 | +0.0027 | Minor improvement |
| **Flare F1** | 0.6660 | 0.6652 | -0.0009 | Slight degradation |
| **Pulsating star F1** | 0.7402 | 0.7396 | -0.0006 | Slight degradation |
| **Instrument glitch F1** | 0.8193 | 0.8182 | -0.0011 | Slight degradation |
| **Quiet star F1** | 0.6197 | 0.6194 | -0.0003 | Neutral |
| **Standard Fold Std ($\sigma$)** | ±0.0038 | ±0.0032 | -0.0006 | Marginally lower fold variance |
| **Detector Fold Std ($\sigma$)** | ±0.0137 | ±0.0138 | +0.0001 | Identical detector stability |
| **Test Predictions Changed** | Baseline (0) | 30 / 7,000 (0.43%) | — | **99.57% prediction identity** |

### Statistical Significance Analysis
The measured improvement of **+0.0006** on Standard OOF and **+0.0002** on Detector OOF is substantially smaller than the fold-to-fold standard deviation ($\sigma_{\text{strat}} = \pm 0.0038$, $\sigma_{\text{det}} = \pm 0.0137$).
Out of 7,000 test stars, only **30 labels change** (0.43%), while 6,970 remain exactly identical.

Under the prompt's Non-Negotiable Gate Rule:
> *"A tiny improvement in one validation score is not enough to justify replacing the current submission."*

Replacing the approved submission for a +0.0002 detector gain on 30 shifting stars introduces unnecessary last-minute operational risk without statistical justification.

---

## 8. Experimental Candidate Verification

Experimental candidate files were generated and validated for inspection purposes:
- **Primary Candidate File:** `submissions/submission_PHASE6_candidate_01.csv`
- **Secondary Candidate File:** `submissions/submission_PHASE6_candidate.csv`
- **SHA-256 Checksum (both bitwise identical):** `243b382359960efcc2fb44a75dfaa993f906b0052b4d7479813c6f1bf9d7ac8b`
- **Row Count:** Exactly 7,000 data rows.
- **Columns:** Exactly two columns: `id`, `label`.
- **Validation Command:** `.venv\Scripts\python.exe validate_submission.py submissions/submission_PHASE6_candidate_01.csv` -> **14/14 CHECKS PASSED**.
- **Unit Tests:** `.venv\Scripts\python.exe -m unittest discover tests` -> **11/11 TESTS PASSED**.

---

## 9. Mission Control Visual Preview Status

The Streamlit Mission Control platform was successfully updated with the required **PHASE 6 — OPTIMIZATION LAB & CANDIDATE PREVIEW** station (`dashboard/components/phase6_preview.py`):
- **Local URL:** `http://localhost:8501`
- **Panel A (Candidate Comparison):** Displays Phase 4 baseline, Phase 5 approved, and Phase 6 experimental candidate side by side.
- **Panel B (Ensemble Weight Explorer):** Interactive table and scatter plot showing all 10 candidate weight combinations.
- **Panel C (Class Performance Comparison):** Per-class F1 grouped bar chart and delta waterfall table.
- **Panel D (Confusion Matrix Preview):** Interactive heatmaps for both Phase 5 approved and Phase 6 experimental candidates.
- **Panel E (Prediction Comparison):** Highlights 30 differing test rows (0.43%), top label shift pairs, and class distributions.
- **Panel F (Submission Readiness):** Displays file metadata, 14-rule audit status, row count, and SHA-256 checksums.
- **Panel G (Preview & Approval Controls):** Clear tabs for inspecting `submission_FINAL.csv`, `submission_PHASE6_candidate.csv`, and audit logs, with explicit warnings:
  - `"CURRENT APPROVED SUBMISSION: submissions/submission_FINAL.csv"`
  - `"EXPERIMENTAL CANDIDATE — NOT YET APPROVED FOR COMPETITION UPLOAD"`

---

## 10. Remaining Risks & Competition Safety

1. **Overfitting to Public Leaderboard:** The Phase 4 public leaderboard score (0.4214) was infected by instrumental common trends. Phase 5 cotrending increased out-of-detector generalization by +0.1175 (0.5161 -> 0.6336). The Phase 5 submission has not yet been scored online. Swapping submissions for a +0.0002 offline difference would risk replacing a sound model on statistical noise.
2. **Submission Invariance:** Because 6,970 out of 7,000 predictions are identical between Phase 5 and Phase 6, the expected leaderboard difference is $< 0.001$.
3. **Rollback Assurance:** If needed, the byte-for-byte Phase 4 backup is verified at `submissions/submission_FINAL_PHASE4_BACKUP.csv` (`f53a08c4...`).

---

## 11. Final Engineering Recommendation

### **RECOMMENDATION: RETAIN PHASE 5 — NO RELIABLE IMPROVEMENT**

### Scientific & Operational Justification:
1. **Statistically Indistinguishable:** The best experimental candidate (45% LGB + 45% HGB + 10% CB) yields a detector-channel OOF gain of only $+0.0002$ and a stratified OOF gain of $+0.0006$. Both values are well inside the standard cross-validation error margin ($\pm 0.0137$).
2. **High Prediction Identity (99.57%):** Only 30 predictions out of 7,000 change. 
3. **Threshold Tuning Failure:** Post-processing decision multiplier tuning failed to generalize out-of-fold (+0.0000 gain across all 5 folds), confirming that raw argmax probability thresholding remains the optimal, un-overfitted strategy.
4. **Preservation of Approved Candidate:** The current approved submission `submissions/submission_FINAL.csv` (`6a378eae06765a28a39d41a322f47ff25512a43a47827ff4576940282b74330e`) represents our strongest, most rigorously validated architecture and remains approved for competition submission.
