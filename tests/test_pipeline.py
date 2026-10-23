import unittest
import numpy as np
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src import config
from src.preprocessing import normalize_flux, process_centroids
from src.feature_engineering import compute_batch_features
from src.submission_validation import validate_submission

class TestPlanetHuntersPipeline(unittest.TestCase):

    def test_normalize_flux_1d(self):
        flux = np.array([100.0, 102.0, 98.0, 100.0, np.nan])
        rel = normalize_flux(flux)
        self.assertAlmostEqual(rel[0], 0.0, places=4)
        self.assertTrue(np.isnan(rel[4]))

    def test_process_centroids_shape(self):
        cen = np.random.randn(5, 2, 100).astype(np.float32)
        col_rel, row_rel, disp = process_centroids(cen)
        self.assertEqual(col_rel.shape, (5, 100))
        self.assertEqual(row_rel.shape, (5, 100))
        self.assertEqual(disp.shape, (5, 100))
        self.assertTrue(np.all(disp >= 0))

    def test_feature_extraction_no_nan(self):
        B, T = 10, 1315
        flux = np.ones((B, T), dtype=np.float32) * 1000.0 + np.random.randn(B, T) * 10
        cen = np.random.randn(B, 2, T).astype(np.float32) * 5
        stars = pd.DataFrame({
            "tmag": np.random.uniform(9, 15, B),
            "teff": np.random.uniform(4000, 7000, B),
            "logg": np.random.uniform(3.5, 5.0, B),
            "radius": np.random.uniform(0.5, 2.5, B),
            "contamination": np.random.uniform(0.0, 0.5, B),
        })
        cad = pd.DataFrame({
            "cadence": np.arange(T),
            "time_btjd": np.linspace(1000, 1027, T),
            "quality": np.zeros(T, dtype=int)
        })
        feats = compute_batch_features(flux, cen, stars, cad)
        self.assertEqual(feats.shape[0], B)
        self.assertFalse(feats.isnull().any().any())
        self.assertFalse(np.isinf(feats.values).any())

    def test_submission_validation_valid(self):
        sub_file = config.SUBMISSIONS_DIR / "submission.csv"
        if sub_file.exists():
            res = validate_submission(sub_file, verbose=False)
            self.assertTrue(res["passed_all"])

    def test_submission_v2_validation_valid(self):
        sub_v2 = config.SUBMISSIONS_DIR / "submission_v2.csv"
        if sub_v2.exists():
            res = validate_submission(sub_v2, verbose=False)
            self.assertTrue(res["passed_all"])

    def test_submission_v3_validation_valid(self):
        sub_v3 = config.SUBMISSIONS_DIR / "submission_v3.csv"
        if sub_v3.exists():
            res = validate_submission(sub_v3, verbose=False)
            self.assertTrue(res["passed_all"])

    def test_submission_v3_reproduced_valid_and_identical(self):
        sub_v3 = config.SUBMISSIONS_DIR / "submission_v3.csv"
        sub_v3_repr = config.SUBMISSIONS_DIR / "submission_v3_reproduced.csv"
        if sub_v3_repr.exists():
            res = validate_submission(sub_v3_repr, verbose=False)
            self.assertTrue(res["passed_all"])
            if sub_v3.exists():
                df_orig = pd.read_csv(sub_v3)
                df_repr = pd.read_csv(sub_v3_repr)
                self.assertTrue((df_orig["id"] == df_repr["id"]).all())
                self.assertTrue((df_orig["label"] == df_repr["label"]).all())

    def test_submission_FINAL_PHASE4_backup_valid_and_identical(self):
        sub_v3 = config.SUBMISSIONS_DIR / "submission_v3.csv"
        sub_backup = config.SUBMISSIONS_DIR / "submission_FINAL_PHASE4_BACKUP.csv"
        if sub_backup.exists():
            res = validate_submission(sub_backup, verbose=False)
            self.assertTrue(res["passed_all"])
            if sub_v3.exists():
                df_orig = pd.read_csv(sub_v3)
                df_backup = pd.read_csv(sub_backup)
                self.assertTrue((df_orig["id"] == df_backup["id"]).all())
                self.assertTrue((df_orig["label"] == df_backup["label"]).all())

    def test_submission_FINAL_valid_and_identical(self):
        sub_best = config.SUBMISSIONS_DIR / "submission_PHASE5_best.csv"
        sub_final = config.SUBMISSIONS_DIR / "submission_FINAL.csv"
        if sub_final.exists():
            res = validate_submission(sub_final, verbose=False)
            self.assertTrue(res["passed_all"])
            if sub_best.exists():
                df_best = pd.read_csv(sub_best)
                df_final = pd.read_csv(sub_final)
                self.assertTrue((df_best["id"] == df_final["id"]).all())
                self.assertTrue((df_best["label"] == df_final["label"]).all())

    def test_submission_PHASE6_candidate_valid(self):
        sub_p6 = config.SUBMISSIONS_DIR / "submission_PHASE6_candidate.csv"
        if sub_p6.exists():
            res = validate_submission(sub_p6, verbose=False)
            self.assertTrue(res["passed_all"])

    def test_submission_PHASE6_candidate_01_valid(self):
        sub_p6_01 = config.SUBMISSIONS_DIR / "submission_PHASE6_candidate_01.csv"
        if sub_p6_01.exists():
            res = validate_submission(sub_p6_01, verbose=False)
            self.assertTrue(res["passed_all"])

    def test_submission_PHASE7_candidate_01_valid(self):
        sub_p7_01 = config.SUBMISSIONS_DIR / "submission_PHASE7_candidate_01.csv"
        if sub_p7_01.exists():
            res = validate_submission(sub_p7_01, verbose=False)
            self.assertTrue(res["passed_all"])

if __name__ == "__main__":
    unittest.main()
