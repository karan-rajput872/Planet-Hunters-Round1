# Planet Hunters: Complete Experimental Journey & Optimization Log (Phases 1–8)

**Project:** Planet Hunters — Find New Worlds in Starlight  
**Competition:** ML Challenge Hack4Hack 2026 — Round 1  
**Author:** Priyanshu Karan (B.Tech CSE, KIIT)  
**Evaluation Metric:** Eight-Class Macro F1  
**Status:** Completed Engineering & Research Project  

---

## Executive Summary of Development Lifecycle

The Planet Hunters project progressed through eight distinct, hypothesis-driven engineering and validation phases. Each phase investigated specific astronomical degeneracies, domain shifts, or architectural hypotheses under strict cross-validation protocols.

| Phase | Core Objective | Primary Model / Pipeline | Stratified OOF Macro F1 | Detector OOF Macro F1 | Public LB Score | Final Decision |
|:---:|:---|:---|:---:|:---:|:---:|:---:|
| **Phase 1** | Exploratory Data Analysis & Baselines | Single LightGBM (31 leaves) | 0.5512 | — | — | Baseline Established |
| **Phase 2** | Feature Engineering & Pseudo-Labeling | Single LightGBM + 85 Features | 0.5480 | — | — | **REJECTED** (Confirmation bias) |
| **Phase 3** | Dual Ensemble & Domain Generalization | 75% LightGBM + 25% HistGB | 0.5915 | 0.5161 | — | Promoted Architecture |
| **Phase 4** | Full Pipeline Release & Submission | Dual Ensemble (Uncotrended) | 0.5915 | 0.5161 | **0.4214** | **DIAGNOSED** (Uncorrected drift) |
| **Phase 5** | Astro Cotrending & Heterogeneous Tri-Ensemble | 50% LGB + 40% HGB + 10% CB | **0.6455** | **0.6336** | *Pending* | **APPROVED CHAMPION** |
| **Phase 6** | Simplex Grid Search & Threshold Tuning | 45% LGB + 45% HGB + 10% CB | 0.6461 | 0.6338 | — | **REJECTED** (+0.0002 < +0.003 gate) |
| **Phase 7** | Error Analysis & Feature Robustness Audit | 45% LGB + 45% HGB + 10% CB | 0.6461 | 0.6338 | — | **REJECTED** (Retained Phase 5) |
| **Phase 8** | Advanced Optimization & Stacking Meta-Models | Power Ensembling ($p=1.5$) | 0.6462 | 0.6341 | — | **REJECTED** (+0.00046 < +0.003 gate) |

---

## Phase 1: Exploratory Data Analysis & Single-Tree Baselines

### 1. Objective
Establish the baseline machine learning performance on 1,315-cadence space telescope light-curves across 18,000 training stars.

### 2. Problem Investigated
Space-based transit photometry contains 8 diverse astronomical classes (`planet`, `eclipsing_binary`, `background_binary`, `starspots`, `pulsating_star`, `flare_star`, `instrument_glitch`, `quiet_star`). The challenge was determining whether raw time-series summary statistics could distinguish shallow planetary transits ($< 1\%$ flux dip) from geometric binary stars and stellar pulsations.

### 3. Implementation Details
- Extracted basic statistical features: mean, standard deviation, skewness, kurtosis, min, max, percentiles.
- Trained a single baseline LightGBM model with 31 leaves.
- Evaluated via standard 5-fold stratified cross-validation.

### 4. Results & Decision
- **Standard Stratified OOF Macro F1:** **0.5512**
- **Decision:** Baseline established. Rare classes (`planet` F1 = 0.38, `background_binary` F1 = 0.42) suffered severely due to the lack of domain-specific detrending and astrometric centroid features.

---

## Phase 2: Domain Feature Engineering & Pseudo-Labeling Audit

### 1. Objective
Expand the feature representation with physical astronomical metrics and evaluate semi-supervised pseudo-labeling.

### 2. Problem Investigated
Could high-confidence predictions on the 7,000 unlabeled test stars be incorporated into training to improve decision boundaries on rare classes?

