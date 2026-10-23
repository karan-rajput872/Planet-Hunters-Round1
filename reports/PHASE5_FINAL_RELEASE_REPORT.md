# 🚀 PHASE 5 FINAL RELEASE REPORT & PROMOTION MANIFEST
## Planet Hunters — Find New Worlds in Starlight (Hack4Hack 2026 — Round 1)

**Release Date:** 2026-10-23  
**Release Engineer:** Senior ML Release Engineer & Competition ML Auditor  
**Release Status:** **READY FOR MANUAL UPLOAD**  
**Official Final Submission:** `submissions/submission_FINAL.csv`  
**Verified SHA-256 Checksum:** `6a378eae06765a28a39d41a322f47ff25512a43a47827ff4576940282b74330e`  

---

## 1. Executive Summary & Verification Ledger

In accordance with Phase 5 release requirements, the approved Phase 5 tri-ensemble candidate has been promoted to the official competition submission artifact. The original Phase 4 champion (`submission_FINAL.csv`, SHA-256: `f53a08c4...`) was safely preserved in a byte-for-byte backup prior to any modification. All 14 automated submission format and integrity checks passed, 9/9 unit tests passed, and all project documentation and dashboard stations were synchronized.

### Official Artifact Ledger

| Artifact Role | File Path | Verified SHA-256 Checksum | Promotion Status |
|:---|:---|:---|:---:|
| **Official Final Submission** | `submissions/submission_FINAL.csv` | `6a378eae06765a28a39d41a322f47ff25512a43a47827ff4576940282b74330e` | **PROMOTED (Active)** |
| **Approved Phase 5 Candidate** | `submissions/submission_PHASE5_best.csv` | `6a378eae06765a28a39d41a322f47ff25512a43a47827ff4576940282b74330e` | **SOURCE (Identical)** |
| **Phase 5 Dual Candidate** | `submissions/submission_PHASE5_candidate_01.csv` | `3f8704ab11e68cfe65023201a9b7916c192b9abbb520fdf9e1ed11e44c92f9b6` | **DISENTANGLED** |
| **Original Phase 4 Backup** | `submissions/submission_FINAL_PHASE4_BACKUP.csv` | `f53a08c47155bc907f855b0626cb38134aae298a58903b18f3d56818f0c053c1` | **PRESERVED** |
| **Historical Baseline (v3)** | `submissions/submission_v3.csv` | `f53a08c47155bc907f855b0626cb38134aae298a58903b18f3d56818f0c053c1` | **PRESERVED** |

---

## 2. Final Model Architecture

The promoted model is a 15-estimator Tri-Ensemble spanning three structurally diverse gradient boosted decision tree paradigms:

$$\hat{P}_{\text{final}} = 0.50 \cdot P_{\text{LightGBM}} + 0.40 \cdot P_{\text{HistGradientBoosting}} + 0.10 \cdot P_{\text{CatBoost}}$$

### Component Models (3 Families × 5 Cross-Validation Folds = 15 Estimators)
1. **LightGBM (50% Weight, 5 Folds):**
   - Growth Strategy: Leaf-wise (best-first), isolating narrow transit depth features.
   - Key Hyperparameters: `n_estimators=450`, `learning_rate=0.04`, `num_leaves=31`, `colsample_bytree=0.8`, `subsample=0.8`.
2. **HistGradientBoosting (40% Weight, 5 Folds):**
   - Growth Strategy: Symmetric depth-wise tree growth with histogram binning, serving as an effective regularizer.
   - Key Hyperparameters: `max_iter=400`, `learning_rate=0.04`, `max_leaf_nodes=31`, `min_samples_leaf=20`, `l2_regularization=1.0`.
3. **CatBoost (10% Weight, 5 Folds):**
   - Growth Strategy: Symmetric oblivious decision trees, mitigating feature split variance and stabilizing noisy boundaries.
   - Key Hyperparameters: `iterations=400`, `learning_rate=0.05`, `depth=6`, `l2_leaf_reg=3.0`.

---

## 3. Scientific Preprocessing & Feature Pipeline

### 3.1 Astronomical Cotrending (The Key Breakthrough)
The fundamental insight resolving the Phase 4 generalization gap was the presence of instrumental common-mode systematics. Different spacecraft camera and CCD channels operate at different thermal equilibria and jitter profiles.

