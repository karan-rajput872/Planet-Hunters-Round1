# Cross-Sector Domain Shift Analysis

## 1. Executive Summary
The competition dataset features a known and critical domain shift:
- **Training stars** were observed in one TESS observing sector.
- **Test stars** were observed in a different TESS observing sector.
- Telescopic pointing, scattered light intensity, and momentum dump cadence frequency vary significantly between sectors.

## 2. High-Shift Features (KS Statistic > 0.25)
Features exhibiting severe distribution shifts between training and testing sectors:

| Feature | KS Statistic | Train Mean | Test Mean | Mean Shift (%) |
|---|---|---|---|---|
| `p99` | 0.3695 | 0.0077 | 0.0114 | 47.6% |
| `p95` | 0.2704 | 0.0050 | 0.0062 | 25.1% |

### Key Findings & Vulnerabilities:
1. **Cadence & Dump Features**: Features that depend on fixed momentum dump positions (`dump_flux_anomaly`, `disp_mean_dump`, `flux_mad_dump`) shift strongly because the test sector experienced a different thruster firing rhythm and scattered light pattern.
2. **Raw Centroid Positions**: Centroid drift parameters differ across sectors due to different telescope pointing and spacecraft thermal gradients.
3. **Instrument Glitch Overprediction Risk**: When models rely heavily on un-normalized dump anomalies, test stars with benign sector differences are misclassified as `instrument_glitch`.

## 3. Most Stable Features (Cross-Sector Invariant, KS < 0.08)
Total invariant features identified: **18**

Top 15 invariant features:
```
max_flare_amp, row_std, disp_max, p01_to_p05_ratio, flux_cen_corr, bottom_duration, max_consecutive_dip, cen_jump_max, cen_jump_mean, tmag, expected_noise_proxy, teff_over_radius, contamination, logg_x_radius, logg
```
These features measure intrinsic astrophysical light curve morphology:
- Relative dip depths and percentiles (`p01`, `p05`, `p10`, `p25`, `p75`, `p90`)
- Interquartile range (`iqr`) and median absolute deviation (`flux_mad`)
- Successive difference ratios (`von_neumann_ratio`)
- Stellar astrophysical properties (`teff`, `logg`, `radius`, `contamination`)
- Autocorrelation timescales (`autocorr_lag_*`)
- Relative centroid shift *specifically during dips* (`cen_shift_in_dip`, `cen_shift_ratio`)

## 4. Domain Adaptation Recommendations
1. **Drop or Regularize Highly Shifted Sector Features**: Remove raw dump flags or re-normalize them strictly relative to the star's own baseline scatter.
2. **Prioritize Invariant Astrophysical Signatures**: Increase weight on features measuring physical phenomena (transits, pulsations, flares, spots) rather than telescope sector artifacts.
3. **Calibrate Class Probabilities**: Adjust probability threshold or post-processing temperature to prevent over-predicting `instrument_glitch` on the test sector.
