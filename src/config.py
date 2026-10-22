import os
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODELS_DIR = PROJECT_ROOT / "models"
SUBMISSIONS_DIR = PROJECT_ROOT / "submissions"
REPORTS_DIR = PROJECT_ROOT / "reports"
LOGS_DIR = PROJECT_ROOT / "logs"

# Ensure runtime directories exist
for d in [PROCESSED_DATA_DIR, MODELS_DIR, SUBMISSIONS_DIR, REPORTS_DIR, LOGS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Raw files
TRAIN_FLUX_FILE = RAW_DATA_DIR / "train_flux.npy"
TRAIN_CENTROID_FILE = RAW_DATA_DIR / "train_centroid.npy"
TRAIN_STARS_FILE = RAW_DATA_DIR / "train_stars.csv"
TRAIN_CADENCES_FILE = RAW_DATA_DIR / "train_cadences.csv"

TEST_FLUX_FILE = RAW_DATA_DIR / "test_flux.npy"
TEST_CENTROID_FILE = RAW_DATA_DIR / "test_centroid.npy"
TEST_STARS_FILE = RAW_DATA_DIR / "test_stars.csv"
TEST_CADENCES_FILE = RAW_DATA_DIR / "test_cadences.csv"
SAMPLE_SUBMISSION_FILE = RAW_DATA_DIR / "sample_submission.csv"

# Target classes in defined order
CLASSES = [
    "planet",
    "eclipsing_binary",
    "background_binary",
    "starspots",
    "pulsating_star",
    "flare_star",
    "instrument_glitch",
    "quiet_star",
]

CLASS_TO_IDX = {cls_name: idx for idx, cls_name in enumerate(CLASSES)}
IDX_TO_CLASS = {idx: cls_name for idx, cls_name in enumerate(CLASSES)}

# Constants
CADENCES_PER_STAR = 1315
RANDOM_SEED = 42
N_JOBS = -1
