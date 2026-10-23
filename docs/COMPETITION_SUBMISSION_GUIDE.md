# 🏆 Planet Hunters — Competition Submission Guide
## ML Challenge Hack4Hack 2026 | Round 1

**Primary Objective:** Deliver an error-free, strictly formatted, and top-performing competition submission.  
**Official Recommended Candidate:** `submissions/submission_FINAL.csv` (promoted Phase 5 Tri-Ensemble, identical to `submissions/submission_PHASE5_best.csv`)  
**Evaluation Metric:** **Macro F1-Score** across 8 astrophysical & instrumental classes.  
**Original Phase 4 Backup:** `submissions/submission_FINAL_PHASE4_BACKUP.csv` (SHA-256: `f53a08c47155bc907f855b0626cb38134aae298a58903b18f3d56818f0c053c1`)

---

## 1. Selected Final Submission Candidate

| Property | Value / Specification |
|:---|:---|
| **Submission File** | `submissions/submission_FINAL.csv` |
| **Relative Path** | `submissions/submission_FINAL.csv` (relative to repository root) |
| **Model Architecture** | **5-Fold Tri-Architecture Ensemble** (50% LightGBM + 40% HistGradientBoosting + 10% CatBoost) |
| **Feature Pipeline** | **88 Features** (with Camera/CCD Common-Trend Cotrending & Astrometric Vetting) |
| **Total Test Samples** | Exactly **7,000** data rows (+ 1 header row) |
| **Columns** | Exactly **2 columns**: `id,label` |
| **Bitwise Parity** | 100.0000% identical to validated Phase 5 candidate `submissions/submission_PHASE5_best.csv` |
| **SHA-256 Checksum** | `6a378eae06765a28a39d41a322f47ff25512a43a47827ff4576940282b74330e` |
| **Validation Status** | **14 / 14 Automated Checks PASSED** |

### Why This Candidate Was Selected
1. **Physical Systematic Correction (Astro-Cotrending):** Eliminates camera/CCD thermal breathing and spacecraft pointing jitter, dropping Kolmogorov-Smirnov feature drift by **60.3%** (mean KS: 0.1326 $\rightarrow$ 0.0526).
2. **Superior Out-of-Detector Generalization:** Evaluated under Stratified Detector-Channel 5-Fold cross-validation (holding out entire physical detectors), scoring **0.6336 Macro F1** compared to 0.5161 for the un-cotrended baseline (**+0.1175 gain**).
3. **Tri-Model Diversity:** Combines leaf-wise LightGBM (45 leaves), regularized depth-wise HistGradientBoosting, and CatBoost oblivious trees.
4. **Internal Cross-Validation Score:** Reaches **0.6455 OOF Macro F1** across all 18,000 training stars (+0.0540 over Phase 4).

---

## 2. Predicted Class Distribution in `submission_FINAL.csv`

The 7,000 test predictions represent a realistic, astrophysically plausible distribution across the eight target classes, resolving the baseline pulsator/glitch over-prediction:

| Class Name | Predicted Count | Percentage | Training Prior | Astrophysical / Signal Characterization |
|:---|:---:|:---:|:---:|:---|
| `quiet_star` | **1,912** | **27.3%** | 20.1% | Flat lightcurve, Gaussian shot noise |
| `starspots` | **1,122** | **16.0%** | 16.0% | Smooth, rotational quasi-periodic modulation |
| `planet` | **793** | **11.3%** | 11.9% | Shallow, U-shaped transits without centroid shift |
| `pulsating_star` | **785** | **11.2%** | 11.0% | Coherent sinusoidal Fourier harmonics |
| `instrument_glitch` | **777** | **11.1%** | 9.6% | Sharp steps, cosmic ray hits, thruster dumps |
| `eclipsing_binary` | **685** | **9.8%** | 12.5% | Deep geometric V-shaped eclipses (primary/secondary) |
| `flare_star` | **505** | **7.2%** | 10.0% | Fast rise, exponential cooling decay asymmetry |
| `background_binary` | **421** | **6.0%** | 8.9% | Transit dip accompanied by centroid displacement |
| **Total** | **7,000** | **100.0%** | **100.0%** | **All 8 classes balanced and represented** |

---

## 3. How to Validate the Submission Before Upload

A standalone validation script is provided in the repository root:

```powershell
# From project root:
.\.venv\Scripts\python.exe validate_submission.py submissions/submission_FINAL.csv
```

### The 14 Verification Checks Executed:
1. `exists`: File exists on filesystem.
2. `row_count`: Exactly 7,000 rows.
3. `column_count`: Exactly 2 columns (`id,label`).
4. `id_column`: Test star IDs start with `TIC` prefix.
5. `id_match`: Matches test IDs from `test_stars.csv` exactly.
6. `id_order`: Exact row-for-row alignment with competition test order.
7. `no_duplicate_ids`: Exactly 7,000 unique IDs.
8. `no_null_ids`: Zero missing or NaN IDs.
9. `no_null_labels`: Zero missing or NaN labels.
10. `valid_label_set`: Only permitted eight labels.
11. `all_classes_present`: Every class predicted at least once.
12. `no_single_class_dominance`: Max class percentage $< 50\%$.
13. `planet_count_plausible`: Predicted planets between 100 and 1,500.
14. `quiet_star_count_plausible`: Predicted quiet stars $\ge 500$.

---

## 4. SHA-256 Checksum Verification Command

Verify file integrity in PowerShell before uploading:

```powershell
Get-FileHash submissions\submission_FINAL.csv -Algorithm SHA256
```

Expected Output:
```
Algorithm       Hash                                                               Path
---------       ----                                                               ----
SHA256          6A378EAE06765A28A39D41A322F47FF25512A43A47827FF4576940282B74330E  ...submission_FINAL.csv
```

---

## 5. Portal Upload Instructions

1. Navigate to the Hack4Hack 2026 competition portal.
2. Open the **Leaderboard** tab.
3. Select and upload `submissions/submission_FINAL.csv`.
4. The portal checks file format instantly and updates scores every 15 minutes.
5. Note: Internal validation metric is **0.6455 OOF / 0.6336 Detector CV**; public score will update on the leaderboard upon upload.
