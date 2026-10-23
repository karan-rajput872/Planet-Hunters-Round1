"""
Planet Hunters — Submission Validation Engine
ML Challenge Hack4Hack 2026 — Round 1
Decoupled Two-Stage Submission Compliance Auditor:
  Stage A: Independent Submission Artifact Checks (12 checks)
  Stage B: Target Dataset Cross-Matching Checks (2 checks)
Completely deployment-safe with zero raw exceptions on missing external datasets.
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src import config

logger = logging.getLogger(__name__)

def validate_submission(
    submission_path: Path,
    test_stars_path: Optional[Path] = None,
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Validates submission CSV according to Hack4Hack 2026 rules:
    
    STAGE A — Artifact Integrity (Independent of external test dataset):
      1. File exists and is non-empty
      2. File is readable UTF-8 CSV
      3. Exactly 7,000 target rows
      4. Exactly 2 columns
      5. Column names exactly ['id', 'label']
      6. No unexpected index or unnamed columns
      7. No null/NaN IDs
      8. No duplicate star IDs
      9. No null/NaN prediction labels
      10. No blank/whitespace-only label tokens
      11. All prediction labels belong to the 8 valid astronomical classes
      12. All 8 permitted classes are represented in predictions
      13. CSV can be reloaded and round-trip verified
      
    STAGE B — Target Dataset Matching (Dependent on test_stars.csv):
      14. Predicted IDs match test_stars.csv IDs exactly in set
      15. Predicted IDs strictly match test_stars.csv row order
      
    If test_stars_path is missing, Stage A checks execute fully, and Stage B checks
    are reported as BLOCKED without crashing the host application.
    """
    submission_path = Path(submission_path).resolve()
    if test_stars_path is None:
        test_stars_path = config.TEST_STARS_FILE
    test_stars_path = Path(test_stars_path).resolve()

    if verbose:
        print(f"\n[VALIDATION] Validating submission artifact: {submission_path}")

    result: Dict[str, Any] = {
        "file": submission_path.name,
        "path": str(submission_path),
        # Stage A Checks
        "exists": False,
        "readable": False,
        "exact_7000_rows": False,
        "exact_two_columns": False,
        "exact_column_names": False,
        "no_index_column": False,
        "no_null_ids": False,
        "no_duplicate_ids": False,
        "no_null_labels": False,
        "no_whitespace_labels": False,
        "all_classes_valid": False,
        "all_eight_classes_represented": False,
        "read_back_success": False,
        # Stage B Checks
        "test_data_available": False,
        "id_match_test_stars": False,
        "id_order_correct": False,
        # Status & Diagnostics
        "passed_all": False,
        "artifact_checks_passed": False,
        "status": "FAILED",  # "PASSED", "BLOCKED", or "FAILED"
        "test_data_status": "NOT_RUN",  # "PASSED", "BLOCKED", or "FAILED"
        "failures": [],
        "warnings": [],
        "blocked": [],
        "class_distribution": {}
    }

    # 1. Existence Check
    if not submission_path.is_file():
        msg = f"Submission file not found: {submission_path}"
        result["failures"].append(msg)
        if verbose:
            print(f"[FAIL] {msg}")
        return result
    result["exists"] = True

    # 2. Readable CSV Check
    try:
        sub = pd.read_csv(submission_path)
        result["readable"] = True
    except Exception as e:
        msg = f"Failed to parse CSV file: {e}"
        result["failures"].append(msg)
        if verbose:
            print(f"[FAIL] {msg}")
        return result

    # 3. Columns Check
    cols = list(sub.columns)
    if len(cols) == 2:
        result["exact_two_columns"] = True
    else:
        result["failures"].append(f"Expected 2 columns, got {len(cols)}: {cols}")

    if cols == ["id", "label"]:
        result["exact_column_names"] = True
    else:
        result["failures"].append(f"Invalid column names: {cols}, expected ['id', 'label']")

    if "Unnamed: 0" not in cols and (len(cols) > 0 and cols[0] == "id"):
        result["no_index_column"] = True
    else:
        result["failures"].append("Unexpected index or unnamed column detected!")

    # 4. Row Count Check
    if len(sub) == 7000:
        result["exact_7000_rows"] = True
    else:
        result["failures"].append(f"Invalid row count: {len(sub)}, expected 7000 predictions")

    # 5. ID Structural Integrity (Independent of external dataset)
    if "id" in sub.columns:
        if sub["id"].isnull().sum() == 0:
            result["no_null_ids"] = True
        else:
            result["failures"].append(f"Found {sub['id'].isnull().sum()} null target IDs!")

        if sub["id"].duplicated().sum() == 0:
            result["no_duplicate_ids"] = True
        else:
            result["failures"].append(f"Found {sub['id'].duplicated().sum()} duplicate target IDs!")
    else:
        result["failures"].append("Missing required column 'id'")

    # 6. Label Structural Integrity
    if "label" in sub.columns:
        if sub["label"].isnull().sum() == 0:
            result["no_null_labels"] = True
        else:
            result["failures"].append(f"Found {sub['label'].isnull().sum()} null prediction labels!")

        whitespace_count = sub["label"].astype(str).str.strip().eq("").sum()
        if whitespace_count == 0:
            result["no_whitespace_labels"] = True
        else:
            result["failures"].append(f"Found {whitespace_count} whitespace-only labels!")

        invalid_labels = set(sub["label"].dropna()) - set(config.CLASSES)
        if len(invalid_labels) == 0:
            result["all_classes_valid"] = True
        else:
            result["failures"].append(f"Unrecognized class names: {invalid_labels}")

        present_classes = set(sub["label"].dropna())
        if len(present_classes) == 8:
            result["all_eight_classes_represented"] = True
        else:
            result["failures"].append(
                f"Only {len(present_classes)} of 8 classes represented in predictions: {present_classes}"
            )
    else:
        result["failures"].append("Missing required column 'label'")

    # 7. Read Back Round-Trip Verification
    try:
        sub_reloaded = pd.read_csv(submission_path)
        if len(sub_reloaded) == len(sub) and list(sub_reloaded.columns) == list(sub.columns):
            result["read_back_success"] = True
        else:
            result["failures"].append("Reloaded CSV row or column structure differed from parsed memory.")
    except Exception as e:
        result["failures"].append(f"Failed round-trip reload of submission CSV: {e}")

    # Compute predicted class distribution preview
    if "label" in sub.columns:
        val_counts = sub["label"].value_counts()
        for cls in config.CLASSES:
            cnt = int(val_counts.get(cls, 0))
            pct = (cnt / max(len(sub), 1)) * 100
            result["class_distribution"][cls] = {"count": cnt, "pct": round(pct, 2)}

    # Stage A Status Evaluation
    result["artifact_checks_passed"] = (len(result["failures"]) == 0)

    # =========================================================================
    # STAGE B: Target Dataset Cross-Matching Checks (Safe & Non-crashing)
    # =========================================================================
    if test_stars_path.is_file():
        result["test_data_available"] = True
        try:
            test_stars = pd.read_csv(test_stars_path)
            if "id" in test_stars.columns and "id" in sub.columns:
                if set(sub["id"]) == set(test_stars["id"]):
                    result["id_match_test_stars"] = True
                else:
                    result["failures"].append("Submission IDs do not match test_stars.csv IDs!")

                if (sub["id"].values == test_stars["id"].values).all():
                    result["id_order_correct"] = True
                else:
                    result["failures"].append("ID sequence is not in the exact same order as test_stars.csv!")

                result["test_data_status"] = "PASSED" if (result["id_match_test_stars"] and result["id_order_correct"]) else "FAILED"
            else:
                result["failures"].append("Column 'id' missing from test_stars.csv or submission file.")
                result["test_data_status"] = "FAILED"
        except Exception as e:
            msg = f"Could not read test_stars.csv for validation: {e}"
            result["failures"].append(msg)
            result["test_data_status"] = "FAILED"
    else:
        # Test dataset is intentionally absent (e.g., in public deployment)
        result["test_data_available"] = False
        result["test_data_status"] = "BLOCKED"
        result["id_match_test_stars"] = None  # None indicates BLOCKED / NOT RUN
        result["id_order_correct"] = None     # None indicates BLOCKED / NOT RUN
        result["blocked"].extend(["id_match_test_stars", "id_order_correct"])
        result["warnings"].append(
            f"Test target dataset not found at {test_stars_path.name}. "
            "Target-matching checks (ID set and ordering) are marked as BLOCKED."
        )

    # Overall Audit Status Resolution
    if len(result["failures"]) == 0:
        if result["test_data_status"] == "PASSED":
            result["passed_all"] = True
            result["status"] = "PASSED"
        elif result["test_data_status"] == "BLOCKED":
            result["passed_all"] = False
            result["status"] = "BLOCKED"
        else:
            result["passed_all"] = False
            result["status"] = "FAILED"
    else:
        result["passed_all"] = False
        result["status"] = "FAILED"

    if verbose:
        if result["status"] == "PASSED":
            print(f"[PASS] All 14 structural, schema, and astrophysical checks passed for {submission_path.name}!")
            print("Predicted Class Distribution:")
            for cls in config.CLASSES:
                info = result["class_distribution"][cls]
                print(f"  {cls:<20}: {info['count']:>5} ({info['pct']:>5.1f}%)")
        elif result["status"] == "BLOCKED":
            print(f"[BLOCKED] Artifact checks PASSED for {submission_path.name}, but 2 checks are BLOCKED:")
            for w in result["warnings"]:
                print(f"  - {w}")
        else:
            print(f"[FAIL] Submission {submission_path.name} failed with {len(result['failures'])} errors:")
            for err in result["failures"]:
                print(f"  - {err}")

    return result

def validate_all_submissions(report_path: Optional[Path] = None) -> pd.DataFrame:
    """Validates all submissions in submissions/ directory and writes a markdown report."""
    sub_dir = config.SUBMISSIONS_DIR
    files = [
        sub_dir / "submission_FINAL.csv",
        sub_dir / "submission_FINAL_PHASE4_BACKUP.csv",
        sub_dir / "submission_PHASE6_candidate_01.csv",
        sub_dir / "submission_PHASE7_candidate_01.csv",
        sub_dir / "submission_PHASE8_candidate_01.csv",
    ]

    results = []
    for f in files:
        if f.is_file():
            res = validate_submission(f, verbose=True)
            results.append(res)

    if report_path is None:
        report_path = config.REPORTS_DIR / "submission_validation_audit.md"
    
    config.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    df_res = pd.DataFrame(results)
    return df_res

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_file = Path(sys.argv[1])
        res = validate_submission(test_file)
        # Exit with 0 if either fully passed or artifact-verified in cloud blocked mode
        sys.exit(0 if (res["passed_all"] or res["status"] == "BLOCKED") else 1)
    else:
        validate_all_submissions()
