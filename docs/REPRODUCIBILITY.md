# 🔁 Planet Hunters — End-to-End Reproducibility Guide
## Exact Replication Instructions for Evaluators and Developers

**Project:** Planet Hunters — Find New Worlds in Starlight
**Competition:** ML Challenge Hack4Hack 2026 | Round 1
**Reproducibility Certification:** 100.0000% Bitwise Verified

---

## 1. System Requirements & Runtime Environment

- **Operating System:** Windows 10/11, Ubuntu 20.04+, or macOS (tested on Windows 11).
- **Python Version:** **Python 3.11+** (tested on Python 3.11.9).
- **RAM:** Minimum 8 GB (16 GB recommended for feature extraction).
- **Disk Space:** ~1.5 GB for raw data, processed parquets, and model binaries.
- **Hardware Acceleration:** GPU is NOT required. All models are optimized for multi-core CPU inference (`n_jobs=-1`).

---

## 2. Environment Setup

### Option A: Windows (PowerShell)
```powershell
# 1. Clone repository
git clone https://github.com/username/Planet-Hunters-Round1.git
cd Planet-Hunters-Round1

# 2. Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Install audited dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Option B: Linux / macOS (Bash)
```bash
# 1. Clone repository
git clone https://github.com/username/Planet-Hunters-Round1.git
cd Planet-Hunters-Round1

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 3. Data Placement Directory Structure

Raw competition data must be placed in `data/raw/` (read-only):

```
data/raw/
├── train_flux.npy         # (18000, 1315) float32
├── train_centroid.npy     # (18000, 2, 1315) float32
├── train_stars.csv        # 18,000 rows
├── train_cadences.csv     # 1,315 cadences
├── test_flux.npy          # (7000, 1315) float32
├── test_centroid.npy      # (7000, 2, 1315) float32
├── test_stars.csv         # 7,000 rows
└── test_cadences.csv      # 1,315 cadences
```

---

## 4. Deterministic Seed Configuration

All stochastic operations use fixed global seed `42` managed via `src/config.py`:
```python
RANDOM_SEED = 42
```
Cross-validation folds use deterministic progression: `random_state = config.RANDOM_SEED + fold * 10`.

---

## 5. Quick Verification: Replicate Champion Predictions in 6 Seconds

If the pre-trained champion artifacts exist in `models/tuned_cv_models/` and cached features exist in `data/processed/`, you can regenerate predictions immediately without retraining:

```powershell
python generate_submission.py --model champion --output submissions/submission_FINAL.csv
```

### Expected Console Output:
```
=================================================================
GENERATING COMPETITION SUBMISSION (Model Choice: champion)
=================================================================
[CACHE] Loading cached features from .../data/processed...
[CACHE] Loaded train: (18000, 85), test: (7000, 85)
Loaded test features: (7000, 85)
Loaded test stars:    (7000, 8)
[MODEL] Loading 5-Fold Dual-Architecture Champion Ensemble...
  Predicting fold 1/5: LightGBM + HistGradientBoosting...
  Predicting fold 2/5: LightGBM + HistGradientBoosting...
  Predicting fold 3/5: LightGBM + HistGradientBoosting...
  Predicting fold 4/5: LightGBM + HistGradientBoosting...
  Predicting fold 5/5: LightGBM + HistGradientBoosting...

[SAVE] Successfully written submission to: submissions/submission_FINAL.csv
[PASS] All 14 structural, schema, and astrophysical checks passed!
[SUCCESS] Final submission created and validated successfully!
```

---

## 6. Validate the Generated Submission

Run the strict automated submission validator:
```powershell
python validate_submission.py submissions/submission_FINAL.csv
```
**Expected Exit Code:** `0` (Success).

---

## 7. Run Automated Regression Test Suite

Run all unit tests:
```powershell
python -m unittest tests/test_pipeline.py
```
**Expected Output:**
```
........
----------------------------------------------------------------------
Ran 8 tests in ~0.5s

OK
```

---

## 8. Full Retraining from Scratch (Optional)

To wipe the cached features and re-execute the entire pipeline end-to-end:

```powershell
# 1. Force re-extraction of all 85 features (~2.5 minutes on CPU)
python src/feature_engineering.py

# 2. Retrain 5-fold dual-architecture ensemble (~78 seconds on CPU)
python src/train_v3_dual_ensemble.py

# 3. Validate newly generated predictions
python validate_submission.py submissions/submission_FINAL.csv
```

---

## 9. Troubleshooting

| Symptom | Cause | Solution |
|:---|:---|:---|
| `ImportError: Unable to find a usable engine; 'pyarrow' or 'fastparquet'` | Missing parquet driver | Run `pip install pyarrow>=14.0.0` |
| `FileNotFoundError: No trained model found` | Missing models folder | Ensure `models/tuned_cv_models/` is present or run `python src/train_v3_dual_ensemble.py` |
| `MemoryError during feature extraction` | RAM exhausted | Reduce `batch_size=500` in `extract_all_features()` in `src/feature_engineering.py` |
| `KeyError: 'camera'` | Hardware column accessed | Camera and CCD columns are explicitly excluded; ensure feature extraction code is unmodified |
