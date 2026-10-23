"""
Planet Hunters — Scientific Data Loader & State Management
Provides robust, read-only access to submissions/submission_FINAL.csv and evaluation artifacts.
Features non-crashing graceful fallbacks and zero-leakage compliance.
"""

from pathlib import Path
import sys
import pandas as pd
import streamlit as st

# Robust absolute path resolution derived from this file's location
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import logging
from src.submission_validation import validate_submission
from src import config

logger = logging.getLogger(__name__)

SUBMISSION_FILE = PROJECT_ROOT / "submissions" / "submission_FINAL.csv"

# Verified Project Metrics (Strictly non-fabricated, from docs/MODEL_EVALUATION.md)
PROJECT_METRICS = {
    "champion_oof_f1": 0.6455,
    "detector_oof_f1": 0.6336,
    "cv_mean_f1": 0.6455,
    "cv_std_f1": 0.0020,
    "phase4_oof_f1": 0.5915,
    "phase4_public_lb": 0.4214,
    "training_stars": 18000,
    "test_stars": 7000,
    "flux_cadences": 1315,
    "classes_count": 8,
    "features_count": 88,
    "metric_name": "Macro F1",
    "ensemble_lgb": 0.50,
    "ensemble_hgb": 0.40,
    "ensemble_cb": 0.10
}

# Model Benchmarks for Comparison Visualization (from reports/model_comparison.csv & docs)
MODEL_BENCHMARKS = [
    {"model": "ExtraTrees (Baseline)", "macro_f1": 0.5234, "category": "Random Split Forest", "type": "Holdout Baseline"},
    {"model": "CatBoost (Baseline)", "macro_f1": 0.5512, "category": "Symmetric Oblivious Trees", "type": "Holdout Benchmark"},
    {"model": "HistGradientBoosting", "macro_f1": 0.5709, "category": "Depth-Wise Histogram GBDT", "type": "Holdout Benchmark"},
    {"model": "LightGBM (Single)", "macro_f1": 0.5914, "category": "Tuned Leaf-Wise GBDT", "type": "Holdout Benchmark"},
    {"model": "Phase 4 Dual Ensemble", "macro_f1": 0.5915, "category": "5-Fold LGBM (75%) + HistGB (25%)", "type": "Phase 4 Baseline"},
    {"model": "Phase 5 Dual Ensemble", "macro_f1": 0.6438, "category": "5-Fold LGBM (75%) + HistGB (25%) [Cotrended]", "type": "Phase 5 Candidate"},
    {"model": "Phase 5 Tri-Ensemble (Promoted Champion)", "macro_f1": 0.6455, "category": "5-Fold LGB (50%) + HGB (40%) + CB (10%) [Cotrended]", "type": "Promoted Champion"}
]

# Verified Per-Class Validation Breakdown (from Phase 5 Classification Report, 18,000 stars)
CLASS_EVALUATION_METRICS = [
    {"class": "instrument_glitch", "display": "Instrument Glitch", "precision": 0.8505, "recall": 0.7902, "f1": 0.8193, "support": 1721},
    {"class": "eclipsing_binary", "display": "Eclipsing Binary", "precision": 0.8487, "recall": 0.6667, "f1": 0.7468, "support": 2247},
    {"class": "pulsating_star", "display": "Pulsating Star", "precision": 0.8313, "recall": 0.6670, "f1": 0.7402, "support": 1973},
    {"class": "flare_star", "display": "Flare Star", "precision": 0.7980, "recall": 0.5715, "f1": 0.6660, "support": 1804},
    {"class": "quiet_star", "display": "Quiet Star", "precision": 0.4934, "recall": 0.8331, "f1": 0.6197, "support": 3624},
    {"class": "background_binary", "display": "Background Binary", "precision": 0.6980, "recall": 0.4956, "f1": 0.5797, "support": 1604},
    {"class": "starspots", "display": "Starspot Modulation", "precision": 0.5316, "recall": 0.5344, "f1": 0.5330, "support": 2882},
    {"class": "planet", "display": "Exoplanet Transit", "precision": 0.5361, "recall": 0.4014, "f1": 0.4591, "support": 2145},
]

