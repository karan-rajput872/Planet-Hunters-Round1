# 📊 PHASE 7 CANDIDATE COMPARISON & BENCHMARK AUDIT
## Planet Hunters — ML Challenge Hack4Hack 2026 (Round 1)

**Date:** 2026-10-23  
**Status:** **AUDITED — COMPARISON CONCLUDED**  

---

## 1. Candidate Comparison Matrix

| Metric / Dimension | Phase 4 Baseline | Phase 5 Approved Champion | Phase 6 Candidate 01 | Phase 7 Candidate 01 |
|:---|:---:|:---:|:---:|:---:|
| **Submission File** | `submission_FINAL_PHASE4_BACKUP.csv` | `submission_FINAL.csv` | `submission_PHASE6_candidate_01.csv` | `submission_PHASE7_candidate_01.csv` |
| **Verified SHA-256** | `f53a08c4...` | `6a378eae...` | `243b3823...` | `243b3823...` |
| **Ensemble Formula** | 75% LGB + 25% HGB | 50% LGB + 40% HGB + 10% CB | 45% LGB + 45% HGB + 10% CB | 45% LGB + 45% HGB + 10% CB |
| **Feature Count** | 85 (Raw/Local Detrend) | 88 (Camera/CCD Cotrended) | 88 (Camera/CCD Cotrended) | 88 (Camera/CCD Cotrended) |
| **Stratified 5-Fold OOF** | 0.5915 | 0.6455 | 0.6461 | 0.6461 |
| **Detector-Channel OOF** | 0.5161 | 0.6336 | 0.6338 | 0.6338 |
| **Detector Fold Std ($\sigma$)** | ±0.0162 | ±0.0137 | ±0.0139 | ±0.0139 |
| **Planet F1** | 0.4679 | 0.4591 | 0.4606 | 0.4606 |
| **Starspots F1** | 0.4912 | 0.5330 | 0.5339 | 0.5339 |
| **Background Binary F1** | 0.4850 | 0.5797 | 0.5824 | 0.5824 |
| **Flare Star F1** | 0.6410 | 0.6660 | 0.6652 | 0.6652 |
| **Pulsating Star F1** | 0.6820 | 0.7402 | 0.7396 | 0.7396 |
| **Instrument Glitch F1** | 0.7250 | 0.8193 | 0.8182 | 0.8182 |
| **Quiet Star F1** | 0.5120 | 0.6197 | 0.6194 | 0.6194 |
| **Changed Test Labels vs P5** | 2,741 / 7,000 (39.16%) | 0 (Baseline) | 30 / 7,000 (0.43%) | 30 / 7,000 (0.43%) |
| **14-Rule Validator** | PASS (14/14) | PASS (14/14) | PASS (14/14) | PASS (14/14) |
| **Public LB Score** | **0.4214** (Submitted) | **Pending Upload** | **Pending Upload** | **Pending Upload** |

---

## 2. Test Prediction Transition Analysis (Phase 5 Approved vs Phase 7 Candidate)

Of the 7,000 test stars, **6,970 predictions (99.57%) are bitwise identical**. Exactly 30 predictions shifted:

| Original Phase 5 Label | New Phase 7 Label | Shift Count | Astrophysical Context |
|:---|:---|:---:|:---|
| `quiet_star` | `planet` | 8 | Shallow transits on noisy boundaries promoted to planet |
| `starspots` | `quiet_star` | 6 | Low-amplitude rotational modulations demoted to quiet |
| `planet` | `quiet_star` | 5 | Ambiguous dips demoted to quiescent noise floor |
| `background_binary` | `planet` | 4 | Boundary transit SNR shift |
| `flare_star` | `quiet_star` | 3 | Faint single-cadence rise demoted |
| `quiet_star` | `starspots` | 2 | Very low frequency wander labeled starspot |
| `eclipsing_binary` | `background_binary` | 2 | Shallow secondary eclipse adjustment |
| **Total Changed** | — | **30** | **0.43% of test dataset** |

---

## 3. Candidate Conclusion

The candidate `submissions/submission_PHASE7_candidate_01.csv` is fully verified, clean, and reproducible. However, because the detector gain is $+0.0002$ (well below the $+0.003$ acceptance gate), **`submissions/submission_FINAL.csv` is retained as the official competition submission**.
