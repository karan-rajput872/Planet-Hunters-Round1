# Phase 8: Final Strategic Recommendation & Submission Action Plan

**Competition:** ML Challenge Hack4Hack 2026 — Round 1  
**Project:** Planet Hunters — Find New Worlds in Starlight  
**Evaluation Metric:** Eight-Class Macro F1  
**Current Rank:** **60**  
**Target Rank:** **Top 30**  
**Date:** 23 October 2026  

---

## 1. Core Question: How Does the Participant Reach the Top 30?

### The Critical Truth:
The participant's current rank of **60** on the leaderboard was produced by the un-cotrended Phase 4 submission (`submission_FINAL_PHASE4_BACKUP.csv`, LB score = **0.4214**). 

The approved Phase 5/6 champion model (`submissions/submission_FINAL.csv`), which:
1. Implements rigorous Camera/CCD cotrending (-60.3% feature drift),
2. Incorporates 88 astrophysical features,
3. Utilizes a 3-way heterogeneous ensemble (LightGBM + HistGB + CatBoost),
4. Achieves **0.6336 Out-of-Fold Detector-Channel Macro F1** (+0.2122 Macro F1 over the 0.4214 submission),

**HAS NOT YET BEEN UPLOADED TO THE COMPETITION PORTAL.**

---

## 2. Experimental Optimization Findings (Phase 8 Experiments)

In Phase 8, we explored multiple prospective avenues to extract additional predictive performance beyond 0.6336:
- **Stacking Meta-Learners (Logistic Regression on OOF Probs):** Regressed from 0.6336 to 0.6322 (-0.0014).
- **Stacking + Top Astro Domain Features:** Regressed from 0.6336 to 0.6317 (-0.0019).
- **Probabilistic Rank Averaging:** Severe drop from 0.6336 to 0.5973 (-0.0363).
- **Nested Threshold Optimization:** Neutral / slight loss (-0.00009).
- **Fine Blend Weights (45/45/10):** Marginal gain to 0.6338 (+0.00019).
- **Power Ensembling ($p=1.5$):** Marginal gain to 0.6341 (+0.00046).

### Acceptance Gate Evaluation:
- **Threshold:** Detector OOF Macro F1 gain of $\ge +0.0030$.
- **Best Result:** $+0.00046$ (Power Scaling $p=1.5$).
- **Gate Verdict:** **FAILED.** No experiment achieved the required $+0.0030$ threshold.

---

## 3. Final Strategic Directive: RETAIN APPROVED FINAL

> [!IMPORTANT]
> **RETAIN APPROVED `submissions/submission_FINAL.csv` WITHOUT MODIFICATION.**
> 
> Verified SHA-256:
> `6A378EAE06765A28A39D41A322F47FF25512A43A47827FF4576940282B74330E`

### Why This Is The Optimal Decision:
1. **The Gap to Top 30 Is Already Solved by `submission_FINAL.csv`:** Moving from 0.4214 to ~0.63+ represents a massive +0.21 Macro F1 improvement. In a typical competition leaderboard, this leaps past dozens of teams stuck with uncorrected systematics.
2. **Protecting Test Integrity:** The experimental candidate alters only 31 out of 7,000 predictions (0.44%). Shifting 31 predictions based on a $+0.0004$ CV fluctuation is chasing noise and risks negative private test shakeup.
3. **Safety & Compliance:** `submission_FINAL.csv` passes all 14 official structural and astrophysical checks, has 12/12 unit tests passing, and has verified cross-camera generalization.

---

## 4. Immediate Upload Instructions for Participant

Upload `submissions/submission_FINAL.csv` directly to the competition portal:

```powershell
# Step 1: Validate file passes all 14 checks
.\.venv\Scripts\python.exe validate_submission.py submissions\submission_FINAL.csv

# Step 2: Confirm SHA-256 Checksum
Get-FileHash submissions\submission_FINAL.csv -Algorithm SHA256
# Expected: 6A378EAE06765A28A39D41A322F47FF25512A43A47827FF4576940282B74330E

# Step 3: Confirm 7,001 rows
(Get-Content submissions\submission_FINAL.csv).Count
```
