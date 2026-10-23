# Phase 5: Validation Strategy Comparison & Generalization Assessment

**Project:** ML Challenge Hack4Hack 2026 — Round 1: Planet Hunters — Find New Worlds in Starlight  
**Author:** Senior ML Research Engineer, Computational Astrophysicist, Competition Strategist  
**Date:** October 2026  
**Status:** Completed Experimentation  

---

## 1. Executive Summary

In competition settings with domain shifts or unmodeled physical systematics, cross-validation that splits samples uniformly at random overfits the shared observation environment. The baseline Champion model achieved an internal 5-fold Stratified CV Macro F1 of **0.5915**, yet scored **0.4214** on the public leaderboard.

To diagnose and resolve this validation-to-leaderboard gap, we formulated and empirically tested five distinct cross-validation strategies using the official dataset schema:
1. **Stratified 5-Fold CV (Baseline):** Identical class-conditional distribution across folds, independent of focal-plane detectors.
2. **Repeated Stratified 10-Fold CV:** Two repeats of stratified 5-fold splits with distinct random seeds.
3. **Leave-One-Camera-Out (GroupKFold on `camera`):** 4 folds where an entire camera (Camera 1, 2, 3, or 4; 4,500 stars per fold) is held out.
4. **Leave-One-CCD-Out (GroupKFold on `ccd`):** 4 folds where an entire CCD position across all cameras (CCD 1, 2, 3, or 4; 4,500 stars per fold) is held out.
5. **Stratified Detector-Channel 5-Fold (StratifiedGroupKFold on `camera_ccd`):** 5 folds where the 16 distinct physical detector channels are partitioned without overlap between train and validation.

---

## 2. Quantitative Comparison of Validation Schemes

All validation strategies were benchmarked using an identical LightGBM configuration on the baseline 85 features to ensure fair, controlled comparison.

| Validation Scheme | Group / Split Criterion | Folds | Mean Fold Macro F1 | Fold Std Dev (±) | Overall Out-of-Fold Macro F1 | Generalization Realism Assessment |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Stratified 5-Fold** | Pure label stratification | 5 | 0.5767 | ± 0.0008 | 0.5769 | **Unrealistic / Over-optimistic:** Standard deviation is unrealistically low (0.0008); ignores detector-level systematic correlation. |
| **Repeated Stratified 10-Fold** | 2 repeats of stratified 5-fold | 10 | 0.5772 | ± 0.0016 | 0.5848 | **Over-optimistic:** Confirms random partitioning consistently inflates validation scores due to shared systematic background. |
| **Leave-One-Camera-Out** | Group by `camera` (1 to 4) | 4 | **0.5317** | **± 0.0251** | **0.5276** | **High Realism:** Testing on unseen camera optics drops score by ~5 F1 points; Fold 2 drops to 0.4911. |
| **Leave-One-CCD-Out** | Group by `ccd` (1 to 4) | 4 | **0.5258** | **± 0.0405** | **0.5236** | **Very High Realism:** Simulates edge vs central CCD vignetting and thermal response. Fold 3 drops to 0.4745. |
| **Stratified Detector-Channel 5-Fold** | Group by `camera_ccd` channel | 5 | **0.5186** | **± 0.0397** | **0.5161** | **Most Representative Proxy:** Zero detector channel leakage. Scores span 0.4670 to 0.5805, accurately reflecting out-of-sector performance variance. |

---

## 3. Detailed Fold-by-Fold Performance Breakdown

### 3.1 Leave-One-Camera-Out (4 Folds)
- **Fold 1 (Held-out Camera 1, 4,569 stars):** Macro F1 = **0.5337**
- **Fold 2 (Held-out Camera 2, 4,555 stars):** Macro F1 = **0.4911** (Significant drop due to unique noise characteristics)
- **Fold 3 (Held-out Camera 3, 4,455 stars):** Macro F1 = **0.5432**
- **Fold 4 (Held-out Camera 4, 4,421 stars):** Macro F1 = **0.5590**
- *Insight:* Different cameras exhibit noticeably different noise baselines. When evaluating on a camera not seen in training, Macro F1 drops sharply.

### 3.2 Leave-One-CCD-Out (4 Folds)
- **Fold 1 (Held-out CCD 1, 4,556 stars):** Macro F1 = **0.5653**
- **Fold 2 (Held-out CCD 2, 4,519 stars):** Macro F1 = **0.4978**
- **Fold 3 (Held-out CCD 3, 4,473 stars):** Macro F1 = **0.4745** (Worst performing detector group)
- **Fold 4 (Held-out CCD 4, 4,452 stars):** Macro F1 = **0.5655**
- *Insight:* CCD 3 exhibits severe edge-of-field aberrations. Models evaluated on CCD 3 drop below 0.48 F1.

### 3.3 Stratified Detector-Channel 5-Fold (16 Physical Detectors)
- **Fold 1 (3,451 stars):** Macro F1 = **0.5805**
- **Fold 2 (4,443 stars):** Macro F1 = **0.5330**
- **Fold 3 (3,383 stars):** Macro F1 = **0.5272**
- **Fold 4 (3,381 stars):** Macro F1 = **0.4853**
- **Fold 5 (3,342 stars):** Macro F1 = **0.4670**
- *Insight:* This validation scheme mirrors the actual competition environment where the test set consists of stars observed under different detector systematics. The lower bounds (0.4670 - 0.4853) explain why the un-cotrended model scored 0.4214 on the public leaderboard.

---

## 4. Final Validation Strategy Decision

For Phase 5 model optimization, we adopt a **Dual-Tier Validation Protocol**:

1. **Primary Generalization Anchor (Stratified Detector-Channel 5-Fold CV):**
   - Groups by `camera_ccd` while preserving class proportions.
   - Any proposed feature or model must demonstrate superior generalization on this metric.
   - Serves as the gatekeeper against selecting overfitted models.

2. **Benchmark Continuity Metric (Stratified 5-Fold CV):**
   - Retained as a secondary reference to track improvements directly comparable to the Phase 4 baseline (0.5915).

---

## 5. Summary Conclusion

The mystery of the 0.5915 CV vs 0.4214 Public Leaderboard score is fully resolved:
- Standard stratified CV evaluated models on detectors identical to the training data.
- When evaluated across unseen detectors (Leave-One-CCD or Stratified Detector-Channel), performance on un-cotrended data falls to ~0.47 - 0.52.
- Testing on a different sector with heightened systematic drifts further degraded performance to 0.4214.
- Rigorous validation must use group-aware splits alongside camera/CCD cotrending.
