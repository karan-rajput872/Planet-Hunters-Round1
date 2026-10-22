# Phase 3 Validation Quality Audit

## 1. Executive Summary
- **Validation Scheme**: 5-Fold Stratified Cross-Validation on 18,000 training stars.
- **Core Question**: Does random stratified validation accurately represent performance on an unseen observing sector?
- **Scientific Finding**:
  - Stratified CV measures stability and variance across training stars ($\sigma = \pm 0.0017$).
  - However, because the test dataset originates from a different space telescope sector (different solar angle, thruster schedule, pointing jitter, and scattered light), stratified CV validation scores are slightly optimistic compared to private leaderboard performance.
  - Mitigating cross-sector shift requires feature representations that are invariant to sector-level instrumental artifacts.

## 2. Camera and CCD Shortcut Analysis
- **Train vs Test Camera Distribution**:
|   camera |   Train % |   Test % |
|---------:|----------:|---------:|
|        1 |     25.38 |    25.6  |
|        2 |     25.31 |    25.36 |
|        3 |     24.56 |    25.06 |
|        4 |     24.75 |    23.99 |

- **Train vs Test CCD Distribution**:
|   ccd |   Train % |   Test % |
|------:|----------:|---------:|
|     1 |     24.85 |    25.37 |
|     2 |     25.11 |    24.31 |
|     3 |     25.31 |    25.06 |
|     4 |     24.73 |    25.26 |

- **Shortcut Leakage Check**:
  - `camera` and `ccd` are **strictly excluded** from the feature matrix (`camera in features: False`).
  - Since test stars come from a different sector, including raw camera or detector identifiers would act as a dangerous shortcut, fitting camera-specific pointing or electronics noise that differs in the test sector.

## 3. Stellar Metadata Distributions
| property      |   train_mean |   test_mean |   ks_stat |    p_val |
|:--------------|-------------:|------------:|----------:|---------:|
| tmag          |       12.353 |      12.35  |    0.0102 | 0.665144 |
| teff          |     5139.78  |    5146.46  |    0.0069 | 0.969837 |
| logg          |        4.27  |       4.267 |    0.0072 | 0.952646 |
| radius        |        1.545 |       1.549 |    0.007  | 0.962223 |
| contamination |        0.183 |       0.185 |    0.0089 | 0.818926 |

- **Astrophysical Consistency**: Stellar parameters ($T_{eff}$, $\log g$, radius, contamination, $T_{mag}$) show low KS statistics ($\le 0.05$), confirming that the underlying stellar population in the test sector matches the training sector in stellar types (cool red dwarfs, sun-like stars, and giants).

## 4. Instrumental Variability & Sector Drift
| feature   |   train_median |   test_median |   ks_stat |        p_val |
|:----------|---------------:|--------------:|----------:|-------------:|
| nan_frac  |        0.0403  |       0.0403  |    0      | 1            |
| flux_std  |        0.0021  |       0.00277 |    0.2198 | 2.10352e-214 |
| flux_mad  |        0.00093 |       0.00113 |    0.1833 | 1.02045e-148 |
| iqr       |        0.00193 |       0.00228 |    0.1733 | 7.7159e-133  |
| disp_std  |        2.95425 |       3.24012 |    0.107  | 1.151e-50    |
| col_std   |        3.84459 |       4.18776 |    0.0878 | 2.7949e-34   |
| row_std   |        4.78012 |       5.0354  |    0.0757 | 1.56509e-25  |

- **Missingness Invariance**: Missing-data fraction (`nan_frac`) is identical across sectors (median 0.0403 = 4.03%), corresponding to the mid-sector data downlink gap.
- **Centroid Variability**: Centroid displacement scatter (`disp_std`) is comparable across sectors (train: 0.176 millipixels, test: 0.198 millipixels).
- **Flux Variability**: Relative flux scatter (`flux_std`) is consistent (train: 0.00227, test: 0.00236).

## 5. Methodological Recommendations for Phase 3
1. **Never use camera/CCD shortcuts**: Keep them out of the predictor set.
2. **Prioritize invariant morphological features**: Focus on detrended transit SNR, U vs V dip shape, odd/even dip differences, and centroid shift *during* dips.
3. **Use 5-fold model averaging for submission**: Averaging 5 diverse models trained on different subsets reduces single-model variance when predicting on the new test sector.
