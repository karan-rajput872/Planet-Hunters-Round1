# 🏁 Planet Hunters — Final Competition Handover
## ML Challenge Hack4Hack 2026 | Round 1

**Handover Status:** COMPLETED & AUDITED
**Handover Date:** October 2026
**Final Submission Candidate:** `submissions/submission_FINAL.csv`

---

## 1. Final Submission Deliverable Summary

| Parameter | Specification | Verification Status |
|:---|:---|:---:|
| **Recommended File** | `submissions/submission_FINAL.csv` | **VERIFIED** |
| **Relative Path** | `submissions/submission_FINAL.csv` (from repository root) | **VERIFIED** |
| **Alternative Candidate** | `submissions/submission_v2.csv` (Pure 5-Fold LightGBM) | **VERIFIED** |
| **Total Test Rows** | Exactly **7,000** data rows (+ 1 header row) | **VERIFIED** |
| **Columns** | Exactly **2 columns**: `id,label` | **VERIFIED** |
| **Validation Exit Code** | **Code 0** (All 14 checks passed) | **VERIFIED** |
| **Reproducibility** | 100.0000% Bitwise match against champion `submission_v3.csv` | **VERIFIED** |

---

## 2. Immediate User Instructions: Competition Portal Upload

Follow these steps to submit the predictions to the competition platform:

### Step 1: Run Final Local Validation Check
Ensure the file has not been altered:
```powershell
.\.venv\Scripts\python.exe validate_submission.py submissions/submission_FINAL.csv
```
Confirm the terminal displays: `FINAL VALIDATION VERDICT: PASSED`.

### Step 2: Access Competition Portal
1. Open your web browser and navigate to the official **Hack4Hack 2026 Round 1** competition website.
2. Log in to your participant account.
3. Select the **Planet Hunters — Find New Worlds in Starlight** challenge.
4. Navigate to the **Submit Predictions** or **Submission** page.

### Step 3: Upload the CSV
1. Choose the file at:
   ```
   submissions/submission_FINAL.csv
   ```
2. Click **Submit** or **Upload**.

### Step 4: Verify Portal Acceptance
1. Confirm that the platform acknowledges receipt with status: `Accepted` or `Scoring`.
2. Ensure the portal processes all **7,000 rows** without formatting errors.
3. If the platform allows 2 submissions:
   - Upload `submissions/submission_FINAL.csv` as your **Primary Submission**.
   - Optionally upload `submissions/submission_v2.csv` as your **Secondary Submission** to benchmark the Dual-Architecture ensemble against a pure 5-fold LightGBM model on the public 30% leaderboard.

---

## 3. Post-Submission Record Keeping (Fill In After Portal Upload)

Please record your official competition feedback below for future reference and portfolio documentation:

| Information Field | Participant Record Entry |
|:---|:---|
| **Portal Submission Timestamp** | `[Enter Date & Time here, e.g. 2026-10-22 14:30 IST]` |
| **Uploaded Filename** | `submission_FINAL.csv` |
| **Platform Submission ID** | `[Enter Platform Submission ID if provided]` |
| **Portal Acceptance Status** | `[e.g. Successfully Evaluated / Accepted]` |
| **Public Leaderboard Macro F1** | `[Enter your Public LB Macro F1 score here]` |
| **Public Leaderboard Rank** | `[Enter your Leaderboard Rank, e.g. #3 / Top 5%]` |
| **Total Participants on Leaderboard**| `[Enter total active participants]` |
| **Variance vs. OOF Score (0.5915)** | `[Public LB Score - 0.5915]` |
| **Final Competition Standing / Prize**| `[Record after Round 1 evaluation concludes]` |

---

## 4. Key Project Artifacts Summary

- **Source Code:** Modular pipeline in `src/` (`data_loader.py`, `feature_engineering.py`, `model_training.py`, `cross_validation.py`, `submission_validation.py`, `train_v3_dual_ensemble.py`).
- **Trained Model Binaries:** 10 fold models stored in `models/tuned_cv_models/` (5 LightGBM + 5 HistGB).
- **Processed Features:** Columnar parquets in `data/processed/train_features.parquet` (18,000 × 85) and `test_features.parquet` (7,000 × 85).
- **Visual Assets:** 7 diagnostic plots in `assets/architecture/` and `assets/plots/`.
- **Documentation:** Full technical suite in `docs/` and project `README.md`.
- **Portfolio Package:** Compressed standalone archive in `dist/Planet-Hunters-Round1-Portfolio-Ready.zip`.
