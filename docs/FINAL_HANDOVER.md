# 🏁 Planet Hunters — Final Competition Handover
## ML Challenge Hack4Hack 2026 | Round 1

**Handover Status:** COMPLETED, AUDITED & READY FOR MANUAL UPLOAD  
**Handover Date:** October 2026  
**Final Submission Candidate:** `submissions/submission_FINAL.csv` (Promoted Phase 5 Tri-Ensemble)  
**Original Phase 4 Backup:** `submissions/submission_FINAL_PHASE4_BACKUP.csv` (Bitwise Preserved)  

---

## 1. Final Submission Deliverable Summary

| Parameter | Specification | Verification Status |
|:---|:---|:---:|
| **Official Submission File** | `submissions/submission_FINAL.csv` | **VERIFIED PROMOTED** |
| **Relative Path** | `submissions/submission_FINAL.csv` (from repository root) | **VERIFIED** |
| **Verified SHA-256 Checksum**| `6a378eae06765a28a39d41a322f47ff25512a43a47827ff4576940282b74330e` | **MATCHED** |
| **Original Phase 4 Backup** | `submissions/submission_FINAL_PHASE4_BACKUP.csv` | **VERIFIED PRESERVED** |
| **Backup SHA-256 Checksum** | `f53a08c47155bc907f855b0626cb38134aae298a58903b18f3d56818f0c053c1` | **MATCHED** |
| **Model Architecture** | **Phase 5 Tri-Ensemble** (50% LightGBM + 40% HistGB + 10% CatBoost) | **VERIFIED** |
| **Feature Pipeline** | **88 Features** with Camera/CCD Cotrending & Astro Vetting | **VERIFIED** |
| **Total Test Rows** | Exactly **7,000** data rows (+ 1 header row) | **VERIFIED** |
| **Columns** | Exactly **2 columns**: `id,label` | **VERIFIED** |
| **Validation Status** | **Code 0** (All 14 checks passed on FINAL & candidates) | **VERIFIED** |
| **Unit Test Suite** | `tests/test_pipeline.py`: 12/12 tests passed | **VERIFIED** |
| **Phase 7 Candidate** | `submissions/submission_PHASE7_candidate_01.csv` (SHA-256: `243b3823...`) | **VERIFIED AUDITED** |
| **Phase 8 Candidate** | `submissions/submission_PHASE8_candidate_01.csv` (SHA-256: `7597c8e9...`) | **VERIFIED AUDITED (Experimental)** |
| **Final Recommendation** | **RETAIN APPROVED `submission_FINAL.csv`** (Upload immediately) | **APPROVED** |

---

## 2. Immediate User Instructions: Competition Portal Upload

Follow these steps to submit the predictions to the competition platform:

### Step 1: Run Final Local Validation Check
Ensure the file has not been altered:
```powershell
.\.venv\Scripts\python.exe validate_submission.py submissions/submission_FINAL.csv
```
Confirm the terminal displays: `FINAL VALIDATION VERDICT: PASSED`.

### Step 2: Verify SHA-256 Hash
```powershell
Get-FileHash submissions\submission_FINAL.csv -Algorithm SHA256
```
Confirm the hash matches:
`6A378EAE06765A28A39D41A322F47FF25512A43A47827FF4576940282B74330E`

### Step 3: Access Competition Portal & Upload
1. Open your web browser and navigate to the official **Hack4Hack 2026 Round 1** competition website.
2. Log in to your participant account and open the **Planet Hunters** challenge.
3. Navigate to the **Leaderboard** tab and select:
   ```
   submissions/submission_FINAL.csv
   ```
4. Click **Upload** (uses 1 of your 3 remaining uploads today).

---

## 3. Post-Submission Record Keeping (Fill In After Portal Upload)

Please record your official competition feedback below for future reference and portfolio documentation:

| Information Field | Participant Record Entry |
|:---|:---|
| **Portal Submission Timestamp** | `[Enter Date & Time here, e.g. 2026-10-22 23:55 IST]` |
| **Uploaded Filename** | `submission_FINAL.csv` |
| **Platform Submission ID** | `[Enter Platform Submission ID if provided]` |
| **Portal Acceptance Status** | `[e.g. Successfully Evaluated / Accepted]` |
| **Public Leaderboard Macro F1** | `[Enter your Public LB Macro F1 score here]` |
| **Public Leaderboard Rank** | `[Enter your Leaderboard Rank, e.g. Top 3]` |
| **Total Participants on Leaderboard**| `[Enter total active participants]` |
| **Variance vs. Detector CV (0.6336)** | `[Public LB Score - 0.6336]` |
| **Final Competition Standing / Prize**| `[Record after Round 1 evaluation concludes]` |

---

## 4. Key Project Artifacts Summary

- **Source Code:** Modular pipeline in `src/` (`data_loader.py`, `feature_engineering.py`, `phase5_cotrending.py`, `phase5_features.py`, `phase5_generate_submissions.py`).
- **Features:** Columnar parquets in `data/processed/train_features_v5.parquet` (18,000 × 88) and `test_features_v5.parquet` (7,000 × 88).
- **Submissions:** Official promoted candidate `submissions/submission_FINAL.csv`, original backup `submissions/submission_FINAL_PHASE4_BACKUP.csv`, and candidate versions `submission_PHASE5_candidate_01.csv` & `submission_PHASE5_candidate_02.csv`.
- **Documentation:** Full technical reports in `reports/` and project guides in `docs/`.
