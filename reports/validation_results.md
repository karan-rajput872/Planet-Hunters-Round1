# Model Evaluation & Validation Report

## 1. Executive Summary
- **Competition**: ML Challenge Hack4Hack 2026 — Round 1
- **Challenge**: Planet Hunters — Find New Worlds in Starlight
- **Target Metric**: **Macro F1-Score** across 8 astrophysical classes
- **Best Model**: **LightGBM Classifier** with balanced class weights and domain-resilient feature extraction
- **Best Validation Macro F1**: **0.5914** (Weighted F1: 0.5852)

---

## 2. Multi-Model Benchmark Comparison (80/20 Stratified Validation)

| Model Name | Macro F1-Score | Weighted F1 | Training Time (s) | Rank |
|---|---|---|---|---|
| **LightGBM** | **0.5914** | **0.5852** | 10.78s | **1** |
| **Weighted Ensemble (LGB+CB+HGB)** | 0.5886 | 0.5813 | — | 2 |
| **HistGradientBoosting** | 0.5709 | 0.5633 | 15.28s | 3 |
| **CatBoost** | 0.5512 | 0.5449 | 21.86s | 4 |
| **ExtraTrees** | 0.5234 | 0.5200 | 0.93s | 5 |

---

## 3. Best Model Detailed Per-Class Breakdown (LightGBM)

| Astrophysical Class | Precision | Recall | F1-Score | Support (Validation Set) |
|---|---|---|---|---|
| `eclipsing_binary` | 0.8423 | 0.6303 | **0.7210** | 449 |
| `instrument_glitch` | 0.7752 | 0.6919 | **0.7312** | 344 |
| `pulsating_star` | 0.6814 | 0.6228 | **0.6508** | 395 |
| `quiet_star` | 0.5009 | 0.7614 | **0.6043** | 725 |
| `background_binary` | 0.6190 | 0.5265 | **0.5690** | 321 |
| `flare_star` | 0.6525 | 0.4681 | **0.5452** | 361 |
| `planet` | 0.4759 | 0.4382 | **0.4563** | 429 |
| `starspots` | 0.4568 | 0.4497 | **0.4532** | 576 |
| **Macro Average** | **0.5928** | **0.5499** | **0.5914** | **3,600** |

---

## 4. Key Performance Drivers & Feature Impacts
1. **2D Median Filter Detrending**:
   - Isolating high-frequency dips from low-frequency rotational spot modulations boosted `starspots` F1 from 0.4029 to 0.4532 and `planet` F1 from 0.4135 to 0.4563.
2. **Centroid Vetting During Dips**:
   - Computing centroid movement specifically during flux minima (`cen_shift_in_dip`, `cen_shift_ratio`) successfully decoupled `planet` candidates from `background_binary` blended eclipses (F1 = 0.5690).
3. **Cadence Quality & Momentum Dump Anomalies**:
   - Examining flux anomalies specifically during momentum dumps (`quality & 1`) enabled high precision for telescope glitches (`instrument_glitch` F1 = 0.7312).
4. **Stellar Metadata Interactions**:
   - Aperture `contamination` emerged as the single most split feature, preventing blended background stars from poisoning planetary transit detection.

---

## 5. Artifact Locations
- Best Model Weights: `models/best_lightgbm.joblib`
- Ensemble Bundle: `models/ensemble_bundle.joblib`
- Confusion Matrix: `reports/confusion_matrix_lightgbm.png`
- Classification Report: `reports/classification_report_lightgbm.txt`