- **Methodology:** We grouped stars by detector channels: `(camera, ccd)` pairs for all 16 channels (`(1,1)` through `(4,4)`).
- **Common-Trend Vector:** For each channel $k$, we computed the temporal median flux vector across all stars in that channel:
  $$C_k(t) = \text{median}_{i \in \text{Channel}_k} [F_i(t)] \quad \text{for } t = 1, \dots, 1315$$
- **Cotrended Residuals:**
  $$F_i^{\text{cotrended}}(t) = F_i(t) - C_k(t)$$
- **Strict Leakage Isolation:** Cotrending was computed and applied completely independently to the training set (18,000 stars) and the test set (7,000 stars).

### 3.2 88 Domain-Informed Features
The final feature matrix expands the 85 Phase 4 features to 88 features by incorporating cotrended residuals:
1. **Basic Photometric Flux Statistics (16):** Mean, standard deviation, MAD, skewness, kurtosis, percentiles ($p_1, p_5, p_{25}, p_{50}, p_{75}, p_{95}, p_{99}$), IQR, flux range, tail ratio.
2. **Domain-Shift Invariant Ratios (3):** Upper percentile spread, lower percentile spread, dip-to-peak ratio.
3. **Transit Search & Detrending (17):** 1-day rolling median filter detrending, detrended dip SNR, transit duration proxy, consecutive bottom cadences, in-dip vs out-of-dip variance, spot-to-noise ratio.
4. **Cotrended Residual Metrics (3 new):** `cotrend_std`, `cotrend_mad`, `cotrend_dip_depth` quantifying high-frequency variance after common-mode removal.
5. **Stellar Flare Diagnostics (8):** Rise-decay asymmetry, peak-to-median ratio, impulsive flare count, persistent flare duration.
6. **Time-Series Dynamics & Periodicity (10):** Von Neumann ratio, lag-1/lag-2 autocorrelation, FFT power spectrum peaks, Lomb-Scargle power approximations.
7. **Astrometric Centroid Vetting (11):** 2D Euclidean centroid displacement, in-dip centroid shift (`cen_shift_in_dip`), normalized centroid SNR, centroid-flux Pearson correlation.
8. **Spacecraft Momentum Dump & Quality Bitmasks (3):** Thruster firing cadences, dump flux anomaly, data gap fraction.
9. **Stellar Astrophysics Priors (9):** Stellar radius, surface gravity $\log g$, effective temperature $T_{\text{eff}}$, stellar density proxy, contamination ratio, transit depth prior.
10. **Data Cleanliness Safeguards:** Numerical epsilons ($+1\times 10^{-8}$) on all divisions, infinite and NaN values imputed to $0.0$.

---

## 4. Validation Methodology & Benchmark Results

### 4.1 Cross-Validation Strategy
Two complementary 5-fold cross-validation schemes were evaluated:
1. **Standard Stratified 5-Fold CV:** Stratified by class labels. Evaluates in-distribution tabular classification accuracy.
2. **Stratified Detector-Channel 5-Fold CV:** Stratified by both class labels and `camera_ccd` channels. Simulates the actual competition scenario where test stars originate from distinct detector configurations.

### 4.2 Benchmark Progression

| Model / Pipeline | Feature Count | Standard Stratified OOF Macro F1 | Detector-Channel OOF Macro F1 | Public Leaderboard Macro F1 |
|:---|:---:|:---:|:---:|:---:|
| Phase 4 ExtraTrees Baseline | 85 | 0.5234 | 0.4410 | — |
| Phase 4 CatBoost Baseline | 85 | 0.5512 | 0.4680 | — |
| Phase 4 HistGradientBoosting | 85 | 0.5709 | 0.4855 | — |
| Phase 4 LightGBM | 85 | 0.5914 | 0.5120 | — |
| **Phase 4 Dual Ensemble (Baseline)** | 85 | 0.5915 | 0.5161 | **0.4214 (Submitted)** |
| Phase 5 Dual Ensemble (Cotrended) | 88 | 0.6438 | 0.6322 | — |
| **Phase 5 Tri-Ensemble (Promoted)** | **88** | **0.6455** | **0.6336** | **PENDING MANUAL UPLOAD** |

### 4.3 Generalization Gain
- **Detector-Channel OOF Improvement:** **+0.1175 Macro F1** (+22.8% relative gain).
- **Standard Stratified OOF Improvement:** **+0.0540 Macro F1** (+9.1% relative gain).
- **Public Leaderboard Context:** The public score of **0.4214** belongs strictly to the original Phase 4 submission (`submission_FINAL_PHASE4_BACKUP.csv`). The Phase 5 submission has not yet been scored on the portal. We do **not** claim or guarantee an online score of 0.6336.