# Verified Feature Group Ablation Evidence (from docs/MODEL_EVALUATION.md, Section 5)
FEATURE_GROUP_ABLATIONS = [
    {"group": "Full Cotrended Pipeline (88 Features)", "features": 88, "oof_f1": 0.6455, "delta": "+0.0000", "note": "Optimal tri-ensemble champion with CCD cotrending"},
    {"group": "Without Cotrending (Phase 4 Base)", "features": 85, "oof_f1": 0.5915, "delta": "-0.0540", "note": "Severe camera systematic drift degrades generalizability"},
    {"group": "Minus Detrending & Transit BLS", "features": 71, "oof_f1": 0.5670, "delta": "-0.0785", "note": "Planet F1 collapses from 0.46 to 0.37"},
    {"group": "Minus Periodicity & Fourier Power", "features": 75, "oof_f1": 0.5832, "delta": "-0.0623", "note": "Pulsating star F1 degrades significantly"},
    {"group": "Minus Centroid Vetting (Astrometry)", "features": 74, "oof_f1": 0.5844, "delta": "-0.0611", "note": "Background binary false-positive confusion escalates"},
    {"group": "Minus Stellar Metadata (Teff, logg)", "features": 76, "oof_f1": 0.5861, "delta": "-0.0594", "note": "Quiet star and dwarf separation blurs"}
]

# Exact Verified Empirical Class Counts from Official 7,000-sample submission_FINAL.csv
VERIFIED_TEST_CLASS_COUNTS = {
    "quiet_star": 1912,
    "starspots": 1122,
    "planet": 793,
    "pulsating_star": 785,
    "instrument_glitch": 777,
    "eclipsing_binary": 685,
    "flare_star": 505,
    "background_binary": 421,
}

# Exact Astrophysical and Instrumental Class Definitions & Descriptions
CLASS_METADATA = {
    "planet": {
        "display": "Exoplanet Transit",
        "description": "Periodic, flat-bottomed U-shaped dips with negligible centroid displacement during transit.",
        "scientific_type": "Astrophysical Transit",
        "signal_shape": "Periodic flat-bottomed square dip (SNR > 3)",
        "diagnostic_marker": "Zero in-dip centroid shift (Δcentroid ≈ 0)"
    },
    "eclipsing_binary": {
        "display": "Eclipsing Binary",
        "description": "Gravitationally bound stellar binary systems showing alternating primary and secondary V-shaped eclipses.",
        "scientific_type": "Stellar Eclipse",
        "signal_shape": "Deep, alternating primary and secondary flux minima",
        "diagnostic_marker": "Deep alternating eclipse depths"
    },
    "background_binary": {
        "display": "Background Binary",
        "description": "Unrelated off-target binary blending into the aperture; exhibits deep dips accompanied by significant centroid shifts.",
        "scientific_type": "Astrophysical False Positive",
        "signal_shape": "Transit-like dip with simultaneous spatial centroid shift",
        "diagnostic_marker": "Significant in-dip centroid offset (Δcentroid > 3σ)"
    },
    "starspots": {
        "display": "Starspot Modulation",
        "description": "Stellar magnetic activity producing quasi-periodic sinusoidal or rotating photometric modulations.",
        "scientific_type": "Stellar Activity",
        "signal_shape": "Low-frequency quasi-sinusoidal rotational wave",
        "diagnostic_marker": "Smooth rotational modulation matching stellar rotation"
    },
    "pulsating_star": {
        "display": "Pulsating Star",
        "description": "Intrinsic stellar pulsations (Cepheids, RR Lyrae, Delta Scuti) with coherent Fourier periodic harmonics.",
        "scientific_type": "Intrinsic Variable",
        "signal_shape": "Continuous periodic sinusoidal / multi-periodic modes",
        "diagnostic_marker": "High Fourier peak power & discrete frequency peaks"
    },
    "flare_star": {
        "display": "Stellar Flare",
        "description": "Magnetic reconnection events displaying rapid, asymmetric flux spikes followed by exponential cooling decay.",
        "scientific_type": "Magnetic Eruption",
        "signal_shape": "Instantaneous positive spike with exponential decay",
        "diagnostic_marker": "Positive flux skewness & rapid rise with slow tail"
    },
    "instrument_glitch": {
        "display": "Instrument Glitch",
        "description": "Detector anomalies, cosmic ray hits, spacecraft thruster firings, and instantaneous focus drift artifacts.",
        "scientific_type": "Technical Artifact",
        "signal_shape": "Sharp single-point impulse discontinuity",
        "diagnostic_marker": "Extreme Von Neumann ratio & unphysical single-epoch jump"
    },
    "quiet_star": {
        "display": "Quiet / Inactive Star",
        "description": "Photometrically stable stellar targets with Gaussian photon shot noise and no significant periodic variability.",
        "scientific_type": "Constant Star",
        "signal_shape": "Flat light curve within observational noise floor",
        "diagnostic_marker": "Gaussian flux distribution & near-zero variability index"
    }
}

