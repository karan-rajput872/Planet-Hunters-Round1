# Phase 8: Candidate Comparison & Submission Verification

**Competition:** ML Challenge Hack4Hack 2026 — Round 1  
**Project:** Planet Hunters — Find New Worlds in Starlight  
**Evaluation Metric:** Eight-Class Macro F1  
**Date:** 23 October 2026  

---

## 1. Candidate Files Inventory & Cryptographic Hashes

| Submission File | Architecture | Detector OOF Macro F1 | Verified SHA-256 Checksum | Validator Status | Recommendation |
|:---|:---|:---:|:---|:---:|:---:|
| [`submissions/submission_FINAL.csv`](file:///c:/Users/KIIT/OneDrive/Documents/Planet-Hunters-Round1/submissions/submission_FINAL.csv) | **Phase 5 Tri-Ensemble (50/40/10)** | **0.63362** | `6A378EAE06765A28A39D41A322F47FF25512A43A47827FF4576940282B74330E` | **14/14 PASS** | **OFFICIAL APPROVED FINAL** |
| [`submissions/submission_PHASE8_candidate_01.csv`](file:///c:/Users/KIIT/OneDrive/Documents/Planet-Hunters-Round1/submissions/submission_PHASE8_candidate_01.csv) | Phase 8 Power Scaled (p=1.5 on 45/45/10) | **0.63408** | `7597C8E9130502595537C3F3F3B5265348403FC0EFF81680DBE9D996EC79F181` | **14/14 PASS** | **REJECTED (Below Gate)** |
| [`submissions/submission_PHASE7_candidate_01.csv`](file:///c:/Users/KIIT/OneDrive/Documents/Planet-Hunters-Round1/submissions/submission_PHASE7_candidate_01.csv) | Phase 7 Linear Blend (45/45/10) | **0.63381** | `243B382359960EFCC2FB44A75DFAA993F906B0052B4D7479813C6F1BF9D7AC8B` | **14/14 PASS** | **REJECTED (Below Gate)** |
| [`submissions/submission_FINAL_PHASE4_BACKUP.csv`](file:///c:/Users/KIIT/OneDrive/Documents/Planet-Hunters-Round1/submissions/submission_FINAL_PHASE4_BACKUP.csv) | Phase 4 Dual Ensemble (Uncotrended) | 0.51610 | `F53A08C47155BC907F855B0626CB38134AAE298A58903B18F3D56818F0C053C1` | **14/14 PASS** | Preserved (LB 0.4214) |

---

## 2. Test Prediction Transition Analysis (Approved Final vs. Phase 8 Candidate)

Out of 7,000 test stars, exactly **31 predictions change** (99.56% identity, 0.44% shift):

```
Approved Final \ Phase 8 Cand | quiet_star | starspots | planet | eclipsing_binary | background_binary | pulsating_star
------------------------------+------------+-----------+--------+------------------+-------------------+---------------
quiet_star                    |    1907    |     1     |   0    |        0         |         0         |       4
starspots                     |      4     |   1112    |   0    |        0         |         1         |       5
planet                        |      5     |     0     |  787   |        1         |         0         |       0
eclipsing_binary              |      0     |     0     |   1    |      683         |         1         |       0
flare_star                    |      2     |     1     |   0    |        0         |         0         |       0
pulsating_star                |      1     |     0     |   0    |        0         |         0         |     784
background_binary             |      0     |     0     |   0    |        0         |       420         |       1
```

### Shifts by Astronomical Detector Channel:
- Camera 1: 10 changes
- Camera 2: 10 changes
- Camera 3: 3 changes
- Camera 4: 8 changes

The changes are distributed evenly across cameras, confirming that no camera-specific bias was introduced. However, shifting only 31 marginal predictions on 7,000 stars represents leaderboard noise, not a structural breakthrough.
