# 🏆 Planet Hunters — Competition Submission Guide
## ML Challenge Hack4Hack 2026 | Round 1

**Primary Objective:** Deliver an error-free, strictly formatted, and top-performing competition submission.
**Recommended Candidate File:** `submissions/submission_FINAL.csv` (identical to `submissions/submission_v3.csv`)
**Evaluation Metric:** **Macro F1-Score** across 8 astrophysical & instrumental classes.

---

## 1. Selected Final Submission Candidate

| Property | Value / Specification |
|:---|:---|
| **Submission File** | `submissions/submission_FINAL.csv` |
| **Relative Path** | `submissions/submission_FINAL.csv` (relative to repository root) |
| **Model Architecture** | **5-Fold Dual-Architecture Ensemble** (75% LightGBM + 25% HistGradientBoosting) |
| **Total Test Samples** | Exactly **7,000** data rows (+ 1 header row) |
| **Columns** | Exactly **2 columns**: `id,label` |
| **Bitwise Parity** | 100.0000% identical to validated champion `submission_v3.csv` |
| **Validation Status** | **14 / 14 Automated Checks PASSED** |

### Why This Candidate Was Selected
1. **Architectural Diversity:** Combines leaf-wise tree growth (LightGBM with 63 leaves) that captures sharp transit dips with depth-wise tree growth (HistGradientBoosting with 450 trees) that regularizes decision boundaries.
2. **Empirical Superiority:** Outperforms all alternative candidates across 5-fold cross-validation:
   - **Overall OOF Macro F1:** **0.5915** across all 18,000 training stars.
   - **Mean Fold Score:** **0.5914 ± 0.0020**.
   - **Stratified Holdout Blend:** **0.5945 – 0.5956**.
3. **Cross-Sector Resilience:** Evaluated with scale-free percentile spreads and detrended signal-to-noise ratios, preventing over-reliance on training-sector noise characteristics.

---

## 2. Predicted Class Distribution in `submission_FINAL.csv`

The 7,000 test predictions represent a realistic, astrophysically plausible distribution across the eight target classes:

| Class Name | Predicted Count | Percentage | Astrophysical / Signal Characterization |
|:---|:---:|:---:|:---|
| `pulsating_star` | **1,904** | **27.2%** | High-frequency sinusoidal harmonics |
| `instrument_glitch` | **1,372** | **19.6%** | Single-cadence cosmic rays, thruster dumps |
| `quiet_star` | **926** | **13.2%** | Flat lightcurve, Gaussian shot noise |
| `starspots` | **827** | **11.8%** | Smooth, rotational quasi-periodic modulation |
| `eclipsing_binary` | **687** | **9.8%** | Deep, periodic geometric dips (primary/secondary) |
| `planet` | **516** | **7.4%** | Shallow, U-shaped transits without centroid shift |
| `flare_star` | **471** | **6.7%** | Fast rise, exponential decay asymmetry |
| `background_binary` | **297** | **4.2%** | Transit dip accompanied by centroid displacement |
| **Total** | **7,000** | **100.0%** | **All 8 classes represented** |

---

## 3. How to Validate the Submission Before Upload

A standalone validation script is provided in the repository root:

```powershell
# From project root:
.\.venv\Scripts\python.exe validate_submission.py submissions/submission_FINAL.csv
```

### The 14 Verification Checks Executed:
1. `exists`: File exists on filesystem.
2. `readable`: File can be parsed as a standard CSV.
3. `exact_7000_rows`: Contains exactly 7,000 rows.
4. `exact_two_columns`: Exactly 2 columns present.
5. `exact_column_names`: Header is exactly `id,label`.
6. `no_index_column`: No unnamed pandas index column.
7. `no_null_ids`: 0 missing or NaN values in `id`.
8. `no_duplicate_ids`: 0 duplicate test star IDs.
9. `id_match_test_stars`: ID set matches `test_stars.csv` exactly.
10. `id_order_correct`: Row order matches `test_stars.csv` row-for-row.
11. `no_null_labels`: 0 missing or NaN values in `label`.
12. `no_whitespace_labels`: 0 blank or whitespace-only label strings.
13. `all_classes_valid`: 100% of labels belong to the permitted 8 classes.
14. `read_back_success`: File can be read back cleanly with identical shape.

---

## 4. How to Regenerate the Submission

If you ever need to reproduce `submission_FINAL.csv` from the trained models and cached features:

```powershell
.\.venv\Scripts\python.exe generate_submission.py --model champion --output submissions/submission_FINAL.csv
```

Execution runtime: **~6 seconds on CPU**.

---

## 5. Portal Upload Step-by-Step Instructions

1. **Log in** to the official Hack4Hack 2026 competition platform.
2. Navigate to **ML Challenge Hack4Hack 2026 — Round 1: Planet Hunters**.
3. Go to the **Submissions** or **Submit Predictions** page.
4. Select or drag-and-drop the file:
   ```
   submissions/submission_FINAL.csv
   ```
5. Confirm that the platform displays:
   - Rows processed: `7000`
   - File format: `CSV`
   - Status: `Evaluation in progress` / `Accepted`
6. If the portal supports a secondary submission:
   - Consider uploading `submissions/submission_v2.csv` (the pure 5-fold LightGBM candidate) to evaluate single vs. dual architecture performance on the public leaderboard.

---

## 6. Information to Record After Submission

Once uploaded, record the following competition metrics for portfolio and project evaluation:

| Field | Record Value Here |
|:---|:---|
| **Submission Date & Time** | `[e.g., 2026-10-22 14:00 UTC]` |
| **Uploaded Filename** | `submission_FINAL.csv` |
| **Portal Status** | `[e.g., Evaluated / Accepted]` |
| **Public Leaderboard Macro F1** | `[e.g., 0.XXXX]` |
| **Leaderboard Rank** | `[e.g., Top X% / Rank #Y]` |
| **Difference vs. OOF Benchmark** | `[Public LB - 0.5915]` |
