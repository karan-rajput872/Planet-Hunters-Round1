# 🚀 PHASE 7 FINAL OPTIMIZATION & GENERALIZATION AUDIT REPORT
## Planet Hunters — Find New Worlds in Starlight (Hack4Hack 2026 — Round 1)

**Date & Time:** 2026-10-23, 09:25 AM IST  
**Competition Deadline:** 23 October 2026, 10:00 AM IST  
**Lead Roles:** Senior Kaggle-level ML Competition Researcher, Computational Astrophysicist & Independent Validation Auditor  
**Final Submission Decision:** **RETAIN PHASE 5 APPROVED FINAL (`submissions/submission_FINAL.csv`)**  
**Approved Final Checksum (SHA-256):** `6a378eae06765a28a39d41a322f47ff25512a43a47827ff4576940282b74330e`  

---

## 1. Executive Summary & Baseline Ledger

Phase 7 conducted the final emergency generalization sprint to assess whether any defensible, statistically reliable improvement could be achieved over the approved Phase 5/6 baseline before the 10:00 AM IST deadline.

### Verified Baseline Ledger

| Artifact Role | File Path | Verified SHA-256 Checksum | 14-Check Validator | Status |
|:---|:---|:---|:---:|:---:|
| **Current Approved Final** | `submissions/submission_FINAL.csv` | `6a378eae06765a28a39d41a322f47ff25512a43a47827ff4576940282b74330e` | 14/14 PASS | **APPROVED FINAL (100% Intact)** |
| **Phase 5 Approved Best** | `submissions/submission_PHASE5_best.csv` | `6a378eae06765a28a39d41a322f47ff25512a43a47827ff4576940282b74330e` | 14/14 PASS | **IDENTICAL SOURCE** |
| **Phase 4 Baseline Backup** | `submissions/submission_FINAL_PHASE4_BACKUP.csv` | `f53a08c47155bc907f855b0626cb38134aae298a58903b18f3d56818f0c053c1` | 14/14 PASS | **PRESERVED BACKUP (Pub LB: 0.4214)** |
| **Phase 6 Candidate 01** | `submissions/submission_PHASE6_candidate_01.csv` | `243b382359960efcc2fb44a75dfaa993f906b0052b4d7479813c6f1bf9d7ac8b` | 14/14 PASS | **EXPERIMENTAL CANDIDATE** |
| **Phase 7 Candidate 01** | `submissions/submission_PHASE7_candidate_01.csv` | `243b382359960efcc2fb44a75dfaa993f906b0052b4d7479813c6f1bf9d7ac8b` | 14/14 PASS | **EXPERIMENTAL CANDIDATE** |

---

## 2. High-Priority Investigation A: Error Analysis & Misclassifications

Evaluating 18,000 out-of-fold validation stars revealed that total classification errors equal 6,580 (36.56% error rate, 63.44% accuracy).

### Class-Wise Macro F1 Loss Contribution Ranking
Each of the 8 classes carries an equal $0.125$ weight in Macro F1:

| Target Class | Support | F1 Score | Precision | Recall | Macro F1 Loss ($0.125 \times (1 - \text{F1})$) | Primary Error Mechanism |
|:---|---:|:---:|:---:|:---:|:---:|:---|
| **`planet`** | 2,145 | 0.4591 | 0.5361 | 0.4014 | **0.0676** | Shallow transits ($R_p \le 1.5 R_\oplus$) below photon shot noise |
| **`starspots`** | 2,882 | 0.5330 | 0.5316 | 0.5344 | **0.0584** | Low-amplitude rotational waves blending with noise |
| **`background_binary`** | 1,604 | 0.5797 | 0.6980 | 0.4956 | **0.0525** | Diluted off-target eclipses mimicking primary transit depth |
| **`quiet_star`** | 3,624 | 0.6197 | 0.4934 | 0.8331 | **0.0475** | Conservative attractor state for all subtle signals |
| **`flare_star`** | 1,804 | 0.6660 | 0.7980 | 0.5715 | **0.0417** | Faint impulsive spikes confused with instrumental glitches |
| **`pulsating_star`** | 1,973 | 0.7402 | 0.8313 | 0.6670 | **0.0325** | Low-harmonic Fourier modes confused with stellar activity |
| **`eclipsing_binary`** | 2,247 | 0.7468 | 0.8487 | 0.6667 | **0.0317** | Shallow secondary eclipses mistaken for background binaries |
| **`instrument_glitch`** | 1,721 | 0.8193 | 0.8505 | 0.7902 | **0.0226** | Momentum dumps well-isolated by bitmask features |

### Top 10 Pairwise Misclassifications

