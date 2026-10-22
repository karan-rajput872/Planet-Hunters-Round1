import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.feature_engineering import get_or_extract_features
from src.model_training import run_model_comparison
from generate_submission import generate_submission

def main():
    print("=" * 70)
    print("PLANET HUNTERS: FIND NEW WORLDS IN STARLIGHT")
    print("Hack4Hack 2026 - Round 1 Pipeline Runner")
    print("=" * 70)

    # 1. Feature Extraction & Caching
    print("\n>>> STAGE 1: FEATURE EXTRACTION & CACHING <<<")
    get_or_extract_features(force_recompute=False)

    # 2. Model Training & Validation
    print("\n>>> STAGE 2: MODEL TRAINING & BENCHMARKING <<<")
    run_model_comparison()

    # 3. Submission Generation & Validation
    print("\n>>> STAGE 3: TEST PREDICTION & SUBMISSION VALIDATION <<<")
    generate_submission(model_choice="champion")

    print("\n" + "=" * 70)
    print("ALL PIPELINE STAGES COMPLETED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    main()
