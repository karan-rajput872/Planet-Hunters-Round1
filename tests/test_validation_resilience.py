"""
Comprehensive Validation & Resilience Test Suite
Tests all 8 production scenarios required for Streamlit Cloud deployment:
1. TEST_STARS_FILE resolution when present.
2. Graceful handling and BLOCKED status when test dataset is missing.
3. Decoupled artifact checks run when test dataset is missing without false 14/14 claims.
4. Full 14-point audit passes when both files exist.
5. Malformed submission CSV reports genuine failure without unhandled exceptions.
6. Schema violations (incorrect columns, wrong row count) report specific failures.
7. Repeated validation executions remain stable.
8. Pathlib path resolution is independent of the current working directory.
"""

import unittest
import os
import tempfile
from pathlib import Path
import pandas as pd

from src import config
from src.submission_validation import validate_submission
from dashboard.data_loader import run_submission_validation

class TestValidationResilience(unittest.TestCase):

    def setUp(self):
        self.project_root = config.PROJECT_ROOT
        self.submission_final = self.project_root / "submissions" / "submission_FINAL.csv"
        self.test_stars_file = config.TEST_STARS_FILE

    def test_01_test_stars_file_resolves(self):
        """TEST 1: Configured TEST_STARS_FILE exists and resolves correctly."""
        self.assertTrue(isinstance(config.TEST_STARS_FILE, Path))
        self.assertEqual(config.TEST_STARS_FILE.name, "test_stars.csv")
        self.assertTrue(self.test_stars_file.is_file(), "data/raw/test_stars.csv must be present locally")

    def test_02_missing_test_dataset_graceful_blocked(self):
        """TEST 2: When test dataset is missing, validator reports BLOCKED without crashing."""
        fake_test_path = self.project_root / "data" / "raw" / "non_existent_test_stars.csv"
        self.assertFalse(fake_test_path.exists())

        # Must not raise FileNotFoundError or any exception
        res = validate_submission(self.submission_final, test_stars_path=fake_test_path, verbose=False)
        self.assertFalse(res["passed_all"], "Cannot pass all 14 checks when test dataset is missing")
        self.assertTrue(res["artifact_checks_passed"], "All 12 artifact checks should pass on valid submission")
        self.assertEqual(res["status"], "BLOCKED")
        self.assertEqual(res["test_data_status"], "BLOCKED")
        self.assertIsNone(res["id_match_test_stars"])
        self.assertIsNone(res["id_order_correct"])
        self.assertGreater(len(res["warnings"]), 0)

    def test_03_submission_checks_independent_of_test_data(self):
        """TEST 3: Submission artifact checks run independently and are not falsely marked."""
        fake_test_path = Path("/tmp/does_not_exist_at_all.csv")
        res = validate_submission(self.submission_final, test_stars_path=fake_test_path, verbose=False)
        self.assertTrue(res["exists"])
        self.assertTrue(res["readable"])
        self.assertTrue(res["exact_7000_rows"])
        self.assertTrue(res["exact_two_columns"])
        self.assertTrue(res["exact_column_names"])
        self.assertTrue(res["no_null_ids"])
        self.assertTrue(res["no_duplicate_ids"])
        self.assertTrue(res["no_null_labels"])
        self.assertTrue(res["all_classes_valid"])
        self.assertTrue(res["all_eight_classes_represented"])
        # Group B checks MUST NOT be marked True
        self.assertNotEqual(res["id_match_test_stars"], True)
        self.assertNotEqual(res["id_order_correct"], True)

    def test_04_both_files_present_full_pass(self):
        """TEST 4: When both files exist, all 14 checks execute and PASS."""
        res = validate_submission(self.submission_final, test_stars_path=self.test_stars_file, verbose=False)
        self.assertTrue(res["passed_all"])
        self.assertEqual(res["status"], "PASSED")
        self.assertEqual(res["test_data_status"], "PASSED")
        self.assertTrue(res["id_match_test_stars"])
        self.assertTrue(res["id_order_correct"])
        self.assertEqual(len(res["failures"]), 0)

    def test_05_malformed_csv_handled_safely(self):
        """TEST 5: Malformed submission CSV reports failure without crashing host application."""
        with tempfile.NamedTemporaryFile(suffix=".csv", mode="w", delete=False) as f:
            f.write("This is not a valid CSV\x00\xffbroken corrupted content")
            temp_path = Path(f.name)

        try:
            res = validate_submission(temp_path, test_stars_path=self.test_stars_file, verbose=False)
            self.assertFalse(res["passed_all"])
            self.assertEqual(res["status"], "FAILED")
            self.assertGreater(len(res["failures"]), 0)
        finally:
            if temp_path.exists():
                os.remove(temp_path)

    def test_06_schema_violations_reported(self):
        """TEST 6: CSV with incorrect columns or row counts reports specific failures."""
        with tempfile.NamedTemporaryFile(suffix=".csv", mode="w", delete=False) as f:
            # Only 5 rows and wrong columns
            f.write("wrong_id,wrong_label,extra_col\n1,planet,foo\n2,starspots,bar\n")
            temp_path = Path(f.name)

        try:
            res = validate_submission(temp_path, test_stars_path=self.test_stars_file, verbose=False)
            self.assertFalse(res["passed_all"])
            self.assertFalse(res["exact_7000_rows"])
            self.assertFalse(res["exact_two_columns"])
            self.assertFalse(res["exact_column_names"])
            self.assertIn("Invalid column names", " ".join(res["failures"]))
        finally:
            if temp_path.exists():
                os.remove(temp_path)

    def test_07_repeated_validation_consistency(self):
        """TEST 7: Repeated validation calls return consistent results without side effects."""
        res1 = run_submission_validation(self.submission_final, self.test_stars_file)
        res2 = run_submission_validation(self.submission_final, self.test_stars_file)
        self.assertEqual(res1["passed_all"], res2["passed_all"])
        self.assertEqual(res1["status"], res2["status"])
        self.assertEqual(res1["class_distribution"], res2["class_distribution"])

    def test_08_cwd_independence(self):
        """TEST 8: Project paths resolve correctly regardless of working directory."""
        original_cwd = os.getcwd()
        try:
            # Change to system temporary directory
            os.chdir(tempfile.gettempdir())
            # Path resolution in config and validator should remain anchored to PROJECT_ROOT
            self.assertTrue(config.PROJECT_ROOT.is_dir())
            self.assertEqual(config.PROJECT_ROOT.name, "Planet-Hunters-Round1")
            res = validate_submission(self.submission_final, test_stars_path=self.test_stars_file, verbose=False)
            self.assertTrue(res["passed_all"])
        finally:
            os.chdir(original_cwd)

if __name__ == "__main__":
    unittest.main()
