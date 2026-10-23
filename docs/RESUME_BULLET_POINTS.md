# 📄 Resume Ready Bullet Points & Technical Impact Statements
## Project: Planet Hunters — Find New Worlds in Starlight (Hack4Hack 2026)

---

## 1. One Concise Resume Bullet (Single-Line Impact)
- Engineered an end-to-end time-series classification system on 25,000 stellar lightcurves, combining 88 cotrended astrophysical features with a tri-architecture LightGBM/HistGB/CatBoost ensemble to achieve **0.6455 OOF Macro F1** and **0.6336 out-of-detector generalization** across 8 classes with 100% bitwise reproducible inference.

---

## 2. Two Detailed Technical Bullets (For ML / Data Science Roles)
- **Time-Series Feature Engineering & Astronomical Signal Processing:** Designed and vectorized 88 domain-informed features across 1,315-cadence space telescope lightcurves—implementing camera/CCD common-trend cotrending that reduced train/test distribution drift by 60.3%, alongside transit dip SNR, 2D centroid displacement vetting, and flare rise-decay asymmetry—driving an out-of-detector generalization gain of **+0.1175 Macro F1** (0.5161 $\rightarrow$ 0.6336).
- **Tri-Architecture Ensembling & Production Validation:** Built a 5-fold stratified cross-validation ensemble blending leaf-wise LightGBM, depth-wise HistGradientBoosting, and CatBoost oblivious trees (50/40/10 blend), achieving **0.6455 OOF Macro F1** and implemented an automated 14-point schema validator guaranteeing 100% deterministic test predictions.

---

## 3. Compact Project Description (For Resume "Projects" Section)
**Planet Hunters — Autonomous Stellar Lightcurve Classification | Python, SciPy, LightGBM, CatBoost, Scikit-learn**
- Developed a multiclass machine learning pipeline to classify 25,000 space telescope lightcurves into 8 astrophysical phenomena (exoplanets, eclipsing binaries, starspots, pulsators, flares, glitches, quiet stars).
- Extracted 88 statistical, Fourier, and astrometric centroid features; implemented Camera/CCD cotrending to eliminate detector-level thermal and pointing systematics.
- Deployed a 5-fold tri-architecture gradient boosted tree ensemble yielding **0.6455 Out-of-Fold Macro F1** and **0.6336 Out-of-Detector Generalization**, outperforming baseline models by +22.8% relative gain.
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
