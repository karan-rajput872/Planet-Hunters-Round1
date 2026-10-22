# Submission Verification and Validation Report

## 1. Submission Overview
- **File Path**: `submissions/submission.csv`
- **Generated At**: 2026-10-22
- **Model Used**: Best validated `LightGBM` (Macro F1: 0.5914)
- **Validation Status**: **PASSED 100% OF CHECKS**

---

## 2. Integrity Checklist

| Check Item | Requirement | Actual Status | Result |
|---|---|---|---|
| **File Exists** | `submissions/submission.csv` exists and readable | Found on disk | **PASS** |
| **Exact Columns** | Exactly two columns: `id,label` | `['id', 'label']` | **PASS** |
| **Row Count** | Exactly 7,000 predictions (excluding header) | Exactly 7,000 rows | **PASS** |
| **Test ID Alignment** | 100% matches `test_stars.csv` IDs in exact order | Perfect match | **PASS** |
| **Unique IDs** | Exactly 7,000 unique star IDs (0 duplicates) | 7,000 unique IDs | **PASS** |
| **Missing Values** | No NaN, null, or empty string values | 0 missing values | **PASS** |
| **Allowed Labels** | Labels strictly from the 8 allowed classes | 8 valid classes only | **PASS** |
| **No Extra Index** | CSV index column omitted (`index=False`) | Verified | **PASS** |

---

## 3. Predicted Test Class Distribution

| Label | Predicted Count | Predicted Percentage |
|---|---|---|
| `pulsating_star` | 2,044 | 29.2% |
| `instrument_glitch` | 1,280 | 18.3% |
| `quiet_star` | 802 | 11.5% |
| `starspots` | 769 | 11.0% |
| `eclipsing_binary` | 677 | 9.7% |
| `flare_star` | 543 | 7.8% |
| `planet` | 512 | 7.3% |
| `background_binary` | 373 | 5.3% |
| **Total** | **7,000** | **100.0%** |

---

## 4. Leaderboard Upload Instructions
1. Navigate to the Hack4Hack 2026 team portal: **Leaderboard** tab.
2. Click **Submit Predictions**.
3. Select and upload file: `submissions/submission.csv`.
4. The system will automatically compute the public score on the 30% holdout split.
