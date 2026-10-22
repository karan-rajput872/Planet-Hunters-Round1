"""
Standalone Submission Validation Script for Planet Hunters (Hack4Hack 2026 Round 1).
Validates schema, row counts, ID alignment, labels, and astrophysical distribution.
Exits with code 0 on PASS, code 1 on FAIL.
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from src.submission_validation import validate_submission

def main():
    if len(sys.argv) < 2:
        target = Path("submissions/submission_FINAL.csv")
        if not target.exists():
            target = Path("submissions/submission_v3.csv")
    else:
        target = Path(sys.argv[1])

    print("=" * 65)
    print(f"PLANET HUNTERS SUBMISSION VALIDATOR: {target}")
    print("=" * 65)

    if not target.exists():
        print(f"[FAIL] Target file does not exist: {target}")
        sys.exit(1)

    result = validate_submission(target, verbose=True)

    print("\n" + "=" * 65)
    print(f"FINAL VALIDATION VERDICT: {'PASSED' if result['passed_all'] else 'FAILED'}")
    print("=" * 65)

    sys.exit(0 if result["passed_all"] else 1)

if __name__ == "__main__":
    main()
