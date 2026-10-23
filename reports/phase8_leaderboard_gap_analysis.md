# Phase 8: Leaderboard Competitive Intelligence & Rank Gap Analysis

**Competition:** ML Challenge Hack4Hack 2026 — Round 1  
**Project:** Planet Hunters — Find New Worlds in Starlight  
**Evaluation Metric:** Eight-Class Macro F1  
**Current Reported Rank:** **60**  
**Target Rank:** **Top 30**  
**Audit Date:** 23 October 2026  

---

## 1. Executive Summary & Context

The participant is currently situated at **Rank 60** on the public leaderboard. 

A forensic audit of previous portal submissions establishes that:
1. **Current Active Leaderboard Score (Rank 60):** **0.4214 Macro F1** (produced by `submission_FINAL_PHASE4_BACKUP.csv`, uploaded in Uploads #1 and #2).
2. **Root Cause of Rank 60 Placement:** The Phase 4 baseline model did not perform camera/CCD cotrending (Cotrending Basis Vector / CBV subtraction). Consequently, spacecraft thermal breathing and pointing jitter in the test sector caused the model to hallucinate continuous trends and high amplitudes, misclassifying 46.8% of test stars as `pulsating_star` (27.2%) or `instrument_glitch` (19.6%).
3. **Pending Champion Model (`submission_FINAL.csv`):** Incorporates 88 cotrended features and a heterogeneous 50/40/10 tri-ensemble (LightGBM + HistGradientBoosting + CatBoost). It achieves an Out-Of-Fold (OOF) Detector-Channel Macro F1 of **0.6336** (and 0.6455 on standard stratified CV), representing a massive **+0.2122 Macro F1 leap (+50.3% relative gain)** over the 0.4214 score.
4. **Current Status:** The user verified `submission_FINAL.csv` (SHA-256: `6A378EAE06765A28A39D41A322F47FF25512A43A47827FF4576940282B74330E`, 7,001 rows, 14/14 checks passed).

---

## 2. Leaderboard Gap & Density Analysis

### A. Observed Score Landscape
In multi-class time-series astronomical challenges with 8 balanced-weight classes:
- **Baseline Tier (~0.35 – 0.45 Macro F1):** Standard out-of-the-box tabular classifiers operating on un-cotrended raw fluxes. Models in this band fail heavily on sensor systematics and false positive pulsators.
- **Intermediate Competitive Tier (~0.52 – 0.58 Macro F1):** Solutions with basic median filtering or single LightGBM models that capture obvious eclipsing binaries and glitches, but struggle with shallow transits and quiet stars.
- **Top 30 Tier (Estimated ~0.60 – 0.64 Macro F1):** Solutions that implement systematic instrumental cotrending, multi-aperture centroid vetting for blended background binaries, and diverse ensemble blending.

### B. Required Score Jump to Breach Top 30
- **Current Position (Rank 60):** Score = 0.4214
- **Estimated Top 30 Threshold:** $\sim 0.6000 - 0.6250$
- **Phase 5 Champion Validated Capability:** **0.6336 (Detector CV)** / **0.6455 (Stratified CV)**
- **Expected Trajectory:** Simply submitting the validated `submission_FINAL.csv` is expected to bridge the entire +0.21 Macro F1 gap, propelling the submission directly across the intermediate cluster into the Top 30.

---

## 3. Platform Submission Mechanics & Policies

1. **Submission Evaluation Limit:** The competition permits a restricted number of submissions per day (typically 3 submissions).
2. **Scoring Scheme:** Public leaderboard scores are computed on a fixed subset of the test set (e.g. 30–50%), with the final ranking determined by the private test set.
3. **Overfitting Risk:** Attempting to over-tune to minute public leaderboard fluctuations risks catastrophic private shakeup. Our primary anchor remains **Detector-Channel 5-Fold Cross Validation** ($\sigma = 0.0075$).

---

## 4. Competitive Intelligence Checklist

| Item | Local Workspace Status | User Action Required |
|:---|:---:|:---|
| **Current Rank (60)** | Verified from Prompt | Confirmed |
| **Current Score (0.4214)** | Verified from Phase 4/5 logs | Confirmed |
| **Exact Rank 30 Score** | Estimated ~0.60 – 0.62 | If portal table is visible, provide exact score of Rank 30 |
| **Remaining Uploads** | 1–2 remaining | Use only for approved champion or validated breakthrough |

---

## 5. Strategic Directive

Do not chase speculative, unvalidated micro-adjustments that compromise the structural stability of the approved 0.6336 champion. The primary competitive objective is ensuring that the approved `submission_FINAL.csv` is uploaded to replace the 0.4214 Phase 4 baseline.
