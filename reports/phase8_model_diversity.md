# Phase 8: Model Diversity, Stacking & Ensembling Experiments

**Competition:** ML Challenge Hack4Hack 2026 — Round 1  
**Project:** Planet Hunters — Find New Worlds in Starlight  
**Evaluation Metric:** Eight-Class Macro F1  
**Validation Anchor:** Stratified Detector-Channel 5-Fold Cross Validation  
**Date:** 23 October 2026  

---

## 1. Diversity Audit Across Base Learners

The approved Phase 5 solution blends three structurally distinct gradient boosting architectures:
1. **LightGBM (Leaf-wise growth, 63 leaves):** Excels at sharp decision boundaries and non-linear feature splits.
2. **HistGradientBoosting (Depth-wise growth, max depth 8):** Robust to outliers and smooth continuous distributions.
3. **CatBoost (Symmetric / Oblivious trees, depth 6):** Immune to overfitting, strong regularizer.

### Disagreement & Error Correlation Metrics:
- **Pairwise Disagreement:**
  - LightGBM vs. HistGB: **11.37%** (2,046 stars differ)
  - LightGBM vs. CatBoost: **15.33%** (2,760 stars differ)
  - HistGB vs. CatBoost: **15.88%** (2,858 stars differ)
- **Pairwise Error Correlation:** $r = 0.77 - 0.84$.
- **Complementary Power:** HistGB correctly classifies 658 stars where LightGBM fails; LightGBM correctly classifies 670 stars where HistGB fails.

---

## 2. Experimental Stacking & Diversity Architectures Tested

We conducted rigorous experiments using leakage-free Stratified Detector-Channel 5-Fold cross-validation:

| Architecture / Technique | Description | Detector OOF Macro F1 | Fold Mean ($\pm \sigma$) | Delta vs Phase 5 Champion | Acceptance Status |
|:---|:---|:---:|:---:|:---:|:---:|
| **Phase 5 Champion (50/40/10 Blend)** | Linear probability blend of LGB / HGB / CB | **0.63362** | 0.63384 $\pm$ 0.0137 | **Baseline** | **APPROVED CHAMPION** |
| **Power Scaling ($p=1.5$)** | Non-linear probability sharpening: $P \propto P^{1.5}$ | **0.63408** | 0.63430 $\pm$ 0.0135 | **+0.00046** | Below +0.003 Gate |
| **Fine Weight Blend (45/45/10)** | Equal-weight tree blend with CatBoost | **0.63381** | 0.63395 $\pm$ 0.0139 | **+0.00019** | Below +0.003 Gate |
| **Nested Threshold Multipliers** | Nelder-Mead class multipliers in nested 5-fold CV | 0.63353 | 0.63358 $\pm$ 0.0138 | **-0.00009** | Neutral / Negative |
| **Stacking Meta-Learner (LogReg)** | L2-regularized multinomial logistic regression on 24 OOF probs | 0.63225 | 0.63252 $\pm$ 0.0142 | **-0.00136** | **Regression** |
| **Stacking + Top 5 Astro Features** | Logistic regression on 24 OOF probs + 5 domain features | 0.63171 | 0.63183 $\pm$ 0.0138 | **-0.00191** | **Regression** |
| **Rank Averaging** | Probability percentile rank averaging | 0.59734 | 0.59785 $\pm$ 0.0170 | **-0.03628** | **Severe Regression** |

---

## 3. Detailed Findings & Mathematical Insights

1. **Why Stacking Regressed (-0.0014 to -0.0019):**
   A second-stage linear meta-learner fits decision boundaries on out-of-fold probability distributions that have already been calibrated by tree ensembles. Because the base models share similar high-confidence predictions on dominant classes (`quiet_star`, `pulsating_star`), the meta-learner assigns excessive weight to majority-class certainty, eroding subtle probabilities for rare classes (`planet`, `background_binary`).
2. **Why Rank Averaging Collapsed (-0.0363):**
   Rank averaging destroys absolute probability calibration. In an 8-class problem with skewed prior distributions (quiet stars represent 20% while planets represent 4.8%), replacing calibrated likelihoods with uniform percentiles artificially forces equal predictions across all classes, devastating precision.
3. **Power Ensembling & Softmax Temperature ($+0.00046$):**
   Slight probability sharpening ($p=1.5$) reduces entropy on high-confidence predictions while maintaining correct class ranking. However, the $+0.00046$ gain is small and falls well below the mandatory $+0.0030$ gate.
