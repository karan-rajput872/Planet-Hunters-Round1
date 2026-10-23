"""
Phase 5 Feature Engineering Module with Astro-Cotrending & Morphological Discriminators
Author: Senior ML Research Engineer & Computational Astrophysicist

This module implements:
1. Camera/CCD Systematic Cotrending (CBV removal) on flux and centroid channels.
2. Robust statistical features (MAD, percentiles, robust IQR ratios).
3. Detrended transit dip statistics (depth, U-shape bottom width, odd/even depth consistency).
4. Flare morphology metrics (asymmetric rise/decay, persistence vs single-cadence glitch).
5. Astrometric centroid correlation and shift-in-dip on clean cotrended coordinates.
6. Stellar metadata interactions.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import pandas as pd
from scipy import stats, ndimage
from typing import Dict, Tuple
from tqdm import tqdm

from src.preprocessing import normalize_flux, process_centroids
from src.phase5_cotrending import cotrend_lightcurves_and_centroids
from src import config

def extract_cotrended_features(
    flux_raw: np.ndarray,      # (N, T)
    cen_raw: np.ndarray,       # (N, 2, T)
    stars_df: pd.DataFrame,    # N rows
    cad_df: pd.DataFrame,      # T rows
    batch_size: int = 1500,
    desc: str = "Extracting Phase 5 features",
) -> pd.DataFrame:
    """
    Extracts features across the full dataset after performing camera/CCD cotrending.
    """
    N, T = flux_raw.shape
    print(f"[{desc}] Normalizing raw flux and centroids for {N} stars...")
    f_norm = normalize_flux(flux_raw).astype(np.float64)
    col_rel, row_rel, disp_rel = process_centroids(cen_raw)
    col_rel = col_rel.astype(np.float64)
    row_rel = row_rel.astype(np.float64)

    print(f"[{desc}] Applying Camera/CCD Cotrending (systematic drift subtraction)...")
    f_clean, col_clean, row_clean, disp_clean, _ = cotrend_lightcurves_and_centroids(
        f_norm, col_rel, row_rel, stars_df
    )

    # Cadence quality masks
    dump_mask = (cad_df["quality"].values & 1) > 0 # momentum dumps
    scatt_mask = (cad_df["quality"].values & 2) > 0 # scattered light
    gap_mask = (cad_df["quality"].values & 4) > 0 # data gaps

    feature_chunks = []

    for start_idx in tqdm(range(0, N, batch_size), desc=desc):
        end_idx = min(start_idx + batch_size, N)
        B = end_idx - start_idx

        f = f_clean[start_idx:end_idx]
        col = col_clean[start_idx:end_idx]
        row = row_clean[start_idx:end_idx]
        disp = disp_clean[start_idx:end_idx]
        stars_batch = stars_df.iloc[start_idx:end_idx]

        feats: Dict[str, np.ndarray] = {}

        # ==========================================
        # GROUP A — BASIC STATISTICAL DISTRIBUTIONS
        # ==========================================
        nan_mask = np.isnan(f)
        feats["nan_frac"] = np.mean(nan_mask, axis=1)

        f_med = np.nanmedian(f, axis=1, keepdims=True)
        abs_dev = np.abs(f - f_med)
        mad = np.nanmedian(abs_dev, axis=1)
        mad = np.where(mad < 1e-7, 1e-7, mad)
        mad_2d = mad[:, None]

        feats["flux_std"] = np.nanstd(f, axis=1)
        feats["flux_mad"] = mad
        feats["flux_min"] = np.nanmin(f, axis=1)
        feats["flux_max"] = np.nanmax(f, axis=1)
        feats["flux_range"] = feats["flux_max"] - feats["flux_min"]

        for q in [1, 5, 10, 25, 75, 90, 95, 99]:
            feats[f"p{q:02d}"] = np.nanpercentile(f, q, axis=1)

        feats["iqr"] = feats["p75"] - feats["p25"]
        feats["robust_var"] = (feats["p90"] - feats["p10"]) / (feats["iqr"] + 1e-8)
        feats["p99_norm"] = (feats["p99"] - feats["p75"]) / (feats["iqr"] + 1e-8)
        feats["p01_norm"] = (feats["p25"] - feats["p01"]) / (feats["iqr"] + 1e-8)
        feats["dip_to_peak_ratio"] = (feats["p25"] - feats["p01"]) / (feats["p99"] - feats["p75"] + 1e-8)

        feats["flux_skew"] = stats.skew(f, axis=1, nan_policy="omit")
        feats["flux_kurt"] = stats.kurtosis(f, axis=1, nan_policy="omit")

        feats["pos_frac"] = np.nanmean(f > (3.0 * mad_2d), axis=1)
        feats["neg_frac"] = np.nanmean(f < (-3.0 * mad_2d), axis=1)

        # ==========================================
        # GROUP B — LOCAL SMOOTHING & DETRENDING (STELLAR SPOTS & DIPS)
        # ==========================================
        f_filled = np.nan_to_num(f, nan=0.0)
        # 1-day running median filter
        f_trend = ndimage.median_filter(f_filled.astype(np.float32), size=(1, 49)).astype(np.float64)
        f_detrended = f_filled - f_trend
        f_detrended = np.where(nan_mask, np.nan, f_detrended)

        feats["trend_std"] = np.std(f_trend, axis=1)
        feats["trend_range"] = np.max(f_trend, axis=1) - np.min(f_trend, axis=1)

        detrend_mad = np.nanmedian(np.abs(f_detrended - np.nanmedian(f_detrended, axis=1, keepdims=True)), axis=1)
        detrend_mad = np.where(detrend_mad < 1e-7, 1e-7, detrend_mad)
        feats["detrend_mad"] = detrend_mad
        feats["detrend_std"] = np.nanstd(f_detrended, axis=1)
        feats["spot_to_noise_ratio"] = feats["trend_std"] / (feats["detrend_std"] + 1e-8)

        detrend_min = np.nanmin(f_detrended, axis=1)
        detrend_p01 = np.nanpercentile(f_detrended, 1, axis=1)
        detrend_p05 = np.nanpercentile(f_detrended, 5, axis=1)
        feats["detrend_min"] = detrend_min
        feats["detrend_p01"] = detrend_p01
        feats["detrend_dip_snr"] = -detrend_p01 / detrend_mad
        feats["detrend_p01_p05_ratio"] = detrend_p01 / (detrend_p05 - 1e-8)

        # U-shape vs V-shape bottom cadences
        cut_80 = detrend_min[:, None] * 0.8
        in_bottom_detrend = (f_detrended <= cut_80) & (~nan_mask)
        feats["detrend_bottom_cadences"] = np.sum(in_bottom_detrend, axis=1)

        # Dip statistics
        dip_3sigma = f < (-3.0 * mad_2d)
        dip_5sigma = f < (-5.0 * mad_2d)
        feats["n_dips_3sigma"] = np.nansum(dip_3sigma, axis=1)
        feats["n_dips_5sigma"] = np.nansum(dip_5sigma, axis=1)
        feats["max_dip_depth"] = -feats["flux_min"]
        feats["dip_to_noise"] = -feats["flux_min"] / mad
        feats["p01_to_p05_ratio"] = feats["p01"] / (feats["p05"] - 1e-8)
        feats["p05_to_p25_ratio"] = feats["p05"] / (feats["p25"] - 1e-8)

        # Run length of consecutive dip cadences
        run_lens = np.zeros(B, dtype=np.int32)
        current_run = np.zeros(B, dtype=np.int32)
        for t_idx in range(T):
            is_dip = dip_3sigma[:, t_idx]
            current_run = np.where(is_dip, current_run + 1, 0)
            run_lens = np.maximum(run_lens, current_run)
        feats["max_consecutive_dip"] = run_lens

        # ==========================================
        # GROUP C — TRANSIT VS ECLIPSING BINARY DISCRIMINATORS (NEW)
        # ==========================================
        # 1. Odd vs Even Dip Depth Ratio (Binaries have secondary eclipses with different depth)
        T_half = T // 2
        p01_first_half = np.nanpercentile(f_detrended[:, :T_half], 1, axis=1)
        p01_second_half = np.nanpercentile(f_detrended[:, T_half:], 1, axis=1)
        odd_even_ratio = np.minimum(np.abs(p01_first_half), np.abs(p01_second_half)) / (np.maximum(np.abs(p01_first_half), np.abs(p01_second_half)) + 1e-8)
        feats["odd_even_depth_ratio"] = odd_even_ratio

        # 2. Transit Duty Cycle (Planets < 0.05, Eclipsing Binaries 0.1 - 0.4)
        feats["transit_duty_cycle"] = feats["n_dips_3sigma"] / float(T)

        # 3. Dip Bottom Flatness (U-shape vs V-shape)
        feats["dip_bottom_flatness"] = feats["detrend_bottom_cadences"] / (feats["n_dips_3sigma"] + 1e-8)

        # ==========================================
        # GROUP D — STELLAR FLARES VS GLITCHES
        # ==========================================
        flare_3sigma = f > (3.0 * mad_2d)
        flare_5sigma = f > (5.0 * mad_2d)
        feats["n_flares_3sigma"] = np.nansum(flare_3sigma, axis=1)
        feats["n_flares_5sigma"] = np.nansum(flare_5sigma, axis=1)
        feats["max_flare_amp"] = feats["flux_max"] / mad
        feats["detrend_max_flare"] = np.nanmax(f_detrended, axis=1) / detrend_mad

        persistent_flares = flare_3sigma[:, :-1] & flare_3sigma[:, 1:]
        feats["n_persistent_flares"] = np.sum(persistent_flares, axis=1)
        feats["isolated_flare_ratio"] = (feats["n_flares_3sigma"] - 2 * feats["n_persistent_flares"]).clip(min=0) / (feats["n_flares_3sigma"] + 1e-8)

        df_forward = f_filled[:, 1:] - f_filled[:, :-1]
        feats["max_rise"] = np.max(df_forward, axis=1) / mad
        feats["max_decay"] = -np.min(df_forward, axis=1) / mad
        feats["rise_decay_asym"] = (feats["max_rise"] - feats["max_decay"]) / (feats["max_rise"] + feats["max_decay"] + 1e-8)
        feats["flare_dip_asym"] = (feats["max_flare_amp"] - feats["dip_to_noise"]) / (feats["max_flare_amp"] + feats["dip_to_noise"] + 1e-8)

        # ==========================================
        # GROUP E — TIME-SERIES DYNAMICS & PERIODICITY
        # ==========================================
        sq_diff = np.sum(df_forward**2, axis=1, dtype=np.float64)
        var_flux = np.nanvar(f, axis=1, dtype=np.float64) * T
        feats["von_neumann_ratio"] = sq_diff / (2.0 * var_flux + 1e-8)

        f_norm_centered = f_filled - np.mean(f_filled, axis=1, keepdims=True)
        denom = np.sum(f_norm_centered**2, axis=1, dtype=np.float64) + 1e-8
        for lag in [1, 2, 4, 12, 24, 48]:
            ac = np.sum(f_norm_centered[:, :-lag] * f_norm_centered[:, lag:], axis=1, dtype=np.float64) / denom
            feats[f"autocorr_lag_{lag}"] = ac

        # FFT Spectrum
        fft_vals = np.abs(np.fft.rfft(f_norm_centered, axis=1))[:, 1:]
        total_power = np.sum(fft_vals**2, axis=1, dtype=np.float64) + 1e-8
        low_freq_power = np.sum(fft_vals[:, :27]**2, axis=1, dtype=np.float64) / total_power
        feats["low_freq_power_ratio"] = low_freq_power

        peak_bin = np.argmax(fft_vals, axis=1)
        feats["fft_peak_freq_bin"] = peak_bin
        feats["fft_peak_power"] = np.max(fft_vals**2, axis=1) / total_power

        prob_fft = (fft_vals**2) / total_power[:, None] + 1e-12
        feats["spectral_entropy"] = -np.sum(prob_fft * np.log(prob_fft), axis=1, dtype=np.float64)

        # ==========================================
        # GROUP F — COTRENDED CENTROIDS & ASTROMETRY
        # ==========================================
        feats["col_std"] = np.nanstd(col, axis=1)
        feats["row_std"] = np.nanstd(row, axis=1)
        feats["disp_std"] = np.nanstd(disp, axis=1)
        feats["disp_max"] = np.nanmax(disp, axis=1)
        feats["disp_median"] = np.nanmedian(disp, axis=1)

        disp_filled = np.nan_to_num(disp, nan=0.0)
        in_dip_mask = (f < feats["p05"][:, None]) & (~nan_mask)
        out_dip_mask = (f >= feats["p25"][:, None]) & (f <= feats["p75"][:, None]) & (~nan_mask)

        dip_disp_sum = np.sum(np.where(in_dip_mask, disp_filled, 0.0), axis=1, dtype=np.float64)
        dip_disp_cnt = np.sum(in_dip_mask, axis=1, dtype=np.float64) + 1e-8
        mean_disp_in_dip = dip_disp_sum / dip_disp_cnt

        out_disp_sum = np.sum(np.where(out_dip_mask, disp_filled, 0.0), axis=1, dtype=np.float64)
        out_disp_cnt = np.sum(out_dip_mask, axis=1, dtype=np.float64) + 1e-8
        mean_disp_out_dip = out_disp_sum / out_disp_cnt

        feats["cen_shift_in_dip"] = mean_disp_in_dip - mean_disp_out_dip
        feats["cen_shift_ratio"] = mean_disp_in_dip / (mean_disp_out_dip + 1e-8)
        feats["cen_shift_normalized"] = feats["cen_shift_in_dip"] / (feats["disp_std"] + 1e-4)

        col_filled = np.nan_to_num(col, nan=0.0)
        row_filled = np.nan_to_num(row, nan=0.0)
        col_norm = col_filled - np.mean(col_filled, axis=1, keepdims=True)
        row_norm = row_filled - np.mean(row_filled, axis=1, keepdims=True)
        col_row_cov = np.sum(col_norm * row_norm, axis=1, dtype=np.float64)
        col_row_denom = np.sqrt(np.sum(col_norm**2, axis=1) * np.sum(row_norm**2, axis=1)) + 1e-8
        feats["cen_col_row_corr"] = col_row_cov / col_row_denom

        disp_norm_arr = disp_filled - np.mean(disp_filled, axis=1, keepdims=True)
        disp_denom = np.sqrt(np.sum(disp_norm_arr**2, axis=1, dtype=np.float64) * denom) + 1e-8
        feats["flux_cen_corr"] = np.sum(f_norm_centered * disp_norm_arr, axis=1, dtype=np.float64) / disp_denom

        d_disp = np.abs(disp_filled[:, 1:] - disp_filled[:, :-1])
        feats["cen_jump_max"] = np.max(d_disp, axis=1)
        feats["cen_jump_mean"] = np.mean(d_disp, axis=1)

        # ==========================================
        # GROUP G — CADENCE QUALITY & ARTIFACTS
        # ==========================================
        if np.any(dump_mask):
            feats["flux_mad_dump"] = np.nanmedian(np.abs(f[:, dump_mask]), axis=1)
            feats["disp_mean_dump"] = np.nanmean(disp[:, dump_mask], axis=1)
        else:
            feats["flux_mad_dump"] = np.zeros(B)
            feats["disp_mean_dump"] = np.zeros(B)

        feats["dump_flux_anomaly"] = feats["flux_mad_dump"] / mad

        # ==========================================
        # GROUP H — STELLAR METADATA & PHYSICAL RELATIONS
        # ==========================================
        meta = stars_batch[["tmag", "teff", "logg", "radius", "contamination"]].copy().reset_index(drop=True)
        meta["teff_over_radius"] = meta["teff"] / (meta["radius"] + 1e-4)
        meta["logg_x_radius"] = meta["logg"] * meta["radius"]
        meta["expected_noise_proxy"] = 10.0 ** (0.2 * (meta["tmag"].clip(upper=20.0) - 10.0))
        meta["excess_noise"] = feats["flux_std"] / (meta["expected_noise_proxy"] + 1e-8)

        feat_df = pd.DataFrame(feats)
        full_batch = pd.concat([feat_df, meta], axis=1)
        full_batch = full_batch.replace([np.inf, -np.inf], np.nan).fillna(0.0)
        feature_chunks.append(full_batch)

    result_df = pd.concat(feature_chunks, ignore_index=True)
    return result_df

def compute_phase5_features(force_recompute: bool = False):
    from src.data_loader import load_flux_arrays, load_centroid_arrays, load_stars_metadata, load_cadences

    train_path = config.PROCESSED_DATA_DIR / "train_features_v5.parquet"
    test_path = config.PROCESSED_DATA_DIR / "test_features_v5.parquet"

    if not force_recompute and train_path.exists() and test_path.exists():
        print(f"[CACHE] Loading Phase 5 features from {train_path} and {test_path}...")
        tr = pd.read_parquet(train_path)
        te = pd.read_parquet(test_path)
        print(f"[CACHE] Loaded train: {tr.shape}, test: {te.shape}")
        return tr, te

    print("[PHASE 5] Extracting Cotrended Feature Matrix...")
    train_flux, test_flux = load_flux_arrays()
    train_cen, test_cen = load_centroid_arrays()
    train_stars, test_stars = load_stars_metadata()
    train_cad, test_cad = load_cadences()

    tr_df = extract_cotrended_features(train_flux, train_cen, train_stars, train_cad, desc="Train Phase 5")
    te_df = extract_cotrended_features(test_flux, test_cen, test_stars, test_cad, desc="Test Phase 5")

    print(f"[SAVE] Saving Phase 5 features to {train_path} and {test_path}...")
    tr_df.to_parquet(train_path, index=False)
    te_df.to_parquet(test_path, index=False)
    print(f"[SAVE] Done! Train: {tr_df.shape}, Test: {te_df.shape}")
    return tr_df, te_df

if __name__ == "__main__":
    compute_phase5_features(force_recompute=True)
