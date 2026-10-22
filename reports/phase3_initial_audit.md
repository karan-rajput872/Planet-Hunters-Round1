# Phase 3 Initial Project Audit

## 1. Audit Overview
- **Audit Date**: 2026-10-22
- **Objective**: Complete systematic verification of existing files, models, feature matrices, submission files, and reproducibility before executing Phase 3 experiments.

## 2. Verification Checklist

| Item | Requirement | Actual Status | Result |
|---|---|---|---|
| **A. Core Files** | Raw datasets, CSVs, features, models exist | All 15 required files present | **PASS** |
| **B. Model Loading** | `best_lightgbm.joblib` and `ensemble_bundle.joblib` load | Successfully loaded with joblib | **PASS** |
| **C. Submission Candidates** | `submission.csv` and `submission_v2.csv` valid | Both pass 100% of validation checks | **PASS** |
| **D. Feature Matrix Dimensions** | Train (18,000, 85), Test (7,000, 85) | Exactly (18000, 85) and (7000, 85) | **PASS** |
| **E. Feature Column Alignment** | Feature names and sequence identical | Exact match across all 85 columns | **PASS** |
| **F. Model Configuration** | LightGBM hyperparameters verified | Balanced class weighting, tree subsampling | **PASS** |
| **G. 5-Fold Artifacts** | `tuned_cv_models/` contains 5 fold models | 5 out of 5 fold models present | **PASS** |
| **H. Feature Cleanliness** | Zero NaN, infinite or corrupted values | 0 train nulls, 0 test nulls | **PASS** |

## 3. Submission Candidates Summary
- **Candidate 1 (`submission.csv`)**: Generated from single-split best LightGBM (Holdout Macro F1: 0.5914).
- **Candidate 2 (`submission_v2.csv`)**: Generated from tuned 5-fold probability-averaged ensemble (OOF Macro F1: 0.5890, Mean Fold F1: 0.5889 +/- 0.0017).
- Both submissions are preserved on disk and ready for leaderboard evaluation.