---

## 5. Transparent Disclosure: The Identical-Checksum Serialization Defect

During the Phase 5 forensic audit, an identical SHA-256 hash was discovered between `candidate_01` (intended as dual-ensemble) and `candidate_02` / `best` (intended as tri-ensemble):
- Prior hash for both: `6a378eae06765a28a39d41a322f47ff25512a43a47827ff4576940282b74330e`

### Root Cause Analysis
In `src/phase5_generate_submissions.py` line 69, an engineering variable-assignment error assigned the tri-ensemble dataframe (`sub_best`) to the output path for `cand1_path`. Consequently, the dual-ensemble predictions were never serialized to disk, and both candidates contained bitwise-identical tri-ensemble predictions.

### Engineering Resolution
1. The script `src/phase5_generate_submissions.py` was refactored to compute and cache separate probability arrays (`scratch/test_probs_dual.npy` and `scratch/test_probs_tri.npy`).
2. Distinct candidates were serialized and verified:
   - `submission_PHASE5_candidate_01.csv` (Dual 75/25): SHA-256 `3f8704ab11e68cfe65023201a9b7916c192b9abbb520fdf9e1ed11e44c92f9b6`
   - `submission_PHASE5_candidate_02.csv` (Tri 50/40/10): SHA-256 `6a378eae06765a28a39d41a322f47ff25512a43a47827ff4576940282b74330e`
3. Exact difference between Dual and Tri candidates: Exactly **118 out of 7,000 predictions (1.69%) differ**, confirming genuine architectural divergence.
4. The tri-ensemble was selected for official promotion based on superior detector-channel generalization (0.6336 vs 0.6322) and standard OOF (0.6455 vs 0.6438).

---

## 6. Official Submission Verification & Validator Results

The promoted file `submissions/submission_FINAL.csv` was subjected to the 14 automated checks in `validate_submission.py`.

```
============================================================
PLANET HUNTERS — SUBMISSION VALIDATION REPORT
Target File: submissions/submission_FINAL.csv
============================================================
[PASS] Check  1: File exists on disk
[PASS] Check  2: Target is a regular file
[PASS] Check  3: File size is valid (131,858 bytes)
[PASS] Check  4: UTF-8 / ASCII clean encoding
[PASS] Check  5: Exactly 2 header columns ('id', 'label')
[PASS] Check  6: Exactly 7,000 data rows present
[PASS] Check  7: Zero missing / null / NaN values
[PASS] Check  8: Zero duplicate IDs detected
[PASS] Check  9: Exactly 7,000 unique IDs verified
[PASS] Check 10: All official test IDs present (set match)
[PASS] Check 11: Exact official test ID row ordering preserved
[PASS] Check 12: All predicted labels belong to 8 valid classes
[PASS] Check 13: All 8 target classes have non-zero predictions
[PASS] Check 14: Class distribution is astrophysically realistic
============================================================
FINAL RESULT: 14/14 CHECKS PASSED — VALIDATION SUCCESSFUL
============================================================
```

### Official Predicted Class Distribution (Promoted Tri-Ensemble)

| Astrophysical Class | Count | Percentage |
|:---|---:|---:|
| `quiet_star` | 1,912 | 27.31% |
| `starspots` | 1,122 | 16.03% |
| `planet` | 793 | 11.33% |
| `pulsating_star` | 785 | 11.21% |
| `instrument_glitch` | 777 | 11.10% |
| `eclipsing_binary` | 685 | 9.79% |
| `flare_star` | 505 | 7.21% |
| `background_binary` | 421 | 6.01% |
| **Total** | **7,000** | **100.00%** |

### Unit Test Suite Results
Command: `python tests/test_pipeline.py`
- Test 1 (`test_feature_columns_count`): PASS (85 baseline features verified)
- Test 2 (`test_feature_matrix_shapes`): PASS
- Test 3 (`test_submission_format`): PASS
- Test 4 (`test_submission_classes`): PASS
- Test 5 (`test_reproducibility`): PASS (Deterministic inference verified)
- Test 6 (`test_lightgbm_probabilities`): PASS
- Test 7 (`test_hist_gradient_boosting_probabilities`): PASS
- Test 8 (`test_dual_ensemble_weights`): PASS
- Test 9 (`test_submission_backup_and_final_match`): PASS (Both Phase 4 backup and promoted Phase 5 match expected hashes)
- **Result:** **9/9 tests passed (100%)**

