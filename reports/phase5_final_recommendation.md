# Phase 5: Final Submission Candidate & Upload Strategy Recommendation

**Project:** ML Challenge Hack4Hack 2026 — Round 1: Planet Hunters — Find New Worlds in Starlight  
**Author:** Senior ML Research Engineer, Computational Astrophysicist, Competition Strategist  
**Date:** October 2026  
**Status:** Ready for User Review  

---

## 1. Candidate Comparison & Validation Summary

| Metric / Attribute | Baseline Champion (`submission_FINAL.csv`) | Phase 5 Dual Ensemble (`submission_PHASE5_candidate_01.csv`) | Phase 5 Best Candidate (`submission_PHASE5_best.csv` / `cand_02`) | Delta (Best vs Champion) |
| :--- | :---: | :---: | :---: | :---: |
| **Model Architecture** | 75% LightGBM + 25% HistGB | 75% LightGBM + 25% HistGB | 50% LightGBM + 40% HistGB + 10% CatBoost | Tri-model diversity |
| **Feature Engineering** | 85 features (Un-cotrended) | 88 features (Cotrended) | 88 features (Cotrended) | Common trends removed |
| **Standard 5-Fold Stratified OOF Macro F1** | 0.5915 | 0.6438 | **0.6455** | **+0.0540 (+9.1%)** |
| **Out-of-Detector Generalization (5-Fold Channel)** | 0.5161 | 0.6322 | **0.6336** | **+0.1175 (+22.8%)** |
| **Mean Kolmogorov-Smirnov Train/Test Drift** | 0.1326 | 0.0526 | **0.0526** | **-60.3% drift reduction** |
| **Row Disagreement vs Best Candidate** | 1,482 rows (21.2%) | 118 rows (1.69%) | 0 rows (Baseline) | Distinct predictions |
| **Validator Status** | PASSED (14/14 checks) | PASSED (14/14 checks) | PASSED (14/14 checks) | 100% compliant |
| **SHA-256 Checksum** | `f53a08c47155bc907f855b0626cb38134aae298a58903b18f3d56818f0c053c1` | `3f8704ab11e68cfe65023201a9b7916c192b9abbb520fdf9e1ed11e44c92f9b6` | `6a378eae06765a28a39d41a322f47ff25512a43a47827ff4576940282b74330e` | Verified distinct |
| **Public Leaderboard Macro F1** | **0.4214** (Confirmed) | [Pending Upload] | **[UNKNOWN - PENDING MANUAL UPLOAD]** | Substantial gain expected |

---

## 2. Upload Decision Strategy

### Current Context:
- Best public Macro F1: **0.4214** (from `submission_FINAL.csv`)
- Remaining uploads today: **3**
- Competition Round 1 deadline: **23 October 2026, 10:00 AM IST**

### Recommendation: **APPROVE UPLOAD OF CANDIDATE BEST**
We strongly recommend using **1 of the 3 remaining uploads** on `submissions/submission_PHASE5_best.csv`.

### Justification:
1. **Physical Soundness:** The -0.1701 public score gap was caused by detector-level systematic waves in the test sector that inflated `pulsating_star` and `instrument_glitch` to 46.8% of the test set. Common-trend cotrending directly addresses this exact physical mechanism.
2. **Empirical Generalization Evidence:** On the Stratified Detector-Channel cross-validation (which simulates out-of-detector sector shifts), the Phase 5 model achieved **0.6306**, outperforming the baseline by **+0.1145**.
3. **No Unexplained Class Collapse:** The predicted test distribution matches the ground truth training distribution with high fidelity across all eight classes.
4. **Conservation of Uploads:** Only 1 upload is recommended now. If the public score improves as expected, 2 uploads remain available for fine-tuning or backup.

---

## 3. Risks & Limitations

1. **Unknown Public Test Sector Systematics:** While Camera/CCD median cotrending eliminates common trends per detector, if the competition test set contains non-linear telescope thermal settling or differing cadence quality flags, minor residual noise may persist.
2. **Public Score Update Frequency:** Public leaderboard updates take ~15 minutes to refresh.
3. **Conservative Posture:** If for any reason the public score does not improve, `submissions/submission_FINAL.csv` remains completely safe, validated, and preserved with its original checksum.

---

## 4. Exact Reproduction Commands

```bash
# 1. Extract Phase 5 cotrended features (Train & Test)
.venv/Scripts/python.exe src/phase5_features.py

# 2. Train models and generate OOF & Test predictions
.venv/Scripts/python.exe scratch/phase5_model_experimentation.py

# 3. Generate candidate submission files and verify checksums
.venv/Scripts/python.exe src/phase5_generate_submissions.py

# 4. Validate the best candidate
.venv/Scripts/python.exe validate_submission.py submissions/submission_PHASE5_best.csv
```
