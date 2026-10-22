"""
Data Loader and State Management for Mission Control Dashboard
Strictly read-only access to submissions/submission_FINAL.csv and evaluation artifacts.
"""

from pathlib import Path
import sys
import pandas as pd
import streamlit as st

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.submission_validation import validate_submission

SUBMISSION_FILE = PROJECT_ROOT / "submissions" / "submission_FINAL.csv"

# Actual Project Reported Metrics (Strictly non-fabricated, from docs/MODEL_EVALUATION.md)
PROJECT_METRICS = {
    "champion_oof_f1": 0.5915,
    "cv_mean_f1": 0.5914,
    "cv_std_f1": 0.0020,
    "champion_holdout_f1": 0.5956,
    "training_stars": 18000,
    "test_stars": 7000,
    "flux_cadences": 1315,
    "classes_count": 8,
    "metric_name": "Macro F1"
}

# Model Benchmarks for Comparison Visualization (from reports/model_comparison.csv & docs)
MODEL_BENCHMARKS = [
    {"model": "ExtraTrees (Baseline)", "macro_f1": 0.5234, "category": "Random Split Forest", "type": "Holdout Baseline"},
    {"model": "CatBoost", "macro_f1": 0.5512, "category": "Symmetric Oblivious Trees", "type": "Holdout Benchmark"},
    {"model": "HistGradientBoosting", "macro_f1": 0.5709, "category": "Depth-Wise Histogram GBDT", "type": "Holdout Benchmark"},
    {"model": "LightGBM (Single)", "macro_f1": 0.5914, "category": "Tuned Leaf-Wise GBDT", "type": "Holdout Benchmark"},
    {"model": "Champion Dual Ensemble", "macro_f1": 0.5956, "category": "5-Fold LGBM (75%) + HistGB (25%)", "type": "Holdout Champion"}
]

# Verified Per-Class Validation Breakdown (from docs/MODEL_EVALUATION.md, Section 4)
CLASS_EVALUATION_METRICS = [
    {"class": "instrument_glitch", "display": "Instrument Glitch", "precision": 0.8159, "recall": 0.6851, "f1": 0.7448, "support": 1721},
    {"class": "eclipsing_binary", "display": "Eclipsing Binary", "precision": 0.8463, "recall": 0.6422, "f1": 0.7303, "support": 2247},
    {"class": "pulsating_star", "display": "Pulsating Star", "precision": 0.7136, "recall": 0.6214, "f1": 0.6643, "support": 1973},
    {"class": "quiet_star", "display": "Quiet Star", "precision": 0.4785, "recall": 0.7762, "f1": 0.5920, "support": 3624},
    {"class": "background_binary", "display": "Background Binary", "precision": 0.6396, "recall": 0.4813, "f1": 0.5493, "support": 1604},
    {"class": "flare_star", "display": "Flare Star", "precision": 0.6478, "recall": 0.4446, "f1": 0.5273, "support": 1804},
    {"class": "planet", "display": "Exoplanet Transit", "precision": 0.5068, "recall": 0.4345, "f1": 0.4679, "support": 2145},
    {"class": "starspots", "display": "Starspot Modulation", "precision": 0.4493, "recall": 0.4629, "f1": 0.4560, "support": 2882},
]

# Verified Feature Group Ablation Evidence (from docs/MODEL_EVALUATION.md, Section 5)
FEATURE_GROUP_ABLATIONS = [
    {"group": "Full Pipeline (All Features)", "features": 85, "oof_f1": 0.5915, "delta": "+0.0000", "note": "Optimal balanced baseline"},
    {"group": "Minus Detrending & Transits", "features": 71, "oof_f1": 0.5670, "delta": "-0.0245", "note": "Planet F1 collapses from 0.4679 to 0.3776 (-0.0903)"},
    {"group": "Minus Periodicity & FFT", "features": 75, "oof_f1": 0.5832, "delta": "-0.0083", "note": "Pulsating star F1 drops by -0.0412"},
    {"group": "Minus Centroid Vetting", "features": 74, "oof_f1": 0.5844, "delta": "-0.0071", "note": "Background binary precision degrades"},
    {"group": "Minus Stellar Meta (Teff, logg)", "features": 76, "oof_f1": 0.5861, "delta": "-0.0054", "note": "Quiet star separation blurs"},
]

