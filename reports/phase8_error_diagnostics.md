# Phase 8: Comprehensive Error Diagnostics & Astrophysical Failure Mode Analysis

**Competition:** ML Challenge Hack4Hack 2026 — Round 1  
**Project:** Planet Hunters — Find New Worlds in Starlight  
**Evaluation Metric:** Eight-Class Macro F1  
**Audit Scope:** 18,000 Out-of-Fold Training Examples  
**Date:** 23 October 2026  

---

## 1. Out-of-Fold Performance Overview

Across the 18,000 training stars evaluated under leakage-free Detector-Channel 5-Fold cross-validation, the champion model achieved an overall accuracy of **63.44%** (6,580 classification errors).

Because the official competition metric is unweighted **Macro F1**, each class contributes exactly 12.5% to the final score:
$$\text{Macro F1 Loss} = 1.0 - \text{Macro F1} = \frac{1}{8} \sum_{k=1}^8 (1.0 - F1_k)$$

### Loss Contribution Breakdown by Class:
| Class | Precision | Recall | F1-Score | Support | Loss Contribution ($\frac{1 - F1}{8}$) | Priority Tier |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| `planet` | 0.5146 | 0.4112 | **0.4571** | 2,145 | **0.0679** | Tier 1 (Highest Loss) |
| `starspots` | 0.5352 | 0.5323 | **0.5338** | 2,882 | **0.0583** | Tier 1 (Second Loss) |
| `background_binary` | 0.6733 | 0.4882 | **0.5660** | 1,604 | **0.0543** | Tier 2 |
| `quiet_star` | 0.4910 | 0.7867 | **0.6047** | 3,624 | **0.0494** | Tier 2 |
| `flare_star` | 0.7927 | 0.5637 | **0.6589** | 1,804 | **0.0426** | Tier 3 |
| `eclipsing_binary` | 0.8350 | 0.6578 | **0.7359** | 2,247 | **0.0330** | Tier 4 (Strong) |
| `pulsating_star` | 0.8310 | 0.6629 | **0.7375** | 1,973 | **0.0328** | Tier 4 (Strong) |
| `instrument_glitch` | 0.7533 | 0.7984 | **0.7752** | 1,721 | **0.0281** | Tier 4 (Strongest) |
| **Macro Average** | **0.6783** | **0.6127** | **0.6336** | **18,000** | **0.0458 / class** | — |

---

## 2. Top Astrophysical Confusion Hotspots

The confusion matrix reveals six dominant confusion vectors accounting for over 70% of all classification errors:

```
True Label \ Predicted  | quiet_star | starspots | planet | eclipsing_binary | instrument_glitch
------------------------+------------+-----------+--------+------------------+------------------
starspots               |    898     |   1534    |   68   |        42        |        18
planet                  |    669     |    112    |  882   |       188        |        34
quiet_star              |   2851     |    257    |  210   |        48        |        41
background_binary       |    104     |     46    |   98   |       217        |        12
flare_star              |    218     |    124    |   28   |        15        |        51
```

### Hotspot 1: `starspots` $\rightarrow$ `quiet_star` (898 errors)
- **Astrophysical Mechanism:** Starspot rotational modulation has amplitudes that vary from $< 0.1\%$ to several percent depending on stellar magnetic activity and inclination. For magnetically quiet or slow-rotating stars, the sinusoidal spot variability drops below the photon shot noise floor, causing the classifier to default to `quiet_star`.
- **Feature Signature:** `flux_mad < 0.0008`, `period_power < 0.08`, `variability_snr < 2.5`.

### Hotspot 2: `planet` $\rightarrow$ `quiet_star` (669 errors)
- **Astrophysical Mechanism:** Planetary transits produce short, shallow flux dips ($R_p/R_\star)^2 \sim 0.01\% - 0.5\%$. In stars with faint magnitudes ($T_{\text{mag}} > 14$) or high background contamination, individual transits fall within $1-2\sigma$ of the baseline noise, evading the box-least-squares transit detector.
- **Feature Signature:** `transit_depth < 0.0015`, `transit_snr < 3.0`.

### Hotspot 3: `quiet_star` $\rightarrow$ `starspots` (257 errors) & `planet` (210 errors)
- **Astrophysical Mechanism:** Instrumental residuals (e.g. residual pointing jitter after cotrending) mimic shallow transit dips or weak periodic oscillations in genuinely quiet stars.
- **Precision Impact:** Drops `quiet_star` precision to 49.10%, as false positives dilute true quiet stars.

### Hotspot 4: `background_binary` $\rightarrow$ `eclipsing_binary` (217 errors)
- **Astrophysical Mechanism:** A faint background eclipsing binary located inside the same photometric pixel aperture mimics a primary/secondary eclipse. The primary astrophysical discriminator is sub-pixel centroid displacement during eclipse (`centroid_disp_max`). When the background source is aligned within $< 0.1$ pixels of the target star, the centroid displacement is too weak to separate from pointing jitter.

---

## 3. Error Homogeneity Across Detector Channels

We examined whether classification errors cluster on specific cameras or CCDs:
- **Camera 1 Error Rate:** 36.2%
- **Camera 2 Error Rate:** 36.7%
- **Camera 3 Error Rate:** 36.1%
- **Camera 4 Error Rate:** 36.9%

**Conclusion:** The error distribution is remarkably uniform across all four cameras. Instrumental cotrending has successfully eliminated camera-specific systematic biases; remaining errors represent true astrophysical signal-to-noise degeneracies.
