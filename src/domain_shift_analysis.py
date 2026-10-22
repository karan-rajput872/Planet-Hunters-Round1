import sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src import config

def analyze_domain_shift():
    print("=" * 60)
    print("COMPREHENSIVE CROSS-SECTOR DOMAIN SHIFT ANALYSIS")
    print("=" * 60)

    train_feat_path = config.PROCESSED_DATA_DIR / "train_features.parquet"
    test_feat_path = config.PROCESSED_DATA_DIR / "test_features.parquet"

    train_df = pd.read_parquet(train_feat_path)
    test_df = pd.read_parquet(test_feat_path)

    shift_records = []

    for col in train_df.columns:
        train_vals = train_df[col].dropna()
        test_vals = test_df[col].dropna()

        # Kolmogorov-Smirnov test
        ks_stat, p_val = stats.ks_2samp(train_vals, test_vals)

        train_mean = float(train_vals.mean())
        test_mean = float(test_vals.mean())
        mean_diff_pct = abs(train_mean - test_mean) / (abs(train_mean) + 1e-6) * 100

        shift_records.append({
            "feature": col,
            "ks_stat": round(ks_stat, 4),
            "p_value": p_val,
            "train_mean": round(train_mean, 4),
            "test_mean": round(test_mean, 4),
            "mean_diff_pct": round(mean_diff_pct, 2)
        })

    shift_df = pd.DataFrame(shift_records).sort_values("ks_stat", ascending=False)

    print("\nTop 15 Features with Highest Cross-Sector Domain Shift (KS statistic):")
    print(shift_df.head(15).to_string(index=False))

    # Save CSV
    shift_df.to_csv(config.REPORTS_DIR / "feature_domain_shift.csv", index=False)

    # Write Markdown Report
    high_shift = shift_df[shift_df["ks_stat"] > 0.25]
    stable_feats = shift_df[shift_df["ks_stat"] < 0.08]

    report_md = f"""# Cross-Sector Domain Shift Analysis

## 1. Executive Summary
The competition dataset features a known and critical domain shift:
- **Training stars** were observed in one TESS observing sector.
- **Test stars** were observed in a different TESS observing sector.
- Telescopic pointing, scattered light intensity, and momentum dump cadence frequency vary significantly between sectors.

## 2. High-Shift Features (KS Statistic > 0.25)
Features exhibiting severe distribution shifts between training and testing sectors:

| Feature | KS Statistic | Train Mean | Test Mean | Mean Shift (%) |
|---|---|---|---|---|
"""
    for _, row in high_shift.iterrows():
        report_md += f"| `{row['feature']}` | {row['ks_stat']:.4f} | {row['train_mean']:.4f} | {row['test_mean']:.4f} | {row['mean_diff_pct']:.1f}% |\n"

    report_md += f"""
### Key Findings & Vulnerabilities:
1. **Cadence & Dump Features**: Features that depend on fixed momentum dump positions (`dump_flux_anomaly`, `disp_mean_dump`, `flux_mad_dump`) shift strongly because the test sector experienced a different thruster firing rhythm and scattered light pattern.
2. **Raw Centroid Positions**: Centroid drift parameters differ across sectors due to different telescope pointing and spacecraft thermal gradients.
3. **Instrument Glitch Overprediction Risk**: When models rely heavily on un-normalized dump anomalies, test stars with benign sector differences are misclassified as `instrument_glitch`.

## 3. Most Stable Features (Cross-Sector Invariant, KS < 0.08)
Total invariant features identified: **{len(stable_feats)}**

Top 15 invariant features:
```
{', '.join(stable_feats['feature'].head(15).tolist())}
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
"""

    report_path = config.REPORTS_DIR / "domain_shift_analysis.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_md)
    print(f"\nSaved domain shift report to: {report_path}")

if __name__ == "__main__":
    analyze_domain_shift()