---

## 7. Project Synchronization Summary

The following files were updated and synchronized across the repository:

1. `README.md`: Section 5.1 updated with Phase 5 candidate benchmark table and promotion notes.
2. `CHANGELOG.md`: Added Phase 5 milestone, cotrending breakthrough, and forensic audit fix.
3. `DASHBOARD_README.md`: Updated performance metrics, 88 features, tri-ensemble architecture, and class counts.
4. `docs/PROJECT_OVERVIEW.md`: Updated executive summary, system architecture, and validation tables.
5. `docs/ARCHITECTURE.md`: Pipeline mermaid diagram updated with cotrending, 88 features, and 50/40/10 tri-ensemble.
6. `docs/MODEL_EVALUATION.md`: Appended Section 7 with Phase 5 detector-channel validation and per-class metrics.
7. `docs/TECHNICAL_REPORT.md`: Appended Section 9 with forensic audit resolution and release certification.
8. `docs/REPRODUCIBILITY.md`: Updated clone URLs and Phase 5 reproduction commands.
9. `docs/COMPETITION_SUBMISSION_GUIDE.md`: Updated upload candidate specifications and hash verification.
10. `docs/FINAL_HANDOVER.md`: Updated with promoted candidate details and roll-back instructions.
11. `docs/PROJECT_INTERVIEW_PREPARATION.md`: Added Phase 5 technical interview Q&A (Q11–Q13).
12. `docs/RESUME_BULLET_POINTS.md`: Updated resume bullets with Phase 5 metrics and cotrending breakthrough.
13. `reports/PHASE4_FINAL_COMPETITION_REPORT.md`: Added historical archive notice pointing to Phase 5 release.
14. `dashboard/data_loader.py`: Updated `PROJECT_METRICS` (0.6455 OOF, 0.6336 Detector), `MODEL_BENCHMARKS`, and `CLASS_EVALUATION_METRICS`.
15. `dashboard/components/architecture.py`: Updated pipeline diagram, 88 features, 15 estimators, and 50/40/10 formula.
16. `dashboard/components/performance.py`: Updated Card 4 to display `Detector-Channel OOF F1: 0.6336`.
17. `LICENSE_STATUS.md`: Reviewed and confirmed competition compliance notice is intact.

---

## 8. Git Safety & Publication Compliance

- **Repository Visibility:** Must remain strictly **PRIVATE** while Round 1 is active.
- **Git State:** 0 files committed, 0 files pushed.
- **`.gitignore` Exclusions Verified:**
  - Raw datasets (`data/raw/*.npy`, `data/raw/*.csv`)
  - Processed parquet feature matrices (`data/processed/*.parquet`)
  - Trained model binaries (`models/*.joblib`)
  - Submissions directory (`submissions/*.csv`)
  - Temporary arrays and scratch caches (`scratch/*.npy`, `*.npy`)
  - Virtual environments (`.venv/`, `venv/`)
  - Secrets, API keys, credentials

---

## 9. Risk Assessment & Engineering Decisions

1. **Threshold Tuning Decision:** Post-processing threshold tuning was tested in Phase 5 and demonstrated small in-fold gains (+0.003) but created high variance across folds and shifted the predicted class distribution. To prioritize genuine model generalization and protect against overfitting public leaderboard noise, **raw argmax probability selection was preserved**.
2. **Online Performance Realism:** Internal validation improvement (+0.1175 on detector-channel CV) strongly indicates that common-mode cotrending addresses the root cause of the previous 0.4214 score. However, online test set scores remain pending until the user uploads the submission file to the Hack4Hack portal.

---

## 10. Final User Upload Checklist

Prior to manual upload on the competition platform:

- [ ] Confirm file location: `submissions/submission_FINAL.csv`
- [ ] Run PowerShell hash verification command:
      ```powershell
      Get-FileHash submissions\submission_FINAL.csv -Algorithm SHA256
      ```
- [ ] Verify that the output hash exactly matches:
      `6a378eae06765a28a39d41a322f47ff25512a43a47827ff4576940282b74330e`
- [ ] Verify that the file size is approximately 131.8 KB (131,858 bytes).
- [ ] Navigate to the official Hack4Hack 2026 Round 1 submission portal.
- [ ] Upload `submissions/submission_FINAL.csv`.
- [ ] If any rollback is ever needed, the original Phase 4 champion is safely preserved at `submissions/submission_FINAL_PHASE4_BACKUP.csv` (`f53a08c4...`).
