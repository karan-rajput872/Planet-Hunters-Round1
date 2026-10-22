import sys
import time
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.ensemble import HistGradientBoostingClassifier, ExtraTreesClassifier, RandomForestClassifier
import lightgbm as lgb
from catboost import CatBoostClassifier

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src import config
from src.model_evaluation import evaluate_predictions
from src.data_loader import load_stars_metadata

def load_data():
    train_feat_path = config.PROCESSED_DATA_DIR / "train_features.parquet"
    test_feat_path = config.PROCESSED_DATA_DIR / "test_features.parquet"

    X = pd.read_parquet(train_feat_path)
    X_test = pd.read_parquet(test_feat_path)
    train_stars, test_stars = load_stars_metadata()
    y = train_stars["label"]

    return X, y, X_test, test_stars

def log_experiment(exp_name: str, model_type: str, n_features: int, macro_f1: float, runtime_sec: float, notes: str):
    log_file = config.REPORTS_DIR / "experiment_log.csv"
    record = {
        "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
        "experiment_name": exp_name,
        "model_type": model_type,
        "n_features": n_features,
        "macro_f1": round(macro_f1, 4),
        "runtime_seconds": round(runtime_sec, 2),
        "notes": notes
    }
    df_rec = pd.DataFrame([record])
    if log_file.exists():
        df_rec.to_csv(log_file, mode="a", header=False, index=False)
    else:
        df_rec.to_csv(log_file, index=False)

def run_model_comparison():
    print("=" * 60)
    print("RUNNING SYSTEMATIC MODEL BENCHMARKING (80/20 STRATIFIED)")
    print("=" * 60)

    X, y, X_test, test_stars = load_data()
    print(f"Features: {X.shape[1]} | Samples: {X.shape[0]}")

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.20, stratify=y, random_state=config.RANDOM_SEED
    )

    models = {
        "HistGradientBoosting": HistGradientBoostingClassifier(
            max_iter=350,
            learning_rate=0.06,
            class_weight="balanced",
            random_state=config.RANDOM_SEED
        ),
        "LightGBM": lgb.LGBMClassifier(
            n_estimators=400,
            learning_rate=0.05,
            class_weight="balanced",
            num_leaves=31,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=config.RANDOM_SEED,
            n_jobs=-1,
            verbose=-1
        ),
        "CatBoost": CatBoostClassifier(
            iterations=500,
            learning_rate=0.06,
            depth=6,
            auto_class_weights="Balanced",
            random_seed=config.RANDOM_SEED,
            thread_count=-1,
            verbose=0
        ),
        "ExtraTrees": ExtraTreesClassifier(
            n_estimators=250,
            class_weight="balanced",
            max_depth=20,
            random_state=config.RANDOM_SEED,
            n_jobs=-1
        ),
    }

    results = []
    best_macro_f1 = 0.0
    best_model_name = None
    best_model_obj = None

    val_probs = {}

    for name, model in models.items():
        print(f"\n--- Training {name} ---")
        t0 = time.time()
        model.fit(X_train, y_train)
        fit_time = time.time() - t0

        preds = model.predict(X_val)
        probs = model.predict_proba(X_val)
        val_probs[name] = probs

        eval_res = evaluate_predictions(y_val, preds, model_name=name)
        f1 = eval_res["macro_f1"]

        results.append({
            "model": name,
            "macro_f1": round(f1, 4),
            "weighted_f1": round(eval_res["weighted_f1"], 4),
            "train_time_sec": round(fit_time, 2)
        })

        log_experiment(
            exp_name=f"benchmark_{name.lower()}",
            model_type=name,
            n_features=X.shape[1],
            macro_f1=f1,
            runtime_sec=fit_time,
            notes=f"80/20 Stratified Validation"
        )

        if f1 > best_macro_f1:
            best_macro_f1 = f1
            best_model_name = name
            best_model_obj = model

    # Test Ensemble of Top Gradient Boosters (LightGBM + CatBoost + HistGB)
    print("\n--- Evaluating Weighted Probability Ensemble ---")
    # Blend probabilities
    ensemble_prob = (0.45 * val_probs["LightGBM"] +
                     0.35 * val_probs["CatBoost"] +
                     0.20 * val_probs["HistGradientBoosting"])
    # Classes are alphabetical or based on model.classes_
    classes_order = models["LightGBM"].classes_
    ensemble_pred_indices = np.argmax(ensemble_prob, axis=1)
    ensemble_preds = classes_order[ensemble_pred_indices]

    ens_eval = evaluate_predictions(y_val, ensemble_preds, model_name="Ensemble_LGB_CB_HGB")
    ens_f1 = ens_eval["macro_f1"]

    results.append({
        "model": "Ensemble (LGB+CB+HGB)",
        "macro_f1": round(ens_f1, 4),
        "weighted_f1": round(ens_eval["weighted_f1"], 4),
        "train_time_sec": 0.0
    })

    log_experiment(
        exp_name="ensemble_lgb_cb_hgb",
        model_type="Ensemble",
        n_features=X.shape[1],
        macro_f1=ens_f1,
        runtime_sec=0.0,
        notes="Probability blend: 0.45 LGB + 0.35 CB + 0.20 HGB"
    )

    # Save model comparison
    comp_df = pd.DataFrame(results).sort_values("macro_f1", ascending=False)
    comp_path = config.REPORTS_DIR / "model_comparison.csv"
    comp_df.to_csv(comp_path, index=False)
    print("\n" + "=" * 60)
    print("FINAL MODEL BENCHMARK RANKING:")
    print(comp_df.to_string(index=False))
    print(f"\nSaved comparison to {comp_path}")

    # Save individual best single model
    model_save_path = config.MODELS_DIR / f"best_{best_model_name.lower()}.joblib"
    joblib.dump(best_model_obj, model_save_path)
    print(f"Saved best individual model ({best_model_name}) to {model_save_path}")

    # Also save the full trained models dictionary for the ensemble
    ensemble_bundle = {
        "models": models,
        "weights": {"LightGBM": 0.45, "CatBoost": 0.35, "HistGradientBoosting": 0.20},
        "classes": classes_order,
        "feature_names": list(X.columns),
        "validation_macro_f1": ens_f1
    }
    joblib.dump(ensemble_bundle, config.MODELS_DIR / "ensemble_bundle.joblib")
    print(f"Saved ensemble bundle to {config.MODELS_DIR / 'ensemble_bundle.joblib'}")

if __name__ == "__main__":
    run_model_comparison()