# Exact Astrophysical and Instrumental Class Definitions & Descriptions
CLASS_METADATA = {
    "pulsating_star": {
        "display": "Pulsating Star",
        "description": "Intrinsic stellar pulsations (Cepheids, RR Lyrae, Delta Scuti) with coherent Fourier periodic oscillations.",
        "scientific_type": "Intrinsic Variable",
        "signal_shape": "Continuous periodic sinusoidal / multi-periodic modes"
    },
    "instrument_glitch": {
        "display": "Instrument Glitch",
        "description": "Detector anomalies, cosmic ray hits, spacecraft thruster firings, and instantaneous focus drift artifacts.",
        "scientific_type": "Technical Artifact",
        "signal_shape": "Sharp single-point impulse discontinuity"
    },
    "quiet_star": {
        "display": "Quiet / Inactive Star",
        "description": "Photometrically quiet stellar targets with Gaussian photon shot noise and absence of periodic dips.",
        "scientific_type": "Constant Star",
        "signal_shape": "Flat lightcurve within observational noise floor"
    },
    "starspots": {
        "display": "Starspot Modulation",
        "description": "Stellar magnetic activity producing quasi-periodic sinusoidal or rotating photometric modulations.",
        "scientific_type": "Stellar Activity",
        "signal_shape": "Low-frequency quasi-sinusoidal rotational wave"
    },
    "eclipsing_binary": {
        "display": "Eclipsing Binary",
        "description": "Gravitationally bound binary systems exhibiting alternating deep primary and secondary V-shaped eclipses.",
        "scientific_type": "Stellar Eclipse",
        "signal_shape": "Deep, alternating primary and secondary flux minima"
    },
    "planet": {
        "display": "Exoplanet Transit",
        "description": "Planetary transits showing periodic, flat-bottomed U-shaped dips with zero centroid motion during transit.",
        "scientific_type": "Astrophysical Transit",
        "signal_shape": "Periodic flat-bottomed square dip (SNR > 3)"
    },
    "flare_star": {
        "display": "Stellar Flare",
        "description": "Violent magnetic reconnection events featuring rapid, asymmetric flux spikes with exponential cooling decay.",
        "scientific_type": "Magnetic Eruption",
        "signal_shape": "Instantaneous positive spike followed by exponential tail"
    },
    "background_binary": {
        "display": "Background Binary",
        "description": "Background false positive where an off-target binary blends into the aperture, flagged via centroid shift in dip.",
        "scientific_type": "False Positive",
        "signal_shape": "Transit-like dip accompanied by significant spatial centroid drift"
    }
}

@st.cache_data
def load_submission_data():
    """Load the final validated submission CSV in read-only mode."""
    if not SUBMISSION_FILE.exists():
        raise FileNotFoundError(f"Final submission file not found: {SUBMISSION_FILE}")

    df = pd.read_csv(SUBMISSION_FILE)
    return df

@st.cache_data
def get_class_summary():
    """Get exact counts and percentages from submission_FINAL.csv ordered by count."""
    df = load_submission_data()
    counts = df["label"].value_counts().to_dict()
    total = len(df)

    # Strictly preserve official ranking
    class_order = [
        "pulsating_star", "instrument_glitch", "quiet_star", "starspots",
        "eclipsing_binary", "planet", "flare_star", "background_binary"
    ]

    summary = []
    for cls in class_order:
        meta = CLASS_METADATA[cls]
        count = counts.get(cls, 0)
        pct = (count / total) * 100.0 if total > 0 else 0.0
        summary.append({
            "class": cls,
            "display": meta["display"],
            "count": count,
            "percentage": pct,
            "type": meta["scientific_type"],
            "description": meta["description"],
            "signal_shape": meta["signal_shape"]
        })

    summary_df = pd.DataFrame(summary)
    return summary_df

def run_submission_validation():
    """Executes the strict 14-check validator directly without altering files."""
    return validate_submission(SUBMISSION_FILE, verbose=False)
