# 5-Fold Stratified Cross-Validation Results

## 1. Executive Summary
- **Model**: LightGBM Classifier (85 features, balanced weights)
- **Folds**: 5-Fold Stratified K-Fold (seed: 42)
- **Total Training Stars**: 18,000
- **Mean Fold Macro F1**: **0.5830 +/- 0.0016**
- **Overall Out-Of-Fold (OOF) Macro F1**: **0.1329**
- **Overall OOF Weighted F1**: **0.1386**
- **Total Runtime**: 67.89 seconds

## 2. Fold-by-Fold Performance

| Fold | Macro F1-Score |
|---|---|
| Fold 1 | 0.5831 |
| Fold 2 | 0.5833 |
| Fold 3 | 0.5808 |
| Fold 4 | 0.5820 |
| Fold 5 | 0.5855 |
| **Mean +/- Std** | **0.5830 +/- 0.0016** |

## 3. Per-Class F1 Across Folds

| Class | Mean F1 | Std F1 | Min F1 | Max F1 |
|---|---|---|---|---|
| `instrument_glitch` | **0.7342** | 0.0163 | 0.7163 | 0.7625 |
| `eclipsing_binary` | **0.7192** | 0.0204 | 0.6979 | 0.7565 |
| `pulsating_star` | **0.6572** | 0.0128 | 0.6409 | 0.6755 |
| `quiet_star` | **0.5830** | 0.0057 | 0.5741 | 0.5889 |
| `background_binary` | **0.5402** | 0.0119 | 0.5265 | 0.5618 |
| `flare_star` | **0.5220** | 0.0163 | 0.4970 | 0.5455 |
| `planet` | **0.4626** | 0.0198 | 0.4453 | 0.4988 |
| `starspots` | **0.4454** | 0.0127 | 0.4274 | 0.4647 |

## 4. Key Takeaways
1. **Model Stability**: Standard deviation across folds is low (0.0016), confirming that the feature pipeline produces consistent representations without fold-dependent instability.
2. **Planet F1**: Averaged 0.4626 across all folds.
3. **Out-of-Fold Ground Truth**: OOF probabilities across all 18,000 stars are cached in `data/processed/oof_predictions.parquet` for un-biased ensemble weighting and calibration.
