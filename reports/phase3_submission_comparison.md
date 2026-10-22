# Phase 3: Final Submission Candidates Comparison Report

## 1. Executive Summary
- **Evaluation Metric**: Macro F1-Score across 8 astrophysical classes
- **Candidates Generated & Preserved**:
  1. `submissions/submission.csv` (Holdout LightGBM: Macro F1 = 0.5914)
  2. `submissions/submission_v2.csv` (5-Fold LightGBM Ensemble: OOF Macro F1 = 0.5890)
  3. `submissions/submission_v3.csv` (5-Fold Dual LightGBM + HistGB Ensemble: OOF Macro F1 = **0.5912**, Holdout Blend = **0.5956**)

---

## 2. Model Lineage & Architecture Comparison

| Candidate File | Modeling Architecture | CV / Holdout Validation | Cross-Sector Generalization Strengths |
|---|---|---|---|
| `submission.csv` | Single Best LightGBM (31 leaves, 400 trees) | Holdout Macro F1: **0.5914** | Baseline champion, highly optimized single tree |
| `submission_v2.csv` | 5-Fold Bagged LightGBM (63 leaves, 600 trees) | Mean Fold F1: **0.5889 +/- 0.0017** | 5-fold variance reduction across data splits |
| **`submission_v3.csv` (RECOMMENDED)** | **5-Fold Dual-Architecture (0.75 LightGBM + 0.25 HistGB)** | **Holdout: 0.5956 \| OOF: 0.5912** | **Best of both worlds: dual tree architecture diversity + 5-fold bagging** |

---

## 3. Class Distribution Across Candidates

| Astrophysical Class | `submission.csv` (Single) | `submission_v2.csv` (5-Fold LGB) | `submission_v3.csv` (Dual 5-Fold) |
|---|---|---|---|
| `planet` | 512 (7.3%) | 529 (7.6%) | **516 (7.4%)** |
| `eclipsing_binary` | 677 (9.7%) | 688 (9.8%) | **687 (9.8%)** |
| `background_binary` | 373 (5.3%) | 286 (4.1%) | **297 (4.2%)** |
| `starspots` | 769 (11.0%) | 864 (12.3%) | **827 (11.8%)** |
| `pulsating_star` | 2044 (29.2%) | 1854 (26.5%) | **1904 (27.2%)** |
| `flare_star` | 543 (7.8%) | 449 (6.4%) | **471 (6.7%)** |
| `instrument_glitch` | 1280 (18.3%) | 1374 (19.6%) | **1372 (19.6%)** |
| `quiet_star` | 802 (11.5%) | 956 (13.7%) | **926 (13.2%)** |
| **Total Predictions** | **7,000** | **7,000** | **7,000** |

---

## 4. Submission Integrity Verification
Every single candidate passed 100% of the competition checks:
- Exactly 7,000 rows matching `test_stars.csv` IDs in identical order.
- Exactly two columns: `id,label`.
- 0 null, NaN, or invalid values.
- Exactly 8 permitted class strings.

---

## 5. Recommended Submission Strategy for Participant
1. **Primary Upload Recommendation**: `submissions/submission_v3.csv` (or final verified `submissions/submission_FINAL.csv`).
   - Combines structural tree diversity (leaf-wise LightGBM + depth-wise HistGradientBoosting) with 5-fold cross-validation averaging.
   - Reaches **0.5956** validation Macro F1, the highest recorded score across all experiments.
2. **Alternative / Comparison Candidate**: `submissions/submission_v2.csv`.
   - If multiple submissions are available, compare against v2 to evaluate pure LightGBM vs. Dual-Architecture ensembling on the public 30% leaderboard.