### 3. Implementation Details
- Engineered 85 domain-informed features, including running median detrending (window = 49 cadences $\approx$ 24.5 hr), transit dip SNR, and 2D centroid displacement.
- Extracted pseudo-labels from test stars where model confidence $P > 0.85$.
- Re-trained LightGBM on the augmented dataset (18,000 labeled + 2,400 pseudo-labeled test stars).

### 4. Results & Decision
- **Standard Stratified OOF Macro F1:** Dropped from **0.5512 to 0.5480** (-0.0032 regression).
- **Forensic Discovery:** Over 68% of pseudo-labeled stars belonged to majority or high-amplitude classes (`pulsating_star`, `instrument_glitch`), while only 2.1% were `planet` or `background_binary`. The pseudo-labels reinforced majority-class bias and caused decision boundary degradation (confirmation bias).
- **Decision:** **FIRM REJECTION.** Pseudo-labeling was permanently removed from the project pipeline.

---

## Phase 3: Dual-Ensemble Architecture & Domain Generalization Audit

### 1. Objective
Combine structurally diverse gradient boosting algorithms and audit cross-camera generalization.

### 2. Problem Investigated
Single-tree models tend to overfit high-frequency noise. Combining a leaf-wise growth algorithm (LightGBM) with a depth-wise algorithm (HistGradientBoosting) could provide complementary regularization.

### 3. Implementation Details
- Built a 5-fold cross-validated dual ensemble:
  - **LightGBM:** 63 leaves, learning rate 0.04, feature fraction 0.8.
  - **HistGradientBoosting:** Max depth 8, max iterations 450, L2 regularization 1.5.
- Blended probabilities using a 75% LightGBM / 25% HistGB weighting.
- Formulated the **Stratified Detector-Channel 5-Fold Validation** split (grouping by `camera` and `ccd`) to simulate out-of-sector cross-detector generalization.

### 4. Results & Decision
- **Standard Stratified OOF Macro F1:** **0.5915** (+0.0403 improvement over Phase 1).
- **Detector-Channel OOF Macro F1:** **0.5161** (-0.0754 drop compared to standard CV).
- **Decision:** Promoted architecture to the Phase 4 competition candidate. The large gap between standard CV (0.5915) and detector CV (0.5161) was flagged as an early warning of sensor-level domain shift.

---

## Phase 4: Full-Pipeline Release & Public Leaderboard Diagnostic

### 1. Objective
Package the Phase 3 dual ensemble into a reproducible competition submission pipeline and evaluate it on the Hack4Hack Round 1 leaderboard.

### 2. Problem Investigated
Validate whether offline cross-validation performance transferred to the public test leaderboard.

### 3. Implementation Details
- Built `generate_submission.py` and a 14-point automated submission validator (`validate_submission.py`).
- Generated `submissions/submission_FINAL_PHASE4_BACKUP.csv` (SHA-256: `F53A08C47155BC907F855B0626CB38134AAE298A58903B18F3D56818F0C053C1`).
- Evaluated on the competition portal.

