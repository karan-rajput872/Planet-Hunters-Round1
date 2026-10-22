# 🪐 Planet Hunters — Mission Control Dashboard

**Competition:** ML Challenge Hack4Hack 2026 — Round 1
**Project:** Planet Hunters — Find New Worlds in Starlight
**Dashboard Platform:** Streamlit + Plotly + Vanilla Modern Dark Observatory CSS
**Target Submission:** `submissions/submission_FINAL.csv` (7,000 test stars, 14/14 checks verified)

---

## 🚀 Quick Launch (Windows)

You can launch the dashboard with a single click or command:

### Option A: Via PowerShell (Recommended)
Right-click `START_DASHBOARD.ps1` and select **Run with PowerShell**, or execute:
```powershell
.\START_DASHBOARD.ps1
```

### Option B: Via Windows Command Prompt / Batch
Double-click `START_DASHBOARD.bat` or run:
```cmd
START_DASHBOARD.bat
```

### Option C: Direct Command Line
From the project root:
```powershell
& .\.venv\Scripts\python.exe -m streamlit run dashboard/app.py --server.port 8501
```

Once started, the dashboard automatically opens in your default web browser at:
**`http://localhost:8501`**

---

## 🛠️ Port Conflict Troubleshooting

If port `8501` is already in use by another application on your machine:
```powershell
# Launch on an alternative port (e.g. 8502 or 8505)
& .\.venv\Scripts\python.exe -m streamlit run dashboard/app.py --server.port 8502
```

---

## 🏛️ Dashboard Structure & Features

The Mission Control Dashboard provides eight presentation-ready stations:

1. **Mission Overview (Hero)**
   - High-level telemetry badges (`LOCAL VALIDATION PASSED`, `14/14 CHECKS`).
   - Fundamental dimensions: 18,000 labelled training stars, 7,000 test targets, 1,315 flux cadences per star, 8 multi-class categories.
   - Official metric definition: Unweighted Macro F1.

2. **Performance Intelligence**
   - Verified offline validation metric cards:
     - Champion OOF Macro F1: `0.5915`
     - 5-Fold Mean Macro F1: `0.5914`
     - 5-Fold Standard Deviation: `±0.0020`
     - Champion Holdout Macro F1: `0.5956`
   - Interactive Plotly model benchmark progression comparing ExtraTrees (0.5234), CatBoost (0.5512), HistGradientBoosting (0.5709), LightGBM (0.5914), and Champion Dual Ensemble (0.5956).

3. **Classification Intelligence**
   - Interactive horizontal bar chart and donut chart of exact class distributions:
     - `pulsating_star`: 1,904 stars (27.2%)
     - `instrument_glitch`: 1,372 stars (19.6%)
     - `quiet_star`: 926 stars (13.2%)
     - `starspots`: 827 stars (11.8%)
     - `eclipsing_binary`: 687 stars (9.8%)
     - `planet`: 516 stars (7.4%)
     - `flare_star`: 471 stars (6.7%)
     - `background_binary`: 297 stars (4.2%)
     - **Total:** 7,000 stars
   - Phenomenological descriptions and astrophysical taxonomic reference cards.

4. **Model Architecture & Ensemble Flow**
   - 4-stage prediction pipeline diagram (Stellar Inputs → Feature Extraction → Dual Weighted Ensemble → Calibrated Output).
   - Ensemble weighting formula: `P_final = 0.75 · P_lgb + 0.25 · P_hgb`.
   - Access to full high-resolution pipeline architectural schematic.

5. **Scientific Feature Exploration**
   - Feature engineering principles: Photometric variability (MAD, Skewness, Kurtosis), BLS transit search, Centroid shift astrometry in-dip vs out-of-dip, and asymmetric flare decay.
   - Interactive Phenomenological Lightcurve Explorer demonstrating simulated physics profiles and extracted features.

6. **Submission Verification Center**
   - Live integration with `src.submission_validation.validate_submission`.
   - Real-time **"Execute Live Validator Check"** button.
   - 14/14 automated check breakdown with passing badges.
   - Target candidate verification (`submission_FINAL.csv`, 7,000 rows, 2 columns, zero nulls/duplicates).

7. **Prediction Explorer**
   - Real-time star ID search.
   - Dropdown filter by predicted astrophysical class.
   - Multi-column sorting (ID ascending/descending, label).
   - Configurable pagination (25, 50, 100 rows per page).
   - Safe CSV subset export button (`Download Filtered Subset`).

8. **Project Information & Documentation Hub**
   - Official Hack4Hack 2026 specifications.
   - Complete technical stack summary.
   - Direct clickable references to all repository markdown documentation (`PROJECT_OVERVIEW.md`, `TECHNICAL_REPORT.md`, `COMPETITION_SUBMISSION_GUIDE.md`, etc.).

---

## 🔒 Critical Safety & Integrity Controls

- **Read-Only Access:** The dashboard only reads `submissions/submission_FINAL.csv`. It never modifies or overwrites the file.
- **Offline Self-Contained:** Runs entirely from local Python environment without external cloud dependencies.
- **Zero Retraining:** Reads pre-trained model artifacts and pre-computed validation logs.
- **Scientific Accuracy:** Accurately labels validation metrics as internal offline scores, never claiming confirmed exoplanets or fabricated leaderboard scores.