1. `starspots` $\rightarrow$ `quiet_star`: **956 errors**
2. `planet` $\rightarrow$ `quiet_star`: **699 errors**
3. `pulsating_star` $\rightarrow$ `quiet_star`: **468 errors**
4. `flare_star` $\rightarrow$ `quiet_star`: **401 errors**
5. `planet` $\rightarrow$ `starspots`: **368 errors**
6. `flare_star` $\rightarrow$ `starspots`: **275 errors**
7. `background_binary` $\rightarrow$ `quiet_star`: **240 errors**
8. `quiet_star` $\rightarrow$ `starspots`: **238 errors**
9. `eclipsing_binary` $\rightarrow$ `background_binary`: **216 errors**
10. `background_binary` $\rightarrow$ `eclipsing_binary`: **206 errors**

*Astro-Physical Insight:* The predominant error across the entire model pipeline is asymmetric leakage into `quiet_star` (2,764 total stars). When signals have low signal-to-noise ratio, the gradient-boosted trees default to the dominant quiescent prior.

---

## 3. High-Priority Investigation B: Ensemble Diversity & Model Complementarity

Using saved out-of-fold probability matrices from LightGBM, HistGradientBoosting, and CatBoost:

### Pairwise Model Disagreement & Error Correlation

| Model Pair | Prediction Disagreement (% of stars) | Error Correlation ($r$) | Complementary Behavior |
|:---|:---:|:---:|:---|
| **LightGBM vs HistGB** | **11.37%** (2,047 stars) | 0.8419 | HistGB rescues 658 stars; LGB rescues 670 stars |
| **LightGBM vs CatBoost** | **15.33%** (2,759 stars) | 0.7806 | Distinct tree growth: leaf-wise vs symmetric oblivious |
| **HistGB vs CatBoost** | **15.88%** (2,858 stars) | 0.7750 | Histogram depth-wise vs symmetric oblivious trees |

All three models failed simultaneously on only 5,541 stars out of 18,000, demonstrating that ensembling provides genuine structural variance reduction.

### Targeted Blend Benchmarking across Folds

| Blend Formulation | LGB % | HGB % | CB % | Stratified OOF | Detector OOF | Detector Fold Mean ($\mu$) | Detector Fold Std ($\sigma$) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Phase 5 Approved (Champion)** | **50%** | **40%** | **10%** | **0.6455** | **0.6336** | **0.6338** | **±0.0137** |
| **Candidate (45/45/10)** | 45% | 45% | 10% | 0.6461 | 0.6338 | 0.6340 | ±0.0139 |
| **Candidate (50/45/5)** | 50% | 45% | 5% | 0.6456 | 0.6335 | 0.6337 | ±0.0135 |
| **Candidate (40/50/10)** | 40% | 50% | 10% | 0.6457 | 0.6336 | 0.6337 | ±0.0142 |
| **Candidate (48/44/8)** | 48% | 44% | 8% | 0.6454 | 0.6336 | 0.6338 | ±0.0139 |
| **Candidate (42/48/10)** | 42% | 48% | 10% | 0.6460 | 0.6332 | 0.6333 | ±0.0143 |

---

## 4. High-Priority Investigation C: Feature Robustness

- **Feature Matrix Verification:** 88 features in `train_features_v5.parquet` and `test_features_v5.parquet`.
- **Integrity:** Zero NaN values, zero infinite values, exact column alignment.
- **Detector Shift Audit:** Evaluated the ratio of across-detector mean variation to total feature variance ($\sigma_{\text{det}} / \sigma_{\text{total}}$). Key cotrended metrics (`flux_std`: 0.0387, `flux_mad`: 0.0355, `flux_min`: 0.0354) showed negligible across-detector drift ($< 4\%$), verifying that common-trend subtraction successfully decoupled astrophysical signals from instrumental jitter.

---

## 5. Candidate Generation & Validation Gate Result

Phase 7 acceptance criterion was defined as:
> *"Detector-channel OOF improvement of at least approximately 0.003 over the approved 0.6336–0.6338 range."*

- **Peak Detector-Channel OOF Score:** `0.6338` (Candidate 45/45/10)
- **Phase 5 Baseline:** `0.6336`
- **Measured Gain:** `+0.0002`
- **Gate Requirement:** `+0.0030`
- **Passes Gate:** **NO (REJECTED)**

Only 30 out of 7,000 test predictions (0.43%) differ between Phase 5 and Phase 7. Replacing the approved candidate for 30 boundary cases offers no statistical advantage.

---

## 6. Final Decision & Recommendation

### **VERDICT: RETAIN PHASE 5 APPROVED FINAL (`submissions/submission_FINAL.csv`)**

1. **Approved Final:** `submissions/submission_FINAL.csv` (SHA-256: `6a378eae...`) is 100% verified, passed all 14 schema and astrophysical validator checks, and represents our most thoroughly vetted model.
2. **Action Required:** Manually upload `submissions/submission_FINAL.csv` to the official Hack4Hack portal before 10:00 AM IST.
