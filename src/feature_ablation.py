import os
import sys
import time
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, precision_recall_fscore_support
import lightgbm as lgb

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src import config
from src.data_loader import load_stars_metadata

def run_feature_ablation():
    print("=" * 65)
    print("PHASE 3: CONTROLLED FEATURE ABLATION EXPERIMENTS")
    print("=" * 65)

    train_feat_path = config.PROCESSED_DATA_DIR / "train_features.parquet"
    X = pd.read_parquet(train_feat_path)
    train_stars, _ = load_stars_metadata()
    y = train_stars["label"]

    X_tr, X_val, y_tr, y_val = train_test_split(
        X, y, test_size=0.20, stratify=y, random_state=config.RANDOM_SEED
    )

    all_cols = list(X.columns)
    print(f"Total Features: {len(all_cols)}")

    # Define the 7 functional feature groups
    group_1_flux = [c for c in all_cols if c in [
        "nan_frac", "flux_std", "flux_mad", "flux_min", "flux_max", "flux_range",
        "p01", "p05", "p10", "p25", "p75", "p90", "p95", "p99", "iqr", "robust_var",
        "flux_skew", "flux_kurt", "pos_frac", "neg_frac", "p99_norm", "p01_norm", "dip_to_peak_ratio"
    ]]

    group_2_transit = [c for c in all_cols if c in [
        "trend_std", "trend_range", "detrend_mad", "detrend_std", "spot_to_noise_ratio",
        "detrend_min", "detrend_p01", "detrend_dip_snr", "detrend_p01_p05_ratio",
        "detrend_bottom_cadences", "n_dips_3sigma", "n_dips_5sigma", "max_dip_depth",
        "dip_to_noise", "p01_to_p05_ratio", "p05_to_p25_ratio", "max_consecutive_dip"
    ]]

    group_3_centroid = [c for c in all_cols if c in [
        "col_std", "row_std", "disp_std", "disp_max", "disp_median", "cen_shift_in_dip",
        "cen_shift_ratio", "cen_shift_normalized", "cen_col_row_corr", "flux_cen_corr",
        "cen_jump_max", "cen_jump_mean"
    ]]

    group_4_periodicity = [c for c in all_cols if c in [
        "von_neumann_ratio", "autocorr_lag_1", "autocorr_lag_2", "autocorr_lag_4",
        "autocorr_lag_12", "autocorr_lag_24", "autocorr_lag_48", "low_freq_power_ratio",
        "fft_peak_freq_bin", "fft_peak_power", "spectral_entropy"
    ]]

    group_5_flares = [c for c in all_cols if c in [
        "n_flares_3sigma", "n_flares_5sigma", "max_flare_amp", "detrend_max_flare",
        "n_persistent_flares", "isolated_flare_ratio", "max_rise", "max_decay",
        "rise_decay_asym", "flare_dip_asym"
    ]]

    group_6_metadata = [c for c in all_cols if c in [
        "tmag", "teff", "logg", "radius", "contamination", "teff_over_radius",
        "logg_x_radius", "expected_noise_proxy", "excess_noise"
    ]]

    group_7_quality = [c for c in all_cols if c in [
        "flux_mad_dump", "disp_mean_dump", "dump_flux_anomaly"
    ]]

    groups = {
        "All 85 Features": all_cols,
        "Minus Group 1 (Flux Stats)": [c for c in all_cols if c not in group_1_flux],
        "Minus Group 2 (Detrended Transit)": [c for c in all_cols if c not in group_2_transit],
        "Minus Group 3 (Centroid Vetting)": [c for c in all_cols if c not in group_3_centroid],
        "Minus Group 4 (Periodicity & Freq)": [c for c in all_cols if c not in group_4_periodicity],
        "Minus Group 5 (Flare Features)": [c for c in all_cols if c not in group_5_flares],
        "Minus Group 6 (Stellar Metadata)": [c for c in all_cols if c not in group_6_metadata],
        "Minus Group 7 (Cadence Quality)": [c for c in all_cols if c not in group_7_quality],
    }

    results = []

    params = {
        "num_leaves": 63,
        "learning_rate": 0.035,
        "n_estimators": 600,
        "min_child_samples": 30,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "class_weight": "balanced",
        "random_state": 42,
        "n_jobs": -1,
        "verbose": -1
    }

    for name, cols in groups.items():
        print(f"\n--- Testing: {name} ({len(cols)} features) ---")
        t0 = time.time()
        model = lgb.LGBMClassifier(**params)
        model.fit(X_tr[cols], y_tr)
        fit_time = time.time() - t0

        preds = model.predict(X_val[cols])
        f1 = f1_score(y_val, preds, average="macro")

        # Per class
        prec, rec, per_f1, _ = precision_recall_fscore_support(
            y_val, preds, labels=config.CLASSES, zero_division=0
        )

        planet_f1 = per_f1[config.CLASSES.index("planet")]
        bg_f1 = per_f1[config.CLASSES.index("background_binary")]
        spots_f1 = per_f1[config.CLASSES.index("starspots")]
        glitch_f1 = per_f1[config.CLASSES.index("instrument_glitch")]

        diff_from_all = f1 - 0.5916
        print(f"  Macro F1: {f1:.4f} (Delta vs All: {diff_from_all:+.4f}) | Planet F1: {planet_f1:.4f} | BG F1: {bg_f1:.4f}")

        results.append({
            "experiment": name,
            "n_features": len(cols),
            "macro_f1": round(f1, 4),
            "delta_f1": round(diff_from_all, 4),
            "planet_f1": round(planet_f1, 4),
            "bg_binary_f1": round(bg_f1, 4),
            "starspots_f1": round(spots_f1, 4),
            "glitch_f1": round(glitch_f1, 4),
            "runtime_s": round(fit_time, 2)
        })

    ablation_df = pd.DataFrame(results)
    ablation_csv_path = config.REPORTS_DIR / "phase3_feature_ablation.csv"
    ablation_df.to_csv(ablation_csv_path, index=False)
    print(f"\nSaved ablation results to: {ablation_csv_path}")
    print("\n" + ablation_df.to_string(index=False))

if __name__ == "__main__":
    run_feature_ablation()
