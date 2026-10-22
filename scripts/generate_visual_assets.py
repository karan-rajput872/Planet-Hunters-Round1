"""
Generates publication-quality visual assets for README, documentation, and portfolio.
All figures are created using Matplotlib and Seaborn with clean astronomy/dark-themed palettes.
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import joblib
from sklearn.model_selection import StratifiedKFold

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src import config
from src.data_loader import load_stars_metadata

# Style configuration
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial', 'DejaVu Sans', 'Helvetica'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

arch_dir = Path("assets/architecture")
plots_dir = Path("assets/plots")
arch_dir.mkdir(parents=True, exist_ok=True)
plots_dir.mkdir(parents=True, exist_ok=True)

# ==============================================================================
# 1. assets/architecture/project_architecture.png
# ==============================================================================
print("[PLOTS] 1/7 Generating project architecture diagram...")
fig, ax = plt.subplots(figsize=(13, 7), dpi=300)
ax.axis("off")

boxes = [
    {"title": "1. RAW DATASETS", "desc": "18k Train / 7k Test\nFlux (N, 1315)\nCentroids (N, 2, 1315)\nStellar Meta (Tmag, Teff...)", "xy": (0.02, 0.55), "wh": (0.17, 0.35), "color": "#e3f2fd", "border": "#1976d2"},
    {"title": "2. PREPROCESSING", "desc": "Per-Star Relative Flux\n(f / median(f)) - 1.0\nCentroid Centering\nQuality Bitmasking", "xy": (0.22, 0.55), "wh": (0.17, 0.35), "color": "#e8f5e9", "border": "#388e3c"},
    {"title": "3. 85 DOMAIN FEATURES", "desc": "1-Day 2D Median Detrending\nDetrended Dip SNR (Exoplanets)\nCentroid Shift in Dip (BGs)\nFlare Asymmetry & FFTs", "xy": (0.42, 0.55), "wh": (0.18, 0.35), "color": "#fff3e0", "border": "#f57c00"},
    {"title": "4. DUAL 5-FOLD ENSEMBLE", "desc": "5-Fold Stratified CV (Seed 42)\n75% LightGBM (63 leaves)\n25% HistGradientBoosting\nBalanced Class Weights", "xy": (0.63, 0.55), "wh": (0.18, 0.35), "color": "#f3e5f5", "border": "#7b1fa2"},
    {"title": "5. VERIFIED SUBMISSION", "desc": "submission_FINAL.csv\n7,000 Rows | id,label\n14-Point Strict Validator\n100% Bitwise Reproducible", "xy": (0.84, 0.55), "wh": (0.15, 0.35), "color": "#ffebee", "border": "#d32f2f"}
]

from matplotlib.patches import FancyBboxPatch

for b in boxes:
    rect = FancyBboxPatch(b["xy"], b["wh"][0], b["wh"][1], facecolor=b["color"], edgecolor=b["border"], linewidth=2, transform=ax.transAxes, zorder=2, boxstyle="round,pad=0.01")
    ax.add_patch(rect)
    ax.text(b["xy"][0] + b["wh"][0]/2, b["xy"][1] + b["wh"][1] - 0.06, b["title"], ha="center", va="center", fontsize=11, fontweight="bold", color=b["border"], transform=ax.transAxes)
    ax.text(b["xy"][0] + b["wh"][0]/2, b["xy"][1] + b["wh"][1]/2 - 0.03, b["desc"], ha="center", va="center", fontsize=9.5, color="#333333", transform=ax.transAxes)

# Connect with arrows
arrow_props = dict(facecolor="#555555", edgecolor="#555555", width=2, headwidth=8, shrink=0.05)
for i in range(len(boxes) - 1):
    x_start = boxes[i]["xy"][0] + boxes[i]["wh"][0]
    x_end = boxes[i+1]["xy"][0]
    y_mid = boxes[i]["xy"][1] + boxes[i]["wh"][1]/2
    ax.annotate("", xy=(x_end, y_mid), xytext=(x_start, y_mid), arrowprops=arrow_props, xycoords="axes fraction")

# Lower Summary Box
sum_rect = FancyBboxPatch((0.02, 0.08), 0.97, 0.36, facecolor="#fafafa", edgecolor="#9e9e9e", linewidth=1.5, transform=ax.transAxes, zorder=2, boxstyle="round,pad=0.01")
ax.add_patch(sum_rect)
ax.text(0.5, 0.38, "KEY ARCHITECTURAL HIGHLIGHTS & RIGOROUS CONTROLS", ha="center", va="center", fontsize=11, fontweight="bold", color="#37474f", transform=ax.transAxes)

summary_text = (
    "• Per-Star Time-Series Independence: All time-series operations (detrending, percentiles, FFTs) operate strictly along axis=1 with ZERO cross-sample leakage.\n"
    "• Observing Shortcut Exclusion: Camera and CCD hardware identifiers are explicitly dropped from features to prevent sector-specific noise overfitting.\n"
    "• Structural Model Diversity: Combines leaf-wise tree growth (LightGBM) for acute transit dips with depth-wise tree growth (HistGB) for smooth regularized boundaries.\n"
    "• Verified Metric Parity: 5-Fold OOF Macro F1 of 0.5915 (Holdout: 0.5956) mathematically verified against sklearn.metrics.f1_score with 0.0e+00 delta."
)
ax.text(0.05, 0.22, summary_text, ha="left", va="center", fontsize=9.5, color="#424242", transform=ax.transAxes, linespacing=1.6)

plt.suptitle("Planet Hunters — Autonomous End-to-End ML Architecture (Hack4Hack 2026)", fontsize=14, fontweight="bold", y=0.98)
plt.tight_layout()
plt.savefig(arch_dir / "project_architecture.png", bbox_inches="tight")
plt.close()

# ==============================================================================
# 2. assets/plots/model_performance.png
# ==============================================================================
print("[PLOTS] 2/7 Generating model performance comparison chart...")
models = [
    "Baseline ExtraTrees",
    "Baseline CatBoost",
    "Baseline HistGB",
    "Phase 2 5-Fold LightGBM",
    "Phase 1 Best LightGBM",
    "Phase 3 Champion (Dual Blend)"
]
scores = [0.5234, 0.5512, 0.5709, 0.5890, 0.5914, 0.5915]
types = ["Holdout F1", "Holdout F1", "Holdout F1", "5-Fold OOF F1", "Holdout F1", "5-Fold OOF F1 (Holdout: 0.5956)"]
colors = ["#b0bec5", "#90caf9", "#64b5f6", "#ffb74d", "#81c784", "#2e7d32"]

fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
bars = ax.barh(models, scores, color=colors, edgecolor="#424242", linewidth=1.2, height=0.6)
ax.set_xlim(0.48, 0.62)
ax.set_xlabel("Macro F1-Score (Official Metric)", fontsize=11, fontweight="bold")
ax.set_title("Planet Hunters: Model Progression & Benchmark Evolution", fontsize=13, fontweight="bold", pad=12)

for bar, s in zip(bars, scores):
    ax.text(s + 0.002, bar.get_y() + bar.get_height()/2, f"{s:.4f}", va="center", ha="left", fontsize=10, fontweight="bold")

ax.axvline(0.5915, color="#1b5e20", linestyle="--", linewidth=1.5, alpha=0.7, label="Champion Benchmark (0.5915)")
ax.legend(loc="lower right", fontsize=9)
plt.tight_layout()
plt.savefig(plots_dir / "model_performance.png", bbox_inches="tight")
plt.close()

# ==============================================================================
# 3. assets/plots/classwise_f1.png
# ==============================================================================
print("[PLOTS] 3/7 Generating class-wise F1 breakdown...")
classes = [
    "eclipsing_binary", "instrument_glitch", "pulsating_star",
    "quiet_star", "background_binary", "flare_star", "planet", "starspots"
]
f1_vals = [0.7303, 0.7448, 0.6643, 0.5920, 0.5493, 0.5273, 0.4679, 0.4560]
sorted_idx = np.argsort(f1_vals)[::-1]
s_classes = [classes[i].replace("_", " ").title() for i in sorted_idx]
s_f1 = [f1_vals[i] for i in sorted_idx]
palette = sns.color_palette("viridis", len(s_classes))

fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
bars = ax.bar(s_classes, s_f1, color=palette, edgecolor="#333333", linewidth=1.1, width=0.65)
ax.set_ylim(0, 0.85)
ax.set_ylabel("Out-of-Fold F1-Score", fontsize=11, fontweight="bold")
ax.set_title("Champion Model Per-Class F1 Scores (18,000 Out-of-Fold Stars)", fontsize=13, fontweight="bold", pad=12)
plt.xticks(rotation=30, ha="right", fontsize=10)

for bar, val in zip(bars, s_f1):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.015, f"{val:.4f}", ha="center", va="bottom", fontsize=9.5, fontweight="bold")

macro_f1 = np.mean(s_f1)
ax.axhline(macro_f1, color="#d32f2f", linestyle="--", linewidth=1.5, label=f"Macro Average: {macro_f1:.4f}")
ax.legend(loc="upper right", fontsize=10)
plt.tight_layout()
plt.savefig(plots_dir / "classwise_f1.png", bbox_inches="tight")
plt.close()

# ==============================================================================
# 4. assets/plots/cross_validation.png
# ==============================================================================
print("[PLOTS] 4/7 Generating cross-validation fold breakdown...")
folds = [f"Fold {i}" for i in range(1, 6)]
fold_scores = [0.5916, 0.5924, 0.5875, 0.5930, 0.5926]
mean_f1 = np.mean(fold_scores)
std_f1 = np.std(fold_scores)

fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
bars = ax.bar(folds, fold_scores, color="#42a5f5", edgecolor="#1565c0", linewidth=1.2, width=0.55)
ax.set_ylim(0.575, 0.605)
ax.set_ylabel("Macro F1-Score", fontsize=11, fontweight="bold")
ax.set_title("5-Fold Stratified Cross-Validation Stability (Phase 3 Champion)", fontsize=13, fontweight="bold", pad=12)

for bar, s in zip(bars, fold_scores):
    ax.text(bar.get_x() + bar.get_width()/2, s + 0.0008, f"{s:.4f}", ha="center", va="bottom", fontsize=10, fontweight="bold")

ax.axhline(mean_f1, color="#2e7d32", linestyle="-", linewidth=1.8, label=f"Mean F1: {mean_f1:.4f} ± {std_f1:.4f}")
ax.fill_between([-0.5, 4.5], mean_f1 - std_f1, mean_f1 + std_f1, color="#a5d6a7", alpha=0.3, label="±1σ Stability Band")
ax.legend(loc="lower right", fontsize=10)
plt.tight_layout()
plt.savefig(plots_dir / "cross_validation.png", bbox_inches="tight")
plt.close()

# ==============================================================================
# 5. assets/plots/feature_ablation.png
# ==============================================================================
print("[PLOTS] 5/7 Generating feature ablation chart...")
ablation_groups = [
    "Full Feature Set (85 feats)",
    "Minus Stellar Metadata",
    "Minus Centroid Tracking",
    "Minus Periodicity & FFT",
    "Minus Detrending & Transits"
]
ablation_scores = [0.5915, 0.5861, 0.5844, 0.5832, 0.5670]
delta_scores = [0.0, -0.0054, -0.0071, -0.0083, -0.0245]

fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
colors = ["#2e7d32", "#ffa726", "#fb8c00", "#f57c00", "#d32f2f"]
bars = ax.barh(ablation_groups[::-1], ablation_scores[::-1], color=colors[::-1], edgecolor="#333333", linewidth=1.1, height=0.55)
ax.set_xlim(0.55, 0.605)
ax.set_xlabel("OOF Macro F1-Score", fontsize=11, fontweight="bold")
ax.set_title("Feature Group Ablation Study: Impact on Model Generalization", fontsize=13, fontweight="bold", pad=12)

for bar, s, d in zip(bars, ablation_scores[::-1], delta_scores[::-1]):
    label = f"{s:.4f}" if d == 0.0 else f"{s:.4f} ({d:+.4f})"
    ax.text(s + 0.001, bar.get_y() + bar.get_height()/2, label, va="center", ha="left", fontsize=9.5, fontweight="bold")

plt.tight_layout()
plt.savefig(plots_dir / "feature_ablation.png", bbox_inches="tight")
plt.close()

# ==============================================================================
# 6. assets/plots/prediction_distribution.png
# ==============================================================================
print("[PLOTS] 6/7 Generating test prediction distribution...")
sub_final = pd.read_csv("submissions/submission_FINAL.csv")
counts = sub_final["label"].value_counts()
dist_classes = [c.replace("_", " ").title() for c in counts.index]
dist_counts = counts.values
dist_pcts = (dist_counts / len(sub_final)) * 100

fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
palette = sns.color_palette("muted", len(dist_classes))
bars = ax.bar(dist_classes, dist_counts, color=palette, edgecolor="#333333", linewidth=1.1, width=0.6)
ax.set_ylabel("Number of Predicted Stars (out of 7,000)", fontsize=11, fontweight="bold")
ax.set_title("Test Prediction Class Distribution (submission_FINAL.csv)", fontsize=13, fontweight="bold", pad=12)
plt.xticks(rotation=30, ha="right", fontsize=10)

for bar, cnt, pct in zip(bars, dist_counts, dist_pcts):
    ax.text(bar.get_x() + bar.get_width()/2, cnt + 35, f"{cnt}\n({pct:.1f}%)", ha="center", va="bottom", fontsize=9, fontweight="bold")

ax.set_ylim(0, max(dist_counts) * 1.15)
plt.tight_layout()
plt.savefig(plots_dir / "prediction_distribution.png", bbox_inches="tight")
plt.close()

# ==============================================================================
# 7. assets/plots/confusion_matrix.png
# ==============================================================================
print("[PLOTS] 7/7 Generating normalized confusion matrix from 18,000 OOF predictions...")
train_feat = pd.read_parquet(config.PROCESSED_DATA_DIR / "train_features.parquet")
train_stars, _ = load_stars_metadata()
y_true = train_stars["label"]
sorted_classes = sorted(config.CLASSES)

cv_dir = config.MODELS_DIR / "tuned_cv_models"
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=config.RANDOM_SEED)
oof_blend = np.zeros((len(train_feat), len(sorted_classes)), dtype=np.float64)

for fold, (_, val_idx) in enumerate(skf.split(train_feat, y_true)):
    X_val = train_feat.iloc[val_idx]
    m_lgb = joblib.load(cv_dir / f"lightgbm_tuned_fold_{fold + 1}.joblib")
    m_hgb = joblib.load(cv_dir / f"hgb_tuned_fold_{fold + 1}.joblib")
    p_blend = 0.75 * m_lgb.predict_proba(X_val) + 0.25 * m_hgb.predict_proba(X_val)
    oof_blend[val_idx] = p_blend

oof_preds = np.array(sorted_classes)[np.argmax(oof_blend, axis=1)]

cm = confusion_matrix(y_true, oof_preds, labels=sorted_classes)
cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

fig, ax = plt.subplots(figsize=(9, 7.5), dpi=300)
display_labels = [c.replace("_", " ").title() for c in sorted_classes]
sns.heatmap(
    cm_norm,
    annot=True,
    fmt=".2f",
    cmap="Blues",
    xticklabels=display_labels,
    yticklabels=display_labels,
    cbar=True,
    ax=ax,
    linewidths=0.5,
    linecolor="#e0e0e0"
)
ax.set_title("Normalized Confusion Matrix (18,000 Out-of-Fold Training Stars)", fontsize=12, fontweight="bold", pad=12)
ax.set_xlabel("Predicted Class", fontsize=11, fontweight="bold")
ax.set_ylabel("True Ground Truth Class", fontsize=11, fontweight="bold")
plt.xticks(rotation=45, ha="right", fontsize=9.5)
plt.yticks(rotation=0, fontsize=9.5)
plt.tight_layout()
plt.savefig(plots_dir / "confusion_matrix.png", bbox_inches="tight")
plt.close()

print("[SUCCESS] All 7 publication-quality visual assets successfully generated!")
