import sys
from pathlib import Path
from typing import Optional, Union
import joblib
import numpy as np
import pandas as pd
import argparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
from src import config
from src.submission_validation import validate_submission
from src.feature_engineering import get_or_extract_features

def generate_submission(
    model_choice: str = "champion",
    output_path: Optional[Union[str, Path]] = None,
    use_ensemble: Optional[bool] = None
) -> Path:
    """
    Generates test predictions and creates a strictly validated submission CSV.
    Supports:
      - 'champion' / 'v3': 5-Fold Dual-Architecture Ensemble (0.75 LightGBM + 0.25 HistGB)
      - 'v2': 5-Fold LightGBM Ensemble
      - 'lightgbm': Single best LightGBM holdout model
      - 'ensemble': Phase 1 3-model holdout blend (LGB+CB+HGB)
    """
    if use_ensemble is not None:
        model_choice = "ensemble" if use_ensemble else "lightgbm"

    model_choice = model_choice.lower().strip()
    print("=" * 65)
    print(f"GENERATING COMPETITION SUBMISSION (Model Choice: {model_choice})")
    print("=" * 65)

    # 1. Load test features and metadata
    _, test_feats = get_or_extract_features()
    test_stars = pd.read_csv(config.TEST_STARS_FILE)

    print(f"Loaded test features: {test_feats.shape}")
    print(f"Loaded test stars:    {test_stars.shape}")

    if test_feats.shape[0] != 7000:
        raise ValueError(f"Expected 7000 test stars, got {test_feats.shape[0]}")
    if test_feats.isna().any().any():
        raise ValueError("Test features contain unexpected NaN values!")
    if np.isinf(test_feats.values).any():
        raise ValueError("Test features contain unexpected infinite values!")

    classes = np.array(sorted(config.CLASSES))

    # 2. Determine target output path
    if output_path is not None:
        sub_path = Path(output_path)
    else:
        if model_choice in ["champion", "v3"]:
            sub_path = config.SUBMISSIONS_DIR / "submission_v3.csv"
        elif model_choice == "v2":
            sub_path = config.SUBMISSIONS_DIR / "submission_v2.csv"
        elif model_choice == "ensemble":
            sub_path = config.SUBMISSIONS_DIR / "submission_ensemble_phase1.csv"
        else:
            sub_path = config.SUBMISSIONS_DIR / "submission.csv"

    # 3. Model inference based on choice
    if model_choice in ["champion", "v3"]:
        print("[MODEL] Loading 5-Fold Dual-Architecture Champion Ensemble...")
        cv_dir = config.MODELS_DIR / "tuned_cv_models"
        if not cv_dir.exists():
            raise FileNotFoundError(f"Champion model directory not found at: {cv_dir}")

        test_probs_lgb = np.zeros((len(test_feats), len(classes)), dtype=np.float64)
        test_probs_hgb = np.zeros((len(test_feats), len(classes)), dtype=np.float64)

        for fold in range(1, 6):
            lgb_path = cv_dir / f"lightgbm_tuned_fold_{fold}.joblib"
            hgb_path = cv_dir / f"hgb_tuned_fold_{fold}.joblib"

            if not lgb_path.exists() or not hgb_path.exists():
                raise FileNotFoundError(f"Missing fold models for fold {fold} in {cv_dir}")

            print(f"  Predicting fold {fold}/5: LightGBM + HistGradientBoosting...")
            m_lgb = joblib.load(lgb_path)
            m_hgb = joblib.load(hgb_path)

            test_probs_lgb += m_lgb.predict_proba(test_feats) / 5.0
            test_probs_hgb += m_hgb.predict_proba(test_feats) / 5.0

        total_probs = 0.75 * test_probs_lgb + 0.25 * test_probs_hgb
        preds = classes[np.argmax(total_probs, axis=1)]

    elif model_choice == "v2":
        print("[MODEL] Loading 5-Fold Tuned LightGBM Ensemble...")
        cv_dir = config.MODELS_DIR / "tuned_cv_models"
        total_probs = np.zeros((len(test_feats), len(classes)), dtype=np.float64)
        for fold in range(1, 6):
            lgb_path = cv_dir / f"lightgbm_tuned_fold_{fold}.joblib"
            print(f"  Predicting fold {fold}/5: LightGBM...")
            m_lgb = joblib.load(lgb_path)
            total_probs += m_lgb.predict_proba(test_feats) / 5.0
        preds = classes[np.argmax(total_probs, axis=1)]

    elif model_choice == "ensemble":
        bundle_file = config.MODELS_DIR / "ensemble_bundle.joblib"
        if not bundle_file.exists():
            raise FileNotFoundError(f"Ensemble bundle not found: {bundle_file}")
        print("[MODEL] Loading Phase 1 ensemble bundle...")
        bundle = joblib.load(bundle_file)
        models = bundle["models"]
        weights = bundle["weights"]
        b_classes = bundle["classes"]

        total_probs = np.zeros((len(test_feats), len(b_classes)), dtype=np.float64)
        for name, weight in weights.items():
            if name in models:
                print(f"  Predicting with {name} (weight: {weight})...")
                p = models[name].predict_proba(test_feats)
                total_probs += weight * p
        preds = b_classes[np.argmax(total_probs, axis=1)]

    else: # single LightGBM
        best_model_file = config.MODELS_DIR / "best_lightgbm.joblib"
        if not best_model_file.exists():
            model_files = list(config.MODELS_DIR.glob("best_*.joblib"))
            if not model_files:
                raise FileNotFoundError("No trained model found in models/ directory!")
            best_model_file = model_files[0]

        print(f"[MODEL] Loading best single model: {best_model_file.name}...")
        model = joblib.load(best_model_file)
        preds = model.predict(test_feats)

    # 4. Build submission DataFrame
    sub_df = pd.DataFrame({
        "id": test_stars["id"],
        "label": preds
    })

    # 5. Write to target path
    sub_path.parent.mkdir(parents=True, exist_ok=True)
    sub_df.to_csv(sub_path, index=False)
    print(f"\n[SAVE] Successfully written submission to: {sub_path}")

    # 6. Validate submission strictly
    is_valid = validate_submission(sub_path)
    if not is_valid:
        raise ValueError(f"[ERROR] Generated submission at {sub_path} failed validation checks!")
    print("\n[SUCCESS] Final submission created and validated successfully!")
    return sub_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate competition submission predictions.")
    parser.add_argument(
        "--model",
        type=str,
        default="champion",
        choices=["champion", "v3", "v2", "lightgbm", "ensemble"],
        help="Model architecture to use for predictions (default: champion)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Optional custom output path for submission CSV (e.g. submissions/submission_v3_reproduced.csv)"
    )
    args = parser.parse_args()
    generate_submission(model_choice=args.model, output_path=args.output)