@st.cache_data(show_spinner=False)
def load_submission_data():
    """
    Safely load the final validated submission CSV in read-only mode.
    Returns DataFrame if found, or None if intentionally absent from deployment.
    NEVER raises an unhandled FileNotFoundError to the user.
    """
    try:
        if SUBMISSION_FILE.is_file():
            df = pd.read_csv(SUBMISSION_FILE)
            return df
    except Exception as e:
        print(f"[WARN] Error reading {SUBMISSION_FILE}: {e}")
    return None

@st.cache_data(show_spinner=False)
def get_class_summary():
    """
    Get exact counts and percentages for test set classifications.
    Uses real CSV when available, or verified empirical counts fallback.
    Guaranteed to return a complete, valid DataFrame without throwing exceptions.
    """
    df = load_submission_data()

    if df is not None and "label" in df.columns:
        counts = df["label"].value_counts().to_dict()
        total = len(df)
    else:
        counts = VERIFIED_TEST_CLASS_COUNTS.copy()
        total = sum(counts.values())

    class_order = [
        "planet",
        "eclipsing_binary",
        "background_binary",
        "starspots",
        "pulsating_star",
        "flare_star",
        "instrument_glitch",
        "quiet_star"
    ]

    summary = []
    for cls in class_order:
        meta = CLASS_METADATA.get(cls, {
            "display": cls.replace("_", " ").title(),
            "description": "Astronomical phenomenon.",
            "scientific_type": "Phenomenon",
            "signal_shape": "Light-curve signature",
            "diagnostic_marker": "Photometric marker"
        })
        count = counts.get(cls, 0)
        pct = (count / total) * 100.0 if total > 0 else 0.0
        summary.append({
            "class": cls,
            "display": meta["display"],
            "count": count,
            "percentage": pct,
            "type": meta["scientific_type"],
            "description": meta["description"],
            "signal_shape": meta["signal_shape"],
            "diagnostic_marker": meta.get("diagnostic_marker", "")
        })

    return pd.DataFrame(summary)

def run_submission_validation(submission_path=None, test_stars_path=None):
    """
    Executes the decoupled submission validator.
    Never raises an unhandled exception or raw traceback.
    """
    sub_file = Path(submission_path or SUBMISSION_FILE).resolve()
    test_file = Path(test_stars_path or config.TEST_STARS_FILE).resolve()

    if sub_file.is_file():
        try:
            return validate_submission(sub_file, test_stars_path=test_file, verbose=False)
        except Exception as e:
            logger.error(f"Validator execution error: {e}", exc_info=True)
            return {
                "file": sub_file.name,
                "path": str(sub_file),
                "status": "FAILED",
                "passed_all": False,
                "artifact_checks_passed": False,
                "test_data_status": "FAILED",
                "failures": [f"Validator execution error: {e}"],
                "warnings": [],
                "blocked": [],
                "class_distribution": {}
            }

    return {
        "file": sub_file.name,
        "path": str(sub_file),
        "status": "FAILED",
        "passed_all": False,
        "artifact_checks_passed": False,
        "test_data_status": "NOT_RUN",
        "failures": [f"Submission file not found at {sub_file.name}"],
        "warnings": [],
        "blocked": [],
        "class_distribution": {}
    }
