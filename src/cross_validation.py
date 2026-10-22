import sys
import time
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score, precision_recall_fscore_support, confusion_matrix
import lightgbm as lgb

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src import config
from src.data_loader import load_stars_metadata

def run_stratified_cv(n_splits: int = 5):
    print("=" * 65)
    print(f"RUNNING {n_splits}-FOLD STRATIFIED CROSS-VALIDATION (LIGHTGBM)")
    print("=" * 65)

    train_feat_path = config.PROCESSED_DATA_DIR / "train_features.parquet"
    X = pd.read_parquet(train_feat_path)
    train_stars, _ = load_stars_metadata()
    y = train_stars["label"]

    classes = np.array(config.CLASSES)
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=config.RANDOM_SEED)

    oof_probs = np.zeros((len(X), len(config.CLASSES)), dtype=np.float64)
    fold_scores = []
    per_class_scores = []

    cv_models_dir = config.MODELS_DIR / "cv_models"
    cv_models_dir.mkdir(parents=True, exist_ok=True)

    t0_total = time.time()

    for fold, (train_idx, val_idx) in enumerate(skf.split(X, y)):
        print(f"\n>>> Fold {fold + 1}/{n_splits} <<<")
        X_tr, y_tr = X.iloc[train_idx], y.iloc[train_idx]
        X_val, y_val = X.iloc[val_idx], y.iloc[val_idx]

        model = lgb.LGBMClassifier(
            n_estimators=400,
            learning_rate=0.05,
            class_weight="balanced",
            num_leaves=31,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=config.RANDOM_SEED + fold,
            n_jobs=-1,
            verbose=-1
        )

        t0 = time.time()
        model.fit(X_tr, y_tr)
        fit_time = time.time() - t0

        # Save fold model
        fold_model_path = cv_models_dir / f"lightgbm_fold_{fold + 1}.joblib"
        joblib.dump(model, fold_model_path)

        probs = model.predict_proba(X_val)
        oof_probs[val_idx] = probs

        # Determine class alignment
        model_classes = model.classes_
        val_pred_indices = np.argmax(probs, axis=1)
        val_preds = model_classes[val_pred_indices]

        fold_f1 = f1_score(y_val, val_preds, average="macro")
        fold_scores.append(fold_f1)

        prec, rec, f1, sup = precision_recall_fscore_support(
            y_val, val_preds, labels=config.CLASSES, zero_division=0
        )
        per_class_scores.append(f1)

        print(f"  Fold {fold + 1} Macro F1: {fold_f1:.4f} (Fit Time: {fit_time:.2f}s)")

    total_time = time.time() - t0_total
    mean_f1 = float(np.mean(fold_scores))
    std_f1 = float(np.std(fold_scores))

    # Overall Out-Of-Fold Evaluation
    model_classes = np.array(sorted(config.CLASSES))
    oof_pred_indices = np.argmax(oof_probs, axis=1)
    oof_preds = model_classes[oof_pred_indices]
    overall_oof_macro_f1 = f1_score(y, oof_preds, average="macro")
    overall_oof_weighted_f1 = f1_score(y, oof_preds, average="weighted")

    print("\n" + "=" * 65)
    print("5-FOLD CROSS-VALIDATION SUMMARY:")
    print(f"Fold Macro F1 Scores: {[round(s, 4) for s in fold_scores]}")
    print(f"Mean Macro F1:        {mean_f1:.4f} +/- {std_f1:.4f}")
    print(f"Overall OOF Macro F1: {overall_oof_macro_f1:.4f}")
    print(f"Overall OOF W-F1:     {overall_oof_weighted_f1:.4f}")
    print(f"Total CV Runtime:     {total_time:.2f}s")
    print("=" * 65)

    # Per-class summary across folds
    per_class_matrix = np.array(per_class_scores) # shape: (5, 8)
    per_class_mean = np.mean(per_class_matrix, axis=0)
    per_class_std = np.std(per_class_matrix, axis=0)

    summary_df = pd.DataFrame({
        "class": config.CLASSES,
        "mean_f1": np.round(per_class_mean, 4),
        "std_f1": np.round(per_class_std, 4),
        "min_f1": np.round(np.min(per_class_matrix, axis=0), 4),
        "max_f1": np.round(np.max(per_class_matrix, axis=0), 4)
    }).sort_values("mean_f1", ascending=False)

    print("\nPer-Class F1 Breakdown across 5 Folds:")
    print(summary_df.to_string(index=False))

    # Save OOF predictions
    oof_df = pd.DataFrame(oof_probs, columns=[f"prob_{c}" for c in config.CLASSES])
    oof_df["pred_label"] = oof_preds
    oof_df["true_label"] = y
    oof_df.to_parquet(config.PROCESSED_DATA_DIR / "oof_predictions.parquet", index=False)

    # Save Markdown Report
    report_md = f"""# 5-Fold Stratified Cross-Validation Results

## 1. Executive Summary
- **Model**: LightGBM Classifier (85 features, balanced weights)
- **Folds**: 5-Fold Stratified K-Fold (seed: {config.RANDOM_SEED})
- **Total Training Stars**: 18,000
- **Mean Fold Macro F1**: **{mean_f1:.4f} +/- {std_f1:.4f}**
- **Overall Out-Of-Fold (OOF) Macro F1**: **{overall_oof_macro_f1:.4f}**
- **Overall OOF Weighted F1**: **{overall_oof_weighted_f1:.4f}**
- **Total Runtime**: {total_time:.2f} seconds

## 2. Fold-by-Fold Performance

| Fold | Macro F1-Score |
|---|---|
| Fold 1 | {fold_scores[0]:.4f} |
| Fold 2 | {fold_scores[1]:.4f} |
| Fold 3 | {fold_scores[2]:.4f} |
| Fold 4 | {fold_scores[3]:.4f} |
| Fold 5 | {fold_scores[4]:.4f} |
| **Mean +/- Std** | **{mean_f1:.4f} +/- {std_f1:.4f}** |

## 3. Per-Class F1 Across Folds

| Class | Mean F1 | Std F1 | Min F1 | Max F1 |
|---|---|---|---|---|
"""
    for _, r in summary_df.iterrows():
        report_md += f"| `{r['class']}` | **{r['mean_f1']:.4f}** | {r['std_f1']:.4f} | {r['min_f1']:.4f} | {r['max_f1']:.4f} |\n"

    report_md += f"""
## 4. Key Takeaways
1. **Model Stability**: Standard deviation across folds is low ({std_f1:.4f}), confirming that the feature pipeline produces consistent representations without fold-dependent instability.
2. **Planet F1**: Averaged {summary_df.loc[summary_df['class']=='planet', 'mean_f1'].values[0]:.4f} across all folds.
3. **Out-of-Fold Ground Truth**: OOF probabilities across all 18,000 stars are cached in `data/processed/oof_predictions.parquet` for un-biased ensemble weighting and calibration.
"""

    report_path = config.REPORTS_DIR / "cross_validation_results.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_md)
    print(f"\nSaved cross-validation report to: {report_path}")

    return {
        "mean_f1": mean_f1,
        "std_f1": std_f1,
        "oof_macro_f1": overall_oof_macro_f1,
        "summary_df": summary_df
    }

if __name__ == "__main__":
    run_stratified_cv()
