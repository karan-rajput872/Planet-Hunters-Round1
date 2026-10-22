# 🎯 Planet Hunters: Technical Interview Preparation & Deep-Dive Guide
## Comprehensive Interview Q&A, Architectural Defenses & Design Decisions

This document prepares you for technical interviews, machine learning system design rounds, and recruiter discussions about the **Planet Hunters** project.

---

## 1. Project High-Level Pitch (30-Second Elevator Response)
> "In this project, I built an end-to-end machine learning system to classify 25,000 space telescope light curves into eight astronomical and instrumental categories. The main technical challenge was detecting rare, shallow exoplanetary transits ($< 1\%$ flux drops) in the presence of dominant stellar spot waves and detector jitter. I engineered 85 domain-specific features—including 1-day 2D median detrending and 2D centroid displacement vetting—and trained a 5-fold dual-architecture ensemble of LightGBM and HistGradientBoosting. The model achieved a verified **0.5915 Out-of-Fold Macro F1** across all 18,000 training stars with 100% bitwise reproducible inference."

---

## 2. Core Architectural & Methodological Defenses

### Q1: Why did you evaluate primarily with Macro F1 rather than Accuracy or Micro F1?
**Answer:**
In astronomical surveys, target classes are highly unbalanced. Quiet stars and starspots constitute ~36% of the dataset, while exoplanets (~11.9%), background binaries (~8.9%), and flares (~10.0%) are much rarer. Accuracy or Micro F1 would be heavily biased toward predicting quiet stars or pulsators, achieving a deceptively high score while missing the rare exoplanet transits. Macro F1 computes the unweighted arithmetic mean of F1-scores across all eight classes:
$$\text{Macro F1} = \frac{1}{8} \sum_{k=1}^8 F1_k$$
This forces the model to balance precision and recall equally across both majority and minority classes.

### Q2: Why did you choose a 5-Fold Stratified Cross-Validation scheme instead of a simple train/test split?
**Answer:**
With 18,000 training stars and 8 classes, a single holdout split is susceptible to variance in smaller classes like background binaries. 5-Fold Stratified CV ensures:
1. Every fold preserves the exact class proportions of the overall dataset.
2. 100% of the 18,000 training stars receive an out-of-fold prediction from an estimator that never saw that star during training.
3. We can measure model stability ($\sigma = \pm 0.0020$ across folds), confirming that our feature representations do not suffer from split-dependent instability.

### Q3: Why did you ensemble LightGBM with HistGradientBoosting rather than using a single model or Deep Learning?
**Answer:**
LightGBM and HistGradientBoosting employ complementary tree growth strategies:
- **LightGBM** uses *leaf-wise (best-first)* growth. It splits the leaf with maximum loss reduction, making it effective at isolating sharp, localized non-linear thresholds like transit dips.
- **HistGradientBoosting** uses *depth-wise symmetric* growth with histogram binning. It acts as a structural regularizer against LightGBM's tendency to overfit narrow leaf pathways.
A probability blend of **75% LightGBM + 25% HistGradientBoosting** consistently outperformed both individual models across all 5 cross-validation folds. While 1D CNNs or Transformers are possible, gradient boosted trees on 85 domain-informed features train in ~78 seconds on CPU, offer full interpretability, and match or exceed deep learning benchmarks on tabular time-series features.

### Q4: Why did you test and subsequently reject Semi-Supervised Pseudo-Labeling?
**Answer:**
In Phase 2, I tested pseudo-labeling by assigning predicted labels to high-confidence test stars ($P > 0.85$) and appending them to the training set. It was firmly rejected because of **confirmation bias and negative transfer**:
- High confidence was overwhelmingly concentrated on easy, high-amplitude classes: 68% of pseudo-labels were `pulsating_star` or `instrument_glitch`.
- Only 2.1% were `planet` or `background_binary`.
- Retraining on this skewed distribution degraded validation Macro F1 from **0.5916 down to 0.5894**. Rejecting pseudo-labeling preserved the integrity of our decision boundaries.

