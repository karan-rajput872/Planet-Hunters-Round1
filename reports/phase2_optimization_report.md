# Phase 2: Final Model Optimization & Cross-Validation Report

## 1. Executive Summary
- **Competition**: ML Challenge Hack4Hack 2026 — Round 1
- **Phase Goal**: Verify pipeline integrity, run full 5-fold cross-validation, optimize hyperparameter configuration, test pseudo-labeling, and produce a high-generalization 5-fold ensemble candidate (`submission_v2.csv`) while preserving the existing single-best submission (`submission.csv`).
- **Original Holdout Benchmark**: LightGBM (Macro F1 = 0.5914)
- **Tuned Model Holdout**: LightGBM Tuned (`num_leaves=63, lr=0.035, n_est=600, min_child=30`): **0.5916**
- **5-Fold Stratified CV Mean Macro F1**: **0.5889 +/- 0.0017** (OOF Macro F1: **0.5890**)
- **New Submission**: `submissions/submission_v2.csv` (100% strictly validated)

---

## 2. Task 1 Verification Results
- **Reproducibility**: Re-evaluated `models/best_lightgbm.joblib` on the 80/20 stratified validation split. Obtained **0.5914** exact match.
- **Data Leakage Check**: Confirmed 0 test labels or outside data used. Feature extraction uses memory-mapped array processing with strictly per-star 1D time-series operations (no cross-sample leakage).
- **Detrending Integrity**: The 2D median filter along time (`axis=1`, window=49 cadences) subtracts rotational trends individually per star light curve. No validation labels enter preprocessing.

---

## 3. Task 2: 5-Fold Stratified Cross-Validation Summary
Trained across 5 folds on all 18,000 training stars:

| Fold | Baseline LightGBM F1 | Tuned LightGBM F1 |
|---|---|---|
| Fold 1 | 0.5831 | **0.5892** |
| Fold 2 | 0.5833 | **0.5890** |
| Fold 3 | 0.5808 | **0.5859** |
| Fold 4 | 0.5820 | **0.5908** |
| Fold 5 | 0.5855 | **0.5898** |
| **Mean +/- Std** | **0.5830 +/- 0.0016** | **0.5889 +/- 0.0017** |
| **Overall OOF Macro F1** | **0.5830** | **0.5890** |

---

## 4. Task 3: Planet Detection Analysis
- **Transit Depth & Noise**: The median detrended light curve feature `detrend_dip_snr = -detrend_p01 / detrend_mad` proved to be the single most potent transit detector.
- **Centroid Vetting During Dips**: Evaluating centroid shift specifically during flux minima (`cen_shift_in_dip`, `cen_shift_normalized`) successfully filtered background blended eclipsing binaries from true planets.
- **Odd / Even Transit Symmetry**: Planetary transits have identical depth across cycles, whereas eclipsing binaries alternate in primary/secondary depth.
- **Planet F1 Progression**:
  - Baseline starter notebook: ~0.35 F1
  - Phase 1 LightGBM: 0.4563 F1
  - Phase 2 Tuned 5-Fold CV: **0.4681 F1**

---

## 5. Task 4: Class Balancing & Multipliers
- Testing Nelder-Mead optimization on OOF probabilities confirmed that `class_weight='balanced'` in LightGBM already achieves globally calibrated class thresholds (optimal multipliers stay at 1.000).

---

## 6. Task 7: Pseudo-Labeling Experiment & Rejection
- Tested high-confidence pseudo-labeling on test stars with confidence threshold $\ge 0.85$ (2,648 stars).
- **Finding**: High-confidence predictions were severely skewed toward high-amplitude pulsators (1,014 stars) and instrument glitches (572 stars), while only 45 quiet stars were selected.
- **Validation Outcome**: Retraining with pseudo-labels caused validation Macro F1 to drop from 0.5916 to **0.5894**.
- **Decision**: In strict accordance with competition instructions, **pseudo-labeling was rejected**.

---

## 7. Submission Candidates Comparison

| Submission File | Architecture / Methodology | Validation Macro F1 | Status |
|---|---|---|---|
| **`submissions/submission_v2.csv`** (Recommended) | **Tuned 5-Fold CV Probability Ensemble** | **0.5889 +/- 0.0017 (OOF: 0.5890)** | **Recommended Candidate** |
| `submissions/submission.csv` | Single 80/20 LightGBM Model | 0.5914 (single holdout) | Preserved Candidate |

### Predicted Class Distributions:
| Class | `submission.csv` | `submission_v2.csv` |
|---|---|---|
| `pulsating_star` | 2,044 (29.2%) | 1,854 (26.5%) |
| `instrument_glitch` | 1,280 (18.3%) | 1,374 (19.6%) |
| `quiet_star` | 802 (11.5%) | 956 (13.7%) |
| `starspots` | 769 (11.0%) | 864 (12.3%) |
| `eclipsing_binary` | 677 (9.7%) | 688 (9.8%) |
| `planet` | 512 (7.3%) | 529 (7.6%) |
| `flare_star` | 543 (7.8%) | 449 (6.4%) |
| `background_binary` | 373 (5.3%) | 286 (4.1%) |
| **Total** | **7,000** | **7,000** |
