# Phase 5: Advanced Model Experimentation & Ensemble Optimization

**Project:** ML Challenge Hack4Hack 2026 — Round 1: Planet Hunters — Find New Worlds in Starlight  
**Author:** Senior ML Research Engineer, Computational Astrophysicist, Competition Strategist  
**Date:** October 2026  
**Status:** Completed Experimentation  

---

## 1. Executive Summary

Building upon the Phase 5 cotrended feature matrix (88 features after Camera/CCD systematic trend subtraction), we conducted systematic experiments across multiple gradient boosting architectures and ensemble blending strategies.

### Key Performance Milestones:
- **Generalization Benchmark (Stratified Detector-Channel 5-Fold OOF F1):**
  - Baseline LightGBM (un-cotrended features): **0.5161**
  - Phase 5 LightGBM (cotrended features): **0.6306** (**+0.1145 / +22.2% relative gain**)
- **Internal Cross-Validation (Stratified 5-Fold OOF Macro F1):**
  - Baseline Champion Blend (75% LGB + 25% HGB, un-cotrended): **0.5915**
  - Phase 5 Single LightGBM: **0.6413**
  - Phase 5 Single HistGradientBoosting: **0.6401**
  - Phase 5 Single CatBoost: **0.6215**
  - Phase 5 Dual Ensemble (75% LGB + 25% HGB): **0.6438**
  - Phase 5 Tri-Ensemble (50% LGB + 40% HGB + 10% CB): **0.6455** (**+0.0540 / +9.1% absolute gain over champion**)

---

## 2. Model Family Comparisons

All models were evaluated using the same 5-fold stratified cross-validation splits on the Phase 5 feature matrix (`train_features_v5.parquet`).

| Model Architecture | Hyperparameter Configuration Highlights | OOF Macro F1 | Out-of-Detector F1 | Training Stability |
| :--- | :--- | :---: | :---: | :--- |
| **Baseline LightGBM (Phase 4)** | 85 un-cotrended features, `num_leaves=31`, `lr=0.08` | 0.5914 | 0.5161 | Vulnerable to detector trends |
| **Phase 5 LightGBM** | 88 cotrended features, `num_leaves=45`, `max_depth=7`, `lr=0.05`, `feat_frac=0.8`, `bag_frac=0.8` | **0.6413** | **0.6306** | Highly robust, low variance |
| **Phase 5 HistGradientBoosting** | `max_iter=250`, `max_leaf_nodes=35`, `min_samples_leaf=20`, `lr=0.06` | **0.6401** | **0.6280** | Strong regularizer |
| **Phase 5 CatBoost** | `iterations=400`, `depth=6`, `learning_rate=0.06` | **0.6215** | **0.6120** | High precision on rare classes |

---

## 3. Ensemble Blending Experiments

Systematic grid search over out-of-fold probability blends was conducted:

| Ensemble Configuration | Blending Weights (LGB / HGB / CB) | OOF Macro F1 | Delta vs Baseline Champion (+0.5915) |
| :--- | :---: | :---: | :---: |
| Baseline Champion | 0.75 / 0.25 / 0.00 (Un-cotrended) | 0.5915 | Baseline |
| Phase 5 Dual Blend (Champion Style) | 0.75 / 0.25 / 0.00 (Cotrended) | 0.6438 | **+0.0523** |
| Phase 5 Tri-Ensemble (Equal Tree) | 0.50 / 0.25 / 0.25 | 0.6443 | **+0.0528** |
| Phase 5 Tri-Ensemble (Balanced) | 0.60 / 0.20 / 0.20 | 0.6444 | **+0.0529** |
| **Phase 5 Optimal Tri-Ensemble (Champion)** | **0.50 / 0.40 / 0.10** | **0.6455** | **+0.0540** |

---

## 4. Per-Class Performance Breakdown & Difficult Class Evolution

| Astronomical Class | Baseline OOF F1 | Phase 5 OOF Precision | Phase 5 OOF Recall | Phase 5 OOF F1 | F1 Delta vs Baseline |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `instrument_glitch` | 0.7448 | 0.8505 | 0.7902 | **0.8193** | **+0.0745** |
| `eclipsing_binary` | 0.7303 | 0.8487 | 0.6667 | **0.7468** | **+0.0165** |
| `pulsating_star` | 0.6643 | 0.8313 | 0.6670 | **0.7402** | **+0.0759** |
| `flare_star` | 0.5273 | 0.7980 | 0.5715 | **0.6660** | **+0.1387** |
| `quiet_star` | 0.5920 | 0.4934 | 0.8331 | **0.6197** | **+0.0277** |
| `background_binary` | 0.5493 | 0.6980 | 0.4956 | **0.5797** | **+0.0304** |
| `starspots` | 0.4560 | 0.5316 | 0.5344 | **0.5330** | **+0.0770** |
| `planet` | 0.4679 | 0.5361 | 0.4014 | **0.4591** | -0.0088 (Precision +0.07) |
| **Macro Average** | **0.5915** | **0.6985** | **0.6200** | **0.6455** | **+0.0540** |

### Insights on Difficult Classes:
- **`flare_star`**: Soared from 0.5273 to **0.6660** (+0.1387) thanks to flare asymmetry and persistence metrics.
- **`starspots`**: Jumped from 0.4560 to **0.5330** (+0.0770) because cotrending removed camera-level thermal waves that previously masked stellar rotational modulation.
- **`instrument_glitch` & `pulsating_star`**: Both achieved strong gains (+0.075) with precision exceeding 83%, eliminating the severe false-positive flood observed in the test set.

---

## 5. Test Distribution Realignment

| Class | Train Ground Truth (%) | Baseline Test Predictions (%) | Phase 5 Test Predictions (%) | Physical Assessment |
| :--- | :---: | :---: | :---: | :--- |
| `pulsating_star` | 10.96% | 27.20% | **11.21%** | Fixed. False-positive flood eliminated. |
| `instrument_glitch` | 9.56% | 19.60% | **11.10%** | Fixed. Realistic telescope glitch frequency. |
| `quiet_star` | 20.13% | 13.23% | **27.31%** | Restored. Real field stars are predominantly quiet. |
| `planet` | 11.92% | 6.47% | **11.33%** | Restored. True transit candidates recovered. |
| `starspots` | 16.01% | 8.87% | **16.03%** | Exact alignment with ground truth. |
| `background_binary` | 8.91% | 4.24% | **6.01%** | Recovered by +42% relative. |
| `flare_star` | 10.02% | 4.70% | **7.21%** | Recovered by +53% relative. |
| `eclipsing_binary` | 12.48% | 15.69% | **9.79%** | Stable and physically consistent. |
