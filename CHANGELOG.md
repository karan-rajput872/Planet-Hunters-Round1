# 📜 Changelog
All notable development milestones, architectural improvements, and audit corrections for the **Planet Hunters** project are documented in this file.

---

## [UI Redesign: Scientific Intelligence Platform] — 2026-10-22

### Added
- **Scientific Intelligence Design System**: Replaced heavy neon cyber aesthetic with an Enterprise SaaS Scientific Research Platform design (Light theme default `#F5F7FA`, `#FFFFFF` surfaces, `#2457D6` royal blue, `#172033` primary text).
- **Dual-Theme Engine**: Added an interactive Light / Dark theme toggle in the sidebar with curated color systems and theme-adaptive Plotly figures.
- **Robust Text Overflow Defenses**: Resolved all letter and label escapes across cards, tables, flex headers, and metric containers using strict `box-sizing: border-box`, `min-width: 0`, and smart word breaking.
- **Redesigned Dashboard Stations**: Overhauled all 8 sections (Mission Overview, Performance Intelligence, Classification Intelligence, Model Architecture, Scientific Features, Submission Verification, Prediction Explorer, Documentation Hub).
- **Hardened Windows Launchers**: Implemented native PowerShell (`START_DASHBOARD.ps1`) and Batch (`START_DASHBOARD.bat`) with automated project root detection, dependency verification via `importlib`, and automatic port conflict fallback (8501 -> 8502).

---

## [Final Release: Competition & Portfolio Ready] — 2026-10-22

### Added
- **`submissions/submission_FINAL.csv`**: Created the final verified competition submission candidate (100% bitwise identical to champion `submission_v3.csv`).
- **`validate_submission.py`**: Standalone root validation script checking all 14 schema, format, and astrophysical constraints with clean terminal reporting and exit codes.
- **Visual Assets**: Generated 7 publication-quality figures in `assets/architecture/` and `assets/plots/` (system architecture, benchmark progression, class-wise F1, cross-validation stability, feature ablation, prediction distribution, and normalized confusion matrix).
- **Career & Portfolio Materials**: Added `docs/PROJECT_OVERVIEW.md`, `docs/RESUME_BULLET_POINTS.md`, `docs/LINKEDIN_POST.md`, and `docs/PROJECT_INTERVIEW_PREPARATION.md`.
- **Engineering Documentation**: Added `docs/COMPETITION_SUBMISSION_GUIDE.md`, `docs/TECHNICAL_REPORT.md`, `docs/MODEL_EVALUATION.md`, `docs/REPRODUCIBILITY.md`, and `docs/FINAL_HANDOVER.md`.
- **Licensing & Metadata**: Added `LICENSE_STATUS.md`, `pyproject.toml`, and `.gitattributes`.
- **Packaging**: Created `dist/Planet-Hunters-Round1-Portfolio-Ready.zip` and `dist/ARCHIVE_CONTENTS.md`.

### Fixed
- **CLI Inference Overwrite Hazard**: Refactored `generate_submission.py` to support `--model champion` and custom `--output` paths, preventing silent overwriting of previous candidates.
- **Function Signature Mismatch**: Corrected `train.py` invocation of `generate_submission()` to pass `model_choice="champion"`.
- **Dependency Incompleteness**: Added `pyarrow>=14.0.0` and `tabulate>=0.9.0` to `requirements.txt`.
- **Testing Coverage**: Hardened `tests/test_pipeline.py` with explicit boolean assertions and bitwise identity checks (8/8 tests passing).
- **Git Security**: Hardened `.gitignore` to prevent committing large raw competition arrays (~400MB) or backup checkpoints.

---

## [Phase 3: Dual-Architecture Ensembling] — 2026-10-22

### Added
- **Dual-Architecture Ensemble**: Combined leaf-wise LightGBM (63 leaves) and depth-wise HistGradientBoosting (450 iterations) with a 75/25 probability blend.
- **Evaluation Benchmark**: Reached peak Holdout Macro F1 of **0.5956** and 5-Fold OOF Macro F1 of **0.5915**.
- **Model Persistence**: Serialized all 10 trained fold models to `models/tuned_cv_models/`.
- **Candidate `submission_v3.csv`**: Generated champion submission with high `planet` F1 (0.4679) and `starspots` F1 (0.4560).
- **Feature Ablation Study**: Empirically proved that 1-day rolling median detrending contributes +0.0245 Macro F1 (+0.0903 on planets).

---

## [Phase 2: Cross-Validation & Domain Shift Analysis] — 2026-10-22

### Added
- **5-Fold Stratified Cross-Validation**: Established leak-free, fold-level performance tracking (mean: 0.5889 ± 0.0017, OOF: 0.5890).
- **Candidate `submission_v2.csv`**: Generated 5-fold bagged LightGBM submission.
- **Cross-Sector Shift Analysis**: Conducted two-sample Kolmogorov-Smirnov tests comparing train vs. test observing sectors, proving stellar population identity ($\text{KS} \le 0.0102$).

### Tested & Rejected
- **Semi-Supervised Pseudo-Labeling**: Tested pseudo-labeling on confident test stars ($P > 0.85$). Rejected due to confirmation bias: pseudo-labels were 68% concentrated on easy pulsators/glitches and degraded validation Macro F1 from 0.5916 to 0.5894.

---

## [Phase 1: Pipeline Foundation & Feature Engineering] — 2026-10-22

### Added
- **Modular Codebase**: Established `src/` modular architecture (`config.py`, `data_loader.py`, `preprocessing.py`, `feature_engineering.py`, `model_training.py`, `model_evaluation.py`).
- **85 Vectorized Astronomical Features**: Implemented flux statistics, 2D centroid displacement in transit dips, stellar flare rise/decay asymmetry, Von Neumann ratios, and FFT frequency metrics.
- **Model Benchmarking**: Evaluated ExtraTrees (0.5234), CatBoost (0.5512), HistGB (0.5709), and LightGBM (0.5914).
- **Baseline Candidate `submission.csv`**: Generated initial competition submission using the best single LightGBM model.
