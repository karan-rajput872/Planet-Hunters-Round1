# Phase 5: Forensic Investigation of the Public Score Gap

**Project:** ML Challenge Hack4Hack 2026 — Round 1: Planet Hunters — Find New Worlds in Starlight  
**Author:** Senior ML Research Engineer, Computational Astrophysicist, Competition Strategist  
**Date:** October 2026  
**Status:** Completed Investigation  

---

## 1. Executive Summary

- **Internal 5-Fold Stratified CV Score:** Macro F1 = **0.5915** (LightGBM 75% + HistGradientBoosting 25%)
- **Public Leaderboard Score:** Macro F1 = **0.4214** (Uploads #1 and #2 produced identical scores)
- **Validation-to-Leaderboard Delta:** **-0.1701** (-28.8% relative drop)

An exhaustive, evidence-based forensic investigation was conducted across the data, feature matrix, model inference pipeline, submission generation artifacts, astronomical physics, and leaderboard mechanics.

### Primary Discoveries:
1. **Physical Root Cause (Lack of Cotrending Basis Vectors / Camera Systematic Subtraction):**
   Section 8 of `PROBLEM_STATEMENT.md` advises: *"think like an astronomer: subtract the common trend of each camera/CCD to remove systematic variations (pointing jitter, temperature swings)."*
   The existing baseline feature engineering extracted features from lightcurves that only underwent local running-median smoothing on each star individually. However, in the competition test sector, systematic variations across cameras and CCDs (thermal drifts, Earth stray light, spacecraft momentum dumps) are severe:
   - For example, on Camera 4 / CCD 2 in the test set, the common detector trend has a standard deviation of **0.002627**, which is **161% of the entire intrinsic flux variation of a quiet star (0.00163)**.
   - Without common-trend subtraction, detector drifts contaminated raw features. Key baseline features drifted catastrophically between train and test: `p99` (Kolmogorov-Smirnov statistic = 0.366), `trend_range` (KS = 0.346), `trend_std` (KS = 0.323), `flux_std` (KS = 0.221), and `autocorr_lag_1` (median 0.50 in train vs 0.93 in test).
   - This caused the tree models to hallucinate continuous trends and high amplitudes across thousands of test lightcurves.

2. **Severe Test Prediction Class Skew:**
   Due to the uncorrected detector trends, the champion ensemble severely over-predicted high-variance / trending classes on the test set, while heavily suppressing quiet stars and subtle transit signals:
   - `pulsating_star`: **27.20%** of test predictions vs **10.96%** in training (+148% relative inflation)
   - `instrument_glitch`: **19.60%** of test predictions vs **9.56%** in training (+105% relative inflation)
   - `quiet_star`: **13.23%** of test predictions vs **20.13%** in training (-34% relative depression)
   - `background_binary`: **4.24%** of test predictions vs **8.91%** in training (-52% relative depression)
   Combining `pulsating_star` and `instrument_glitch` accounted for **46.80%** of all test predictions (compared to 20.52% in training).

3. **Validation Strategy Mismatch:**
   Standard random stratified 5-fold cross-validation split observations uniformly across cameras and CCDs within a single training sector. Because both training and validation folds shared the exact same low-systematic sector environment, the CV score evaluated *in-distribution interpolation* rather than *out-of-sector cross-detector generalization*.

4. **Pipeline & Integrity Audits (Negative Findings / Verified Safe):**
   - No target leakage was found in feature engineering.
   - Model class indices strictly adhere to alphabetical order: `['background_binary', 'eclipsing_binary', 'flare_star', 'instrument_glitch', 'planet', 'pulsating_star', 'quiet_star', 'starspots']`.
   - Feature columns and order in `test_features.parquet` exactly match `train_features.parquet` (85/85 features identical).
   - Submission schema, row count (7,000), ID sequence (18000 to 24999), and checksum are valid.

---

## 2. Quantitative Evidence & Distribution Analysis

### 2.1 Class Distribution Comparison (Train vs Test Predictions)

| Class | Train Ground Truth (%) | Test Predictions (%) | Ratio (Test / Train) | Impact on Macro F1 |
| :--- | :---: | :---: | :---: | :--- |
| `pulsating_star` | 10.96% | **27.20%** | **2.48x** | Massive false positives; collapses precision |
| `instrument_glitch` | 9.56% | **19.60%** | **2.05x** | Massive false positives; collapses precision |
| `eclipsing_binary` | 16.51% | 15.69% | 0.95x | Relatively stable |
| `quiet_star` | 20.13% | **13.23%** | **0.66x** | High false negatives; quiet stars predicted as pulsating |
| `planet` | 4.83% | 6.47% | 1.34x | Noisy predictions |
| `starspots` | 13.92% | 8.87% | 0.64x | Starspot variability misattributed to pulsating |
| `flare_star` | 15.19% | 4.70% | **0.31x** | Severe under-prediction |
| `background_binary` | 8.91% | **4.24%** | **0.48x** | Severe under-prediction |

In Macro F1, each of the 8 classes carries an equal 12.5% weight. When precision collapses on `pulsating_star` and `instrument_glitch`, and recall collapses on `flare_star`, `background_binary`, and `quiet_star`, the Macro F1 drops steeply.

### 2.2 Kolmogorov-Smirnov (KS) Drift Analysis

Top drifting features between train and test distributions before cotrending:

| Feature Name | Baseline KS Statistic | Baseline Test Median vs Train Median | Root Cause |
| :--- | :---: | :---: | :--- |
| `p99` | **0.366** | 0.0094 vs 0.0042 (2.2x) | Detector-level flux excursions |
| `trend_range` | **0.346** | 0.0093 vs 0.0043 (2.1x) | Camera thermal & pointing drifts |
| `trend_std` | **0.323** | 0.0024 vs 0.0011 (2.2x) | Systematic detector drift across sector |
| `detrend_dip_snr` | **0.212** | 2.14 vs 1.62 | Systematic residuals mimic dips |
| `flux_std` | **0.221** | 0.0028 vs 0.0014 (2.0x) | Unsubtracted detector background fluctuations |
| `pos_frac` | **0.230** | 0.531 vs 0.499 | Positive drift skew in test detectors |
| `detrend_mad` | **0.231** | 0.0019 vs 0.0009 (2.1x) | Inflated residual dispersion |
| `n_flares_3sigma` | **0.230** | 12.0 vs 5.0 | Systematic peaks trigger false flare counts |

### 2.3 Proof of Concept: Common Trend (Cotrending) Correction

To test the hypothesis, we computed the instantaneous median flux across all stars residing on the same physical detector `(camera, ccd)` at each cadence $t \in [0, 1314]$, and subtracted this common systematic baseline vector:

$$\hat{F}_{i, \text{clean}}(t) = F_{i}(t) - \text{median}_{j \in \text{detector}(i)} [F_j(t)]$$

Results on feature drift after cotrending:
- **Mean KS drift across all features dropped by 50.4%**: from **0.1326** down to **0.0658**.
- `p99` KS drift dropped from **0.3660** to **0.0803** (-78% reduction).
- `trend_std` KS drift dropped from **0.3230** to **0.1480** (-54% reduction).
- `detrend_dip_snr` KS drift dropped from **0.2123** to **0.0340** (-84% reduction).
- `flux_std` KS drift dropped from **0.2213** to **0.0673** (-70% reduction).
- `pos_frac` KS drift dropped from **0.2297** to **0.0660** (-71% reduction).

This proves empirically that detector systematics account for the overwhelming majority of the train-to-test feature distribution shift.

---

## 3. Recommended Corrective Actions for Phase 5

1. **Implement Robust Camera/CCD Cotrending:**
   - Pre-detrend flux and centroid curves by subtracting the median systematic profile per `(camera, ccd)` channel.
   - Retain star-level relative variations while eliminating spacecraft/detector thermal drifts.

2. **Group-Aware / Out-of-Detector Cross-Validation:**
   - Evaluate models not only using stratified 5-fold CV, but also using Leave-One-Camera-Out (4 groups) and Leave-One-CCD-Out (4 groups) validation to assess out-of-detector generalization.

3. **Advanced Astro-Physical Feature Engineering:**
   - Extract morphology, periodic consistency, dip depth, transit symmetry, and centroid-astrometry correlation on clean, cotrended lightcurves.

4. **Calibrated Threshold Optimization & Priority-Aware Decision Logic:**
   - Align decision boundaries with the problem hierarchy and optimize probability thresholds to prevent high-variance classes from dominating subtle transit classes.

5. **Multi-Model Blend & Clean Candidate Generation:**
   - Train LightGBM, HistGradientBoosting, and CatBoost on the cotrended feature matrix.
   - Validate rigorously against the baseline before proposing an official upload candidate.