### Q5: How did you investigate and guard against Domain Shift between Train and Test sectors?
**Answer:**
The test stars originate from a distinct space telescope observing sector. I used a two-pronged approach:
1. **Statistical Population Verification:** Performed two-sample Kolmogorov-Smirnov (KS) tests on stellar metadata ($T_{\text{eff}}, \log g, R_\star, T_{\text{mag}}, \text{contamination}$). All KS statistics were $\le 0.0102$ ($p > 0.7$), proving the underlying stellar population is identical.
2. **Domain-Invariant Features:** Instrumental sensor noise floors differ across sectors. Instead of raw flux scatter, I engineered scale-free percentile spreads: $(p_{99} - p_{75})/\text{IQR}$ and $(p_{25} - p_{01})/\text{IQR}$, which measure tail asymmetry invariant to overall sensor noise amplitude.
3. **Hardware Shortcut Exclusion:** I strictly omitted `camera` and `ccd` identifiers from the predictor set so the model could not memorize detector-specific noise patterns.

### Q6: How did you ensure zero Data Leakage in the feature pipeline?
**Answer:**
Data leakage can happen through target contamination or cross-sample contamination:
- **Target Leakage:** The feature engineering function `compute_batch_features()` does not take target labels `y`; it operates purely unsupervised on raw flux, centroids, and stellar parameters.
- **Cross-Sample Contamination:** All time-series operations (median detrending, percentiles, FFTs) operate strictly along `axis=1` (the 1,315 cadences). 2D median filtering uses `size=(1, 49)`, which filters strictly along time for each star independently without adjacent row blending.
- **Validation Isolation:** Features were extracted identically for both train and test without fitting global dataset-level scalers.

### Q7: What was the single most impactful feature you engineered, and why?
**Answer:**
The **Detrended Dip SNR** (`detrend_dip_snr`), defined as $-\text{Percentile}(f_{\text{detrended}}, 1\%) / \text{MAD}(f_{\text{detrended}})$.
In raw starlight, shallow planetary transits are masked by large stellar rotation waves caused by starspots. By applying a 1-day rolling median filter, we strip away the rotational wave and compute the dip depth relative to the high-frequency residual noise. Ablation testing proved that removing this feature dropped `planet` F1 from **0.4679 to 0.3776** (-0.0903) and reduced overall Macro F1 by **-0.0245**.

### Q8: How did you distinguish bona fide Exoplanets from Background Blended Binaries?
**Answer:**
Using **astrometric centroid displacement during dips** (`cen_shift_in_dip`). When an exoplanet transits the target star, the flux drops but the center-of-light (centroid) of the star does not move ($\Delta \text{centroid} \approx 0$). In contrast, when an unresolved background eclipsing binary in the same pixel aperture undergoes an eclipse, the center-of-light shifts toward the primary star. Comparing the mean centroid position during dips ($f < p_{05}$) against out-of-dip baseline ($p_{25} \le f \le p_{75}$) allows the model to cleanly separate background binaries from genuine planets.

### Q9: How did you ensure 100% Reproducibility in inference?
**Answer:**
I implemented three strict engineering controls:
1. Fixed global random seeds (`RANDOM_SEED = 42`) across all cross-validation splits and tree estimators.
2. Verified class array alignment: all models store identical sorted alphabetical class orders (`model.classes_`).
3. Built an automated CLI interface (`generate_submission.py --model champion --output <path>`) and regression unit test that validates that 7,000 out of 7,000 predictions match `submission_FINAL.csv` bitwise.

### Q10: What are the primary limitations of the current solution, and what would you improve next?
**Answer:**
The main limitation is confusion between `quiet_star` and low-amplitude `starspots`. On faint red dwarfs ($T_{\text{mag}} > 14$), low-amplitude spot modulations ($< 0.2\%$ flux change) approach the photon shot noise floor. If given more time, I would:
1. Implement Lomb-Scargle periodogram peak power with False Alarm Probability (FAP) thresholds to distinguish true rotational periodicity from white noise.
2. Train a lightweight 1D ResNet directly on raw lightcurves and ensemble its probability outputs with the gradient boosted trees.
