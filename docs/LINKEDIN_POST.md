# 📢 LinkedIn Announcement Post

```markdown
🚀 Excited to share my latest machine learning project: Planet Hunters — Autonomous Stellar Lightcurve Classification for the ML Challenge Hack4Hack 2026 (Round 1)! 🪐✨

Detecting rare exoplanetary transits in space telescope photometry is a classic needle-in-a-haystack challenge. Shallow planetary transits (< 1% flux attenuation) are easily obscured by stellar rotation waves, acoustic pulsations, flares, or confused with eclipsing binaries and thruster glitches.

To solve this 8-class time-series classification problem across 25,000 stars (18k train, 7k test; 1,315 cadences per star), I built an end-to-end, scientifically grounded ML pipeline:

🔬 Key Engineering Highlights:
• Astronomical Feature Engineering: Extracted 85 domain-informed features across 8 modules—including 1-day 2D median detrending to strip out stellar rotation, transit dip SNR, 2D centroid displacement vetting (to flag background blended binaries), and flare rise-decay asymmetry.
• Sector-Invariant Ratios: Designed scale-free percentile spreads to protect models against domain shifts in sensor noise between observing sectors.
• Dual-Architecture Ensembling: Blended leaf-wise LightGBM (for acute transit thresholds) with depth-wise HistGradientBoosting (for smooth boundary regularization) across a 5-fold stratified cross-validation scheme (75% / 25% probability weighting).
• Strict Production Standards: Implemented a 14-point automated CSV validator and regression test suite, achieving 100% bitwise reproducible inference on test predictions.

📈 Verified Validation Results:
• 5-Fold Out-of-Fold Macro F1: 0.5915 across all 18,000 training stars
• Stratified Holdout Macro F1: 0.5956
• Substantial gains on difficult classes: Planet F1 reached 0.4679 (up from 0.3776 without detrending) and Eclipsing Binary F1 reached 0.7303.

Check out the full open-source codebase, technical reports, and diagnostic plots in the repository below! 👇

#MachineLearning #DataScience #Astronomy #TimeSeries #Python #LightGBM #ScikitLearn #FeatureEngineering #Exoplanets #Hack4Hack #OpenSource
```
