# 📄 Resume Ready Bullet Points & Technical Impact Statements
## Project: Planet Hunters — Find New Worlds in Starlight (Hack4Hack 2026)

---

## 1. One Concise Resume Bullet (Single-Line Impact)
- Engineered an end-to-end time-series classification system on 25,000 stellar lightcurves, combining 85 astrophysical features with a dual-architecture LightGBM/HistGB ensemble to achieve **0.5915 OOF Macro F1** across 8 classes with 100% bitwise reproducible inference.

---

## 2. Two Detailed Technical Bullets (For ML / Data Science Roles)
- **Time-Series Feature Engineering & Signal Processing:** Designed and vectorized 85 domain-informed features across 1,315-cadence space telescope lightcurves—including 1-day 2D median detrending, transit dip SNR, 2D centroid displacement vetting, and flare rise-decay asymmetry—improving exoplanet F1 by **+0.0903** and overall validation Macro F1 by **+0.0245**.
- **Dual-Architecture Ensembling & Production Validation:** Built a 5-fold stratified cross-validation ensemble blending leaf-wise LightGBM (63 leaves) and depth-wise HistGradientBoosting (450 trees) with 0.75/0.25 probability weighting, achieving **0.5915 OOF Macro F1** (Holdout: **0.5956**) and implemented an automated 14-point schema validator guaranteeing 100% deterministic test predictions.

---

## 3. Compact Project Description (For Resume "Projects" Section)
**Planet Hunters — Autonomous Stellar Lightcurve Classification | Python, SciPy, LightGBM, Scikit-learn**
- Developed a multiclass machine learning pipeline to classify 25,000 space telescope lightcurves into 8 astrophysical phenomena (exoplanets, eclipsing binaries, starspots, pulsators, flares, glitches, quiet stars).
- Extracted 85 statistical, Fourier, and astrometric centroid features; implemented 1-day median filtering to isolate subtle transits from high-amplitude stellar spot modulations.
- Deployed a 5-fold dual-architecture gradient boosted tree ensemble yielding **0.5915 Out-of-Fold Macro F1**, outperforming baseline models by +7.0% relative gain.
- Packaged complete repository with automated unit tests, strict submission validation, and reproducible CLI inference.

---

## 4. Key Skills & Competencies Demonstrated

| Skill Category | Specific Competencies Demonstrated |
|:---|:---|
| **Machine Learning** | Multiclass classification, Macro F1 optimization, heterogeneous tree ensembling, probability calibration, class weighting, feature ablation. |
| **Signal Processing & Time-Series** | Photometric normalization, 2D median filter detrending, Fourier power spectrum analysis (FFT), autocorrelation, Von Neumann ratios, transit dip detection. |
| **Data Engineering & Architecture** | Memory-mapped NumPy arrays, compressed Parquet caching via PyArrow, zero-leakage feature pipelines, modular code organization. |
| **Software Quality & Testing** | Python `unittest`, automated regression testing, deterministic random seeds, defensive programming against division by zero, schema validation. |
| **Tools & Libraries** | Python 3.11, LightGBM, Scikit-learn, SciPy, NumPy, Pandas, Matplotlib, Seaborn, PyArrow. |