### 4. Results & Decision
- **Public Leaderboard Macro F1:** **0.4214** (Uploads #1 and #2 yielded identical scores).
- **Forensic Diagnosis:** The massive drop from internal CV (0.5915) to leaderboard (0.4214) matched the drop predicted by the Detector-Channel CV (0.5161). Spacecraft thermal breathing and pointing jitter in the test sector caused uncotrended models to hallucinate trends, predicting 46.8% of test stars as `pulsating_star` (27.2%) or `instrument_glitch` (19.6%).
- **Decision:** Preserved the Phase 4 submission as a reference baseline and initiated an emergency forensic audit (Phase 5).

---

## Phase 5: Astronomical Cotrending & Heterogeneous Tri-Ensemble Champion

### 1. Objective
Eliminate instrumental sensor systematics via Cotrending Basis Vector (CBV) subtraction and construct a 3-way heterogeneous ensemble.

### 2. Problem Investigated
Space telescope cameras exhibit common-mode noise patterns (pointing drift, orbital thermal cycles) that overwhelm subtle astrophysical signals. Section 8 of the problem statement recommended "thinking like an astronomer" by subtracting the common trend per camera/CCD.

### 3. Implementation Details
- **Vectorized Common-Mode Median Cotrending (`src/phase5_cotrending.py`):** Computed instantaneous median flux and centroid vectors across all stars observed by each `(camera, ccd)` detector channel, subtracting them from each star's time-series:
  $$\tilde{f}_i(t) = f_i(t) - \text{median}_{j \in \text{channel}}(f_j(t))$$
- **88 Astronomical Features (`src/phase5_features.py`):** Extracted transit odd-even depth ratios, transit duty cycle, Box Least Squares (BLS) dip SNR, and in/out-of-dip astrometric centroid displacement on cotrended signals.
- **Tri-Model Ensemble:** Integrated CatBoost (symmetric oblivious trees) alongside LightGBM and HistGradientBoosting:
  $$P(c) = 0.50 \cdot P_{\text{LGB}}(c) + 0.40 \cdot P_{\text{HGB}}(c) + 0.10 \cdot P_{\text{CB}}(c)$$

### 4. Results & Decision
- **Kolmogorov-Smirnov Feature Drift:** Reduced by **60.3%** across all features (mean KS: 0.1326 $\rightarrow$ 0.0526).
- **Detector-Channel OOF Macro F1:** Surged from **0.5161 to 0.6336** (+0.1175 / +22.8% relative gain).
- **Standard Stratified OOF Macro F1:** **0.6455** (+0.0540 over Phase 4).
- **Generated File:** `submissions/submission_FINAL.csv` (SHA-256: `6A378EAE06765A28A39D41A322F47FF25512A43A47827FF4576940282B74330E`).
- **Decision:** **APPROVED AS THE PERMANENT CHAMPION MODEL.**

---

## Phase 6: Simplex Grid Search & Decision Multiplier Audit

### 1. Objective
Investigate whether fine-tuning ensemble blending weights or post-hoc probability threshold multipliers could improve performance.

### 2. Problem Investigated
Test 45 simplex weight formulations and evaluate whether adjusting class-specific probability multipliers via Nelder-Mead optimization could address class imbalance without overfitting.

### 3. Implementation Details
- Evaluated linear probability combinations across a 45-point grid.
- Implemented a nested 5-fold cross-validation routine to tune 8 class decision multipliers on training folds and evaluate them on held-out folds.

### 4. Results & Decision
- **Peak Alternative Blend (45% LGB + 45% HGB + 10% CB):** Detector OOF = **0.63381** (a tiny $+0.00019$ gain over Phase 5's 0.63362).
- **Nested Threshold Tuning:** Yielded $+0.00000$ holdout gain across all 5 folds; class multipliers converged to 1.0, proving raw probabilistic argmax was already optimal.
- **Prediction Shift:** Only 30 out of 7,000 predictions (0.43%) differed from Phase 5.
- **Decision:** **REJECTED.** The $+0.00019$ delta fell far below the mandatory $+0.0030$ acceptance gate and was within CV standard error ($\pm 0.0139$). Candidate preserved as `submission_PHASE6_candidate_01.csv`.

---

## Phase 7: Deep Error Diagnostics & Model Diversity Audit

### 1. Objective
Conduct a granular error analysis across all 18,000 out-of-fold predictions to determine physical failure modes and evaluate architectural disagreement.

### 2. Problem Investigated
Identify the primary contributors to Macro F1 loss and determine whether base models contributed complementary predictive information.

### 3. Implementation Details
- Generated complete confusion matrices, class-wise precision/recall, and pairwise error correlation matrices across LightGBM, HistGB, and CatBoost.
- Measured pairwise model disagreement:
  - LGB vs HistGB: **11.37%** (2,046 stars differ)
  - LGB vs CatBoost: **15.33%** (2,760 stars differ)
  - HistGB vs CatBoost: **15.88%** (2,858 stars differ)

### 4. Key Diagnostic Discoveries
- **Top Loss Contributors:** `planet` (loss contribution = 0.0679, F1 = 0.4571) and `starspots` (loss contribution = 0.0583, F1 = 0.5338).
- **Physical Confusion Hotspots:**
  - 898 `starspots` misclassified as `quiet_star`: Low-amplitude rotational spot modulation ($< 0.3\%$) fell below observational photon noise ($\sigma_{\text{photon}} \approx 0.0018$).
  - 669 `planet` misclassified as `quiet_star`: Shallow transits ($< 0.15\%$ depth) on faint hosts ($T_{\text{mag}} > 14$) fell below the BLS detection threshold.
- **Decision:** **RETAIN PHASE 5 CHAMPION.** Reconfirmed that attempting to force detections below the photon noise floor causes severe false-positive inflation on quiet stars. Candidate preserved as `submission_PHASE7_candidate_01.csv`.

---

## Phase 8: Advanced Optimization, Stacking & Ensembling Experiments

### 1. Objective
Explore second-stage stacking meta-learners, power ensembling (temperature sharpening), and rank averaging to test if non-linear probability combinations could break the 0.6336 plateau.

### 2. Problem Investigated
Can a logistic regression meta-learner trained on out-of-fold probability distributions extract non-linear decision boundaries that simple weighted averaging cannot?

### 3. Implementation Details
Evaluated five distinct experimental paradigms under strict leakage-free Detector-Channel 5-Fold cross-validation:
1. **Power Ensembling / Softmax Temperature ($p=1.5$):** $P_{\text{pow}}(c) \propto P(c)^{1.5}$.
2. **Stacking Meta-Learner (Multinomial Logistic Regression):** Fit on 24 OOF probability features (8 classes $\times$ 3 base models).
3. **Stacking + Top 5 Astronomical Features:** Fit on 24 OOF probabilities plus normalized `transit_depth`, `transit_snr`, `flux_mad`, `centroid_disp_max`, and `p01`.
4. **Probabilistic Rank Averaging:** Uniform percentile rank transformation across classes.
5. **Fine-Grained Convex Simplex Search:** Evaluated 8 fine-grained weight vectors.

### 4. Empirical Benchmark Results

| Experiment Description | Detector OOF Macro F1 | Fold Mean ($\pm \sigma$) | Delta vs. Phase 5 | Engineering Verdict |
|:---|:---:|:---:|:---:|:---|
| **Phase 5 Champion (50/40/10 Linear)** | **0.63362** | 0.63384 $\pm$ 0.0137 | Baseline | **APPROVED CHAMPION** |
| **Power Ensembling ($p=1.5$)** | **0.63408** | 0.63430 $\pm$ 0.0135 | **+0.00046** | Below +0.003 Gate (Rejected) |
| **Phase 6/7 Alternative (45/45/10)** | **0.63381** | 0.63395 $\pm$ 0.0139 | **+0.00019** | Below +0.003 Gate (Rejected) |
| **Nested Threshold Multipliers** | 0.63353 | 0.63358 $\pm$ 0.0138 | **-0.00009** | Neutral / Negative (Rejected) |
| **Stacking Meta-Learner (LogReg)** | 0.63225 | 0.63252 $\pm$ 0.0142 | **-0.00136** | **Regression** (Rejected) |
| **Stacking + Top 5 Astro Features** | 0.63171 | 0.63183 $\pm$ 0.0138 | **-0.00191** | **Regression** (Rejected) |
| **Probabilistic Rank Averaging** | 0.59734 | 0.59785 $\pm$ 0.0170 | **-0.03628** | **Severe Regression** (Rejected) |

### 5. Why Stacking and Rank Averaging Failed
- **Stacking Regression (-0.0014):** Tree models produce calibrated probabilities. The meta-learner assigned disproportionate weight to majority-class certainty (`quiet_star`, `pulsating_star`), compressing subtle probability tails for rare classes (`planet`, `background_binary`).
- **Rank Averaging Collapse (-0.0363):** Forcing uniform rank distributions destroyed natural class priors, resulting in massive false-positive over-prediction for rare classes.
- **Power Ensembling (+0.00046):** Mild probability sharpening ($p=1.5$) slightly reduced entropy, yielding 0.63408, but fell well below the $+0.0030$ acceptance threshold.

### 6. Final Decision & Synchronization
- Candidate generated as `submissions/submission_PHASE8_candidate_01.csv` (SHA-256: `7597C8E9...F181`, 31 changed predictions, 14/14 checks pass).
- **FINAL VERDICT: RETAIN APPROVED CHAMPION `submissions/submission_FINAL.csv`.** Negative experimental results were preserved and documented as valuable engineering findings.
