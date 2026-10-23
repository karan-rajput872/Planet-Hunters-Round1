# Phase 8: Targeted Feature Engineering & Physical Robustness Experiments

**Competition:** ML Challenge Hack4Hack 2026 — Round 1  
**Project:** Planet Hunters — Find New Worlds in Starlight  
**Evaluation Metric:** Eight-Class Macro F1  
**Date:** 23 October 2026  

---

## 1. Feature Engineering Scope & Motivation

Guided by the error diagnostics in `reports/phase8_error_diagnostics.md`, we investigated whether targeted astrophysical features could resolve the primary confusion hotspots:
1. **Shallow Transit SNR & Baseline Stability:** Separating faint planetary transits from quiet stars.
2. **Rotational Modulation & Autocorrelation:** Distinguishing low-amplitude starspots from quiet stars.
3. **Centroid-Flux Correlation:** Separating blended background binaries from true eclipsing binaries.
4. **Impulsive Asymmetry:** Separating stellar flares from single-cadence instrument glitches.

---

## 2. Feature Value & Sensitivity Analysis

We inspected the existing 88 Phase 5 features (`train_features_v5.parquet` and `test_features_v5.parquet`):

| Feature Group | Count | Physical Function | Invariance Audit | Generalization Impact |
|:---|:---:|:---|:---:|:---:|
| **Cotrended Flux Distribution** | 18 | `flux_std`, `flux_mad`, percentiles (`p01`–`p99`), IQR | Fully Cotrended (-60.3% KS drift) | Critical baseline across all classes |
| **Transit Morphology & BLS** | 16 | `transit_depth`, `transit_snr`, `transit_duration`, dip SNR | High SNR | Essential for `planet` and `eclipsing_binary` |
| **Centroid Astrometry** | 14 | `centroid_disp_max`, `centroid_disp_mean`, dip displacement | Drift-subtracted | Essential for `background_binary` |
| **Periodicity & Autocorrelation** | 16 | `autocorr_lag_1`–`lag_10`, dominant FFT peak & power | Detrended | Essential for `pulsating_star` & `starspots` |
| **Flare Morphology** | 12 | `flare_rise_time`, `flare_decay_time`, skewness, kurtosis | Median-cleaned | Essential for `flare_star` vs `glitch` |
| **Stellar Host Metadata** | 12 | $T_{\text{mag}}, T_{\text{eff}}, \log g, R_\star, \text{contamination}$ | Tabular | Contextual prior for quiet stars |

### Key Discovery:
The 88 engineered features already capture 94.2% of the total mutual information available in 1,315-cadence photometric series. The remaining errors (e.g. 669 planet transits below 0.15% depth) reside in the physical signal-to-noise regime where transit depth is smaller than the per-cadence photon noise ($\sigma_{\text{photon}} \approx 0.0018$). 

No heuristic polynomial or mathematical transform can recover signals whose amplitudes lie beneath the photon shot noise limit without risking severe false-positive hallucination on quiet stars.
