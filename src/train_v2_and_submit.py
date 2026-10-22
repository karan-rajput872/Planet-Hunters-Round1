import sys
import time
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score, precision_recall_fscore_support
import lightgbm as lgb

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src import config
from src.data_loader import load_stars_metadata
from src.submission_validation import validate_submission

def train_tuned_5fold_and_generate_v2():
    print("=" * 65)
    print("TRAINING TUNED 5-FOLD LIGHTGBM ENSEMBLE & GENERATING SUBMISSION V2")
    print("=" * 65)

    # Load features
    train_feat_path = config.PROCESSED_DATA_DIR / "train_features.parquet"
    test_feat_path = config.PROCESSED_DATA_DIR / "test_features.parquet"

    X = pd.read_parquet(train_feat_path)
    X_test = pd.read_parquet(test_feat_path)
    train_stars, test_stars = load_stars_metadata()
    y = train_stars["label"]

    classes = np.array(sorted(config.CLASSES))
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=config.RANDOM_SEED)

    oof_probs = np.zeros((len(X), len(config.CLASSES)), dtype=np.float64)
    test_probs = np.zeros((len(X_test), len(config.CLASSES)), dtype=np.float64)

    save_dir = config.MODELS_DIR / "tuned_cv_models"
    save_dir.mkdir(parents=True, exist_ok=True)

    fold_scores = []
    per_class_scores = []

    t0_start = time.time()

    # Tuned hyperparameters
    best_params = {
        "num_leaves": 63,
        "learning_rate": 0.035,
        "n_estimators": 600,
        "min_child_samples": 30,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "class_weight": "balanced",
        "n_jobs": -1,
        "verbose": -1
    }

    for fold, (train_idx, val_idx) in enumerate(skf.split(X, y)):
        print(f"\n--- Training Fold {fold + 1}/5 ---")
        X_tr, y_tr = X.iloc[train_idx], y.iloc[train_idx]
        X_val, y_val = X.iloc[val_idx], y.iloc[val_idx]

        model = lgb.LGBMClassifier(
            **best_params,
            random_state=config.RANDOM_SEED + fold * 10
        )

        t0 = time.time()
        model.fit(X_tr, y_tr)
        fit_time = time.time() - t0

        # Save fold model
        fold_save_path = save_dir / f"lightgbm_tuned_fold_{fold + 1}.joblib"
        joblib.dump(model, fold_save_path)

        # Validation prediction
        p_val = model.predict_proba(X_val)
        oof_probs[val_idx] = p_val

        # Test prediction (accumulate for 5-fold bagging)
        p_test = model.predict_proba(X_test)
        test_probs += p_test / 5.0

        val_preds = model.classes_[np.argmax(p_val, axis=1)]
        f1 = f1_score(y_val, val_preds, average="macro")
        fold_scores.append(f1)

        _, _, class_f1, _ = precision_recall_fscore_support(
            y_val, val_preds, labels=classes, zero_division=0
        )
        per_class_scores.append(class_f1)

        print(f"  Fold {fold + 1} Macro F1: {f1:.4f} (Fit time: {fit_time:.2f}s)")

    total_time = time.time() - t0_start
    mean_f1 = float(np.mean(fold_scores))
    std_f1 = float(np.std(fold_scores))

    # Overall OOF score
    oof_preds = classes[np.argmax(oof_probs, axis=1)]
    overall_oof_macro_f1 = f1_score(y, oof_preds, average="macro")
    overall_oof_w_f1 = f1_score(y, oof_preds, average="weighted")

    print("\n" + "=" * 65)
    print("TUNED 5-FOLD CV EVALUATION RESULTS:")
    print(f"Fold Scores:         {[round(s, 4) for s in fold_scores]}")
    print(f"Mean Fold Macro F1:  {mean_f1:.4f} +/- {std_f1:.4f}")
    print(f"Overall OOF Macro F1:{overall_oof_macro_f1:.4f}")
    print(f"Overall OOF W-F1:    {overall_oof_w_f1:.4f}")
    print(f"Total CV Runtime:    {total_time:.2f}s")
    print("=" * 65)

    # Per-class summary
    per_class_mean = np.mean(np.array(per_class_scores), axis=0)
    per_class_df = pd.DataFrame({
        "class": classes,
        "mean_f1": np.round(per_class_mean, 4)
    }).sort_values("mean_f1", ascending=False)
    print("\nPer-Class Macro F1 Breakdown across 5 Folds:")
    print(per_class_df.to_string(index=False))

    # Generate submission_v2.csv
    test_pred_indices = np.argmax(test_probs, axis=1)
    test_preds = classes[test_pred_indices]

    sub_v2_path = config.SUBMISSIONS_DIR / "submission_v2.csv"
    sub_v2_df = pd.DataFrame({
        "id": test_stars["id"],
        "label": test_preds
    })
    sub_v2_df.to_csv(sub_v2_path, index=False)
    print(f"\n[SAVE] Written submission_v2 to: {sub_v2_path}")

    # Validate submission_v2
    is_valid = validate_submission(sub_v2_path)
    if not is_valid:
        raise ValueError("[ERROR] submission_v2.csv failed validation!")

    print("\n[SUCCESS] submission_v2.csv validated and ready for competition leaderboard!")
    return sub_v2_path

if __name__ == "__main__":
    train_tuned_5fold_and_generate_v2()
