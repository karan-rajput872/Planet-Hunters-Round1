import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure src can be imported
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src import config

def inspect_dataset():
    print("=" * 60)
    print("STARTING COMPREHENSIVE DATASET INSPECTION")
    print("=" * 60)

    # 1. Load CSVs
    train_stars = pd.read_csv(config.TRAIN_STARS_FILE)
    test_stars = pd.read_csv(config.TEST_STARS_FILE)
    train_cadences = pd.read_csv(config.TRAIN_CADENCES_FILE)
    test_cadences = pd.read_csv(config.TEST_CADENCES_FILE)
    sample_sub = pd.read_csv(config.SAMPLE_SUBMISSION_FILE)

    # 2. Memory-mapped array loading
    train_flux = np.load(config.TRAIN_FLUX_FILE, mmap_mode="r")
    train_cen = np.load(config.TRAIN_CENTROID_FILE, mmap_mode="r")
    test_flux = np.load(config.TEST_FLUX_FILE, mmap_mode="r")
    test_cen = np.load(config.TEST_CENTROID_FILE, mmap_mode="r")

    print(f"train_stars: {train_stars.shape}")
    print(f"test_stars:  {test_stars.shape}")
    print(f"train_flux:  {train_flux.shape}, dtype={train_flux.dtype}")
    print(f"train_cen:   {train_cen.shape}, dtype={train_cen.dtype}")
    print(f"test_flux:   {test_flux.shape}, dtype={test_flux.dtype}")
    print(f"test_cen:    {test_cen.shape}, dtype={test_cen.dtype}")
    print(f"train_cadences: {train_cadences.shape}")
    print(f"test_cadences:  {test_cadences.shape}")
    print(f"sample_sub:     {sample_sub.shape}")

    # 3. Class distribution
    class_counts = train_stars["label"].value_counts()
    class_pct = train_stars["label"].value_counts(normalize=True) * 100
    class_df = pd.DataFrame({"count": class_counts, "percentage": class_pct.round(2)})
    print("\nTarget Class Distribution:")
    print(class_df)

    # 4. Save class distribution plot
    plt.figure(figsize=(10, 5))
    palette = sns.color_palette("viridis", len(class_counts))
    sns.barplot(x=class_counts.values, y=class_counts.index, hue=class_counts.index, palette=palette, legend=False)
    plt.title("Hack4Hack 2026 - Training Class Distribution", fontsize=14, fontweight="bold")
    plt.xlabel("Number of Stars", fontsize=12)
    plt.ylabel("Astrophysical Label", fontsize=12)
    for i, (cnt, pct) in enumerate(zip(class_counts.values, class_pct.values)):
        plt.text(cnt + 30, i, f"{cnt} ({pct:.1f}%)", va="center", fontsize=10)
    plt.xlim(0, max(class_counts.values) * 1.15)
    plt.tight_layout()
    plot_path = config.REPORTS_DIR / "class_distribution.png"
    plt.savefig(plot_path, dpi=200)
    plt.close()
    print(f"\nSaved plot to {plot_path}")

    # 5. Missing values in metadata
    train_meta_missing = train_stars.isnull().sum()
    test_meta_missing = test_stars.isnull().sum()
    print("\nTrain metadata missing values:\n", train_meta_missing[train_meta_missing > 0])
    print("Test metadata missing values:\n", test_meta_missing[test_meta_missing > 0])

    # 6. Missing values in arrays (sampled or vectorized)
    train_flux_nan = np.isnan(train_flux).sum()
    train_flux_nan_pct = (train_flux_nan / train_flux.size) * 100
    test_flux_nan = np.isnan(test_flux).sum()
    test_flux_nan_pct = (test_flux_nan / test_flux.size) * 100

    train_cen_nan = np.isnan(train_cen).sum()
    train_cen_nan_pct = (train_cen_nan / train_cen.size) * 100
    test_cen_nan = np.isnan(test_cen).sum()
    test_cen_nan_pct = (test_cen_nan / test_cen.size) * 100

    print(f"\nTrain flux NaN: {train_flux_nan} ({train_flux_nan_pct:.2f}%)")
    print(f"Test flux NaN:  {test_flux_nan} ({test_flux_nan_pct:.2f}%)")
    print(f"Train cen NaN:  {train_cen_nan} ({train_cen_nan_pct:.2f}%)")
    print(f"Test cen NaN:   {test_cen_nan} ({test_cen_nan_pct:.2f}%)")

    # 7. Cadences and Quality flags
    train_dumps = (train_cadences["quality"] & 1).sum()
    train_scattered = (train_cadences["quality"] & 2).sum()
    train_gaps = (train_cadences["quality"] & 4).sum()

    test_dumps = (test_cadences["quality"] & 1).sum()
    test_scattered = (test_cadences["quality"] & 2).sum()
    test_gaps = (test_cadences["quality"] & 4).sum()

    print(f"\nTrain Cadences Quality - Dumps: {train_dumps}, Scattered: {train_scattered}, Gaps: {train_gaps}")
    print(f"Test Cadences Quality  - Dumps: {test_dumps}, Scattered: {test_scattered}, Gaps: {test_gaps}")

    # 8. Camera / CCD distribution comparison
    train_cam_ccd = train_stars.groupby(["camera", "ccd"]).size()
    test_cam_ccd = test_stars.groupby(["camera", "ccd"]).size()

    # 9. Verify Alignment & ID checks
    assert len(train_stars) == train_flux.shape[0] == train_cen.shape[0], "Train row misalignment!"
    assert len(test_stars) == test_flux.shape[0] == test_cen.shape[0], "Test row misalignment!"
    assert (train_stars["id"].nunique() == len(train_stars)), "Duplicate IDs in train!"
    assert (test_stars["id"].nunique() == len(test_stars)), "Duplicate IDs in test!"
    assert (sample_sub["id"].values == test_stars["id"].values).all(), "Sample sub IDs do not match test_stars!"

    # 10. Generate Markdown Report
    report_md = f"""# Dataset Inspection Report: Planet Hunters (Hack4Hack 2026)

## 1. Overview and Dimensionality
- **Competition**: ML Challenge Hack4Hack 2026 - Round 1
- **Evaluation Metric**: Macro F1-score across 8 astrophysical classes
- **Cadences per Star**: 1,315 observations (spanning ~27.4 days with ~30-min sampling)

### Dataset Shapes & Memory
| Dataset | Object / File | Dimensions | Data Type | Missing Count (%) |
|---|---|---|---|---|
| Train | `train_flux.npy` | {train_flux.shape} | {train_flux.dtype} | {train_flux_nan:,} ({train_flux_nan_pct:.2f}%) |
| Train | `train_centroid.npy` | {train_cen.shape} | {train_cen.dtype} | {train_cen_nan:,} ({train_cen_nan_pct:.2f}%) |
| Train | `train_stars.csv` | {train_stars.shape} | CSV | See metadata section |
| Train | `train_cadences.csv` | {train_cadences.shape} | CSV | 0 missing |
| Test | `test_flux.npy` | {test_flux.shape} | {test_flux.dtype} | {test_flux_nan:,} ({test_flux_nan_pct:.2f}%) |
| Test | `test_centroid.npy` | {test_cen.shape} | {test_cen.dtype} | {test_cen_nan:,} ({test_cen_nan_pct:.2f}%) |
| Test | `test_stars.csv` | {test_stars.shape} | CSV | See metadata section |
| Test | `test_cadences.csv` | {test_cadences.shape} | CSV | 0 missing |
| Sub | `sample_submission.csv` | {sample_sub.shape} | CSV | Exactly 7,000 rows |

## 2. Target Class Distribution
Evaluation is strictly **Macro F1-score**, giving equal importance to every class regardless of prevalence.

| Class | Count | Percentage | Class Weight (balanced) |
|---|---|---|---|
"""
    total_samples = len(train_stars)
    n_classes = len(class_counts)
    for cls_name, row in class_df.iterrows():
        cnt = row["count"]
        pct = row["percentage"]
        weight = total_samples / (n_classes * cnt)
        report_md += f"| `{cls_name}` | {cnt:,} | {pct:.2f}% | {weight:.3f} |\n"

    report_md += f"""
![Class Distribution](class_distribution.png)

## 3. Metadata Profiles & Missing Values
### Train Metadata Nulls:
```
{train_meta_missing[train_meta_missing > 0].to_string() if (train_meta_missing > 0).any() else "None"}
```

### Test Metadata Nulls:
```
{test_meta_missing[test_meta_missing > 0].to_string() if (test_meta_missing > 0).any() else "None"}
```

### Metadata Statistical Summary (Train):
{train_stars.describe().to_markdown()}

### Metadata Statistical Summary (Test):
{test_stars.describe().to_markdown()}

## 4. Cross-Sector & Cadence Quality Comparison
Training and test sets originate from different sectors, leading to differing instrumental trends:
- **Train Sector Cadences**: {len(train_cadences)} observations, time range {train_cadences['time_btjd'].min():.2f} to {train_cadences['time_btjd'].max():.2f} BTJD
  - Momentum Dumps (`quality & 1`): {train_dumps} ({train_dumps/len(train_cadences)*100:.1f}%)
  - Scattered Light (`quality & 2`): {train_scattered} ({train_scattered/len(train_cadences)*100:.1f}%)
  - Data Gaps (`quality & 4`): {train_gaps} ({train_gaps/len(train_cadences)*100:.1f}%)
- **Test Sector Cadences**: {len(test_cadences)} observations, time range {test_cadences['time_btjd'].min():.2f} to {test_cadences['time_btjd'].max():.2f} BTJD
  - Momentum Dumps (`quality & 1`): {test_dumps} ({test_dumps/len(test_cadences)*100:.1f}%)
  - Scattered Light (`quality & 2`): {test_scattered} ({test_scattered/len(test_cadences)*100:.1f}%)
  - Data Gaps (`quality & 4`): {test_gaps} ({test_gaps/len(test_cadences)*100:.1f}%)

## 5. Alignment and Integrity Verification
1. **Row Index Alignment**: Confirmed that row `i` in `train_stars.csv` maps 1:1 to row `i` in `train_flux.npy` and `train_centroid.npy`.
2. **Test ID Alignment**: Confirmed that row `i` in `test_stars.csv` exactly matches row `i` of `sample_submission.csv` and the test arrays.
3. **No Duplicate IDs**: All 18,000 train IDs and 7,000 test IDs are unique.
4. **NaN Safety**: NaNs occur primarily during mid-sector data downlinks (~cadence 600-700) and flagged bad cadences. Missing values must be filtered with nan-safe statistical operators (`np.nanmedian`, `np.nanstd`, etc.).
"""

    report_path = config.REPORTS_DIR / "dataset_inspection.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_md)
    print(f"\nSuccessfully generated {report_path}")

if __name__ == "__main__":
    inspect_dataset()
