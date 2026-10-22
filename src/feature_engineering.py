import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import pandas as pd
from scipy import stats, ndimage
from typing import Dict
from tqdm import tqdm
from src.preprocessing import normalize_flux, process_centroids
from src import config

def compute_batch_features(
    flux_batch: np.ndarray,      # (B, T)
    cen_batch: np.ndarray,       # (B, 2, T)
    stars_batch: pd.DataFrame,   # B rows
    cad_df: pd.DataFrame,        # T rows
) -> pd.DataFrame:
    """
    Computes comprehensive, vectorized features for a batch of stars.
    flux_batch: raw flux array
    cen_batch: raw centroid array (B, 2, T)
    stars_batch: metadata dataframe
    cad_df: cadences dataframe (quality flags, time)
    """
    B, T = flux_batch.shape

    # 1. Normalization & Preprocessing in float64 for stability
    f = normalize_flux(flux_batch).astype(np.float64) # relative flux: (B, T)
    col_rel, row_rel, disp = process_centroids(cen_batch)
    col_rel = col_rel.astype(np.float64)
    row_rel = row_rel.astype(np.float64)
    disp = disp.astype(np.float64)

    # Cadence quality masks
    dump_mask = (cad_df["quality"].values & 1) > 0 # momentum dumps
    scatt_mask = (cad_df["quality"].values & 2) > 0 # scattered light
    gap_mask = (cad_df["quality"].values & 4) > 0 # data gaps

    features: Dict[str, np.ndarray] = {}

    # ==========================================
    # GROUP A — BASIC FLUX STATISTICS
    # ==========================================
    nan_mask = np.isnan(f)
    features["nan_frac"] = np.mean(nan_mask, axis=1)

    # Nan-safe medians and MAD
    f_med = np.nanmedian(f, axis=1, keepdims=True)
    abs_dev = np.abs(f - f_med)
    mad = np.nanmedian(abs_dev, axis=1)
    mad = np.where(mad < 1e-7, 1e-7, mad) # avoid div by zero
    mad_2d = mad[:, None]

    features["flux_std"] = np.nanstd(f, axis=1)
    features["flux_mad"] = mad
    features["flux_min"] = np.nanmin(f, axis=1)
    features["flux_max"] = np.nanmax(f, axis=1)
    features["flux_range"] = features["flux_max"] - features["flux_min"]

    # Percentiles
    for q in [1, 5, 10, 25, 75, 90, 95, 99]:
        features[f"p{q:02d}"] = np.nanpercentile(f, q, axis=1)

    features["iqr"] = features["p75"] - features["p25"]
    features["robust_var"] = (features["p90"] - features["p10"]) / (features["iqr"] + 1e-8)

    # Domain-shift invariant percentile ratios
    features["p99_norm"] = (features["p99"] - features["p75"]) / (features["iqr"] + 1e-8)
    features["p01_norm"] = (features["p25"] - features["p01"]) / (features["iqr"] + 1e-8)
    features["dip_to_peak_ratio"] = (features["p25"] - features["p01"]) / (features["p99"] - features["p75"] + 1e-8)

    # Skewness & Kurtosis
    features["flux_skew"] = stats.skew(f, axis=1, nan_policy="omit")
    features["flux_kurt"] = stats.kurtosis(f, axis=1, nan_policy="omit")

    # Positive / Negative deviation fractions
    features["pos_frac"] = np.nanmean(f > (3.0 * mad_2d), axis=1)
    features["neg_frac"] = np.nanmean(f < (-3.0 * mad_2d), axis=1)

    # ==========================================
    # GROUP B & DETRENDING — TRANSIT SEARCH & STELLAR SPOTS
    # ==========================================
    f_filled = np.nan_to_num(f, nan=0.0)
    # Fast 2D median filter for stellar trend (window ~ 49 cadences = 24.5 hours = 1 day)
    f_trend = ndimage.median_filter(f_filled.astype(np.float32), size=(1, 49)).astype(np.float64)
    f_detrended = f_filled - f_trend
    # Mask out gaps from detrended calculations
    f_detrended = np.where(nan_mask, np.nan, f_detrended)

    # Stellar spot features from the trend:
    features["trend_std"] = np.std(f_trend, axis=1)
    features["trend_range"] = np.max(f_trend, axis=1) - np.min(f_trend, axis=1)

    # Detrended light curve metrics:
    detrend_mad = np.nanmedian(np.abs(f_detrended - np.nanmedian(f_detrended, axis=1, keepdims=True)), axis=1)
    detrend_mad = np.where(detrend_mad < 1e-7, 1e-7, detrend_mad)
    features["detrend_mad"] = detrend_mad
    features["detrend_std"] = np.nanstd(f_detrended, axis=1)

    # Spot vs transit power ratio
    features["spot_to_noise_ratio"] = features["trend_std"] / (features["detrend_std"] + 1e-8)

    # Clean detrended minimum & dip SNR (the golden planet feature)
    detrend_min = np.nanmin(f_detrended, axis=1)
    detrend_p01 = np.nanpercentile(f_detrended, 1, axis=1)
    detrend_p05 = np.nanpercentile(f_detrended, 5, axis=1)
    features["detrend_min"] = detrend_min
    features["detrend_p01"] = detrend_p01
    features["detrend_dip_snr"] = -detrend_p01 / detrend_mad
    features["detrend_p01_p05_ratio"] = detrend_p01 / (detrend_p05 - 1e-8)

    # Transit shape on detrended curve (bottom width / U-shape)
    cut_80 = detrend_min[:, None] * 0.8
    in_bottom_detrend = (f_detrended <= cut_80) & (~nan_mask)
    features["detrend_bottom_cadences"] = np.sum(in_bottom_detrend, axis=1)

    # Raw dip metrics
    dip_3sigma = f < (-3.0 * mad_2d)
    dip_5sigma = f < (-5.0 * mad_2d)
    features["n_dips_3sigma"] = np.nansum(dip_3sigma, axis=1)
    features["n_dips_5sigma"] = np.nansum(dip_5sigma, axis=1)
    features["max_dip_depth"] = -features["flux_min"]
    features["dip_to_noise"] = -features["flux_min"] / mad
    features["p01_to_p05_ratio"] = features["p01"] / (features["p05"] - 1e-8)
    features["p05_to_p25_ratio"] = features["p05"] / (features["p25"] - 1e-8)

    # Consecutive low-flux run length
    run_lens = np.zeros(B, dtype=np.int32)
    current_run = np.zeros(B, dtype=np.int32)
    for t_idx in range(T):
        is_dip = dip_3sigma[:, t_idx]
        current_run = np.where(is_dip, current_run + 1, 0)
        run_lens = np.maximum(run_lens, current_run)
    features["max_consecutive_dip"] = run_lens

    # ==========================================
    # GROUP D — STELLAR FLARES
    # ==========================================
    flare_3sigma = f > (3.0 * mad_2d)
    flare_5sigma = f > (5.0 * mad_2d)
    features["n_flares_3sigma"] = np.nansum(flare_3sigma, axis=1)
    features["n_flares_5sigma"] = np.nansum(flare_5sigma, axis=1)
    features["max_flare_amp"] = features["flux_max"] / mad

    # Detrended flare metrics
    features["detrend_max_flare"] = np.nanmax(f_detrended, axis=1) / detrend_mad

    persistent_flares = flare_3sigma[:, :-1] & flare_3sigma[:, 1:]
    features["n_persistent_flares"] = np.sum(persistent_flares, axis=1)
    features["isolated_flare_ratio"] = (features["n_flares_3sigma"] - 2 * features["n_persistent_flares"]).clip(min=0) / (features["n_flares_3sigma"] + 1e-8)

    df_forward = f_filled[:, 1:] - f_filled[:, :-1]
    features["max_rise"] = np.max(df_forward, axis=1) / mad
    features["max_decay"] = -np.min(df_forward, axis=1) / mad
    features["rise_decay_asym"] = (features["max_rise"] - features["max_decay"]) / (features["max_rise"] + features["max_decay"] + 1e-8)
    features["flare_dip_asym"] = (features["max_flare_amp"] - features["dip_to_noise"]) / (features["max_flare_amp"] + features["dip_to_noise"] + 1e-8)

    # ==========================================
    # GROUP E — TIME-SERIES DYNAMICS & PERIODICITY
    # ==========================================
    sq_diff = np.sum(df_forward**2, axis=1, dtype=np.float64)
    var_flux = np.nanvar(f, axis=1, dtype=np.float64) * T
    features["von_neumann_ratio"] = sq_diff / (2.0 * var_flux + 1e-8)

    # Autocorrelation at various lags
    f_norm = f_filled - np.mean(f_filled, axis=1, keepdims=True)
    denom = np.sum(f_norm**2, axis=1, dtype=np.float64) + 1e-8
    for lag in [1, 2, 4, 12, 24, 48]: # 48 cadences = 1 day
        ac = np.sum(f_norm[:, :-lag] * f_norm[:, lag:], axis=1, dtype=np.float64) / denom
        features[f"autocorr_lag_{lag}"] = ac

    # FFT Frequency features
    fft_vals = np.abs(np.fft.rfft(f_norm, axis=1))[:, 1:] # omit DC (0 Hz)
    total_power = np.sum(fft_vals**2, axis=1, dtype=np.float64) + 1e-8

    low_freq_power = np.sum(fft_vals[:, :27]**2, axis=1, dtype=np.float64) / total_power
    features["low_freq_power_ratio"] = low_freq_power

    peak_bin = np.argmax(fft_vals, axis=1)
    features["fft_peak_freq_bin"] = peak_bin
    features["fft_peak_power"] = np.max(fft_vals**2, axis=1) / total_power

    prob_fft = (fft_vals**2) / total_power[:, None] + 1e-12
    features["spectral_entropy"] = -np.sum(prob_fft * np.log(prob_fft), axis=1, dtype=np.float64)

    # ==========================================
    # GROUP F — CENTROID AND INSTRUMENT FEATURES
    # ==========================================
    features["col_std"] = np.nanstd(col_rel, axis=1)
    features["row_std"] = np.nanstd(row_rel, axis=1)
    features["disp_std"] = np.nanstd(disp, axis=1)
    features["disp_max"] = np.nanmax(disp, axis=1)
    features["disp_median"] = np.nanmedian(disp, axis=1)

    # Centroid displacement during deep flux dips
    disp_filled = np.nan_to_num(disp, nan=0.0)
    in_dip_mask = (f < features["p05"][:, None]) & (~nan_mask)
    out_dip_mask = (f >= features["p25"][:, None]) & (f <= features["p75"][:, None]) & (~nan_mask)

    dip_disp_sum = np.sum(np.where(in_dip_mask, disp_filled, 0.0), axis=1, dtype=np.float64)
    dip_disp_cnt = np.sum(in_dip_mask, axis=1, dtype=np.float64) + 1e-8
    mean_disp_in_dip = dip_disp_sum / dip_disp_cnt

    out_disp_sum = np.sum(np.where(out_dip_mask, disp_filled, 0.0), axis=1, dtype=np.float64)
    out_disp_cnt = np.sum(out_dip_mask, axis=1, dtype=np.float64) + 1e-8
    mean_disp_out_dip = out_disp_sum / out_disp_cnt

    features["cen_shift_in_dip"] = mean_disp_in_dip - mean_disp_out_dip
    features["cen_shift_ratio"] = mean_disp_in_dip / (mean_disp_out_dip + 1e-8)
    features["cen_shift_normalized"] = features["cen_shift_in_dip"] / (features["disp_std"] + 1e-4)

    # Centroid axis correlation
    col_filled = np.nan_to_num(col_rel, nan=0.0)
    row_filled = np.nan_to_num(row_rel, nan=0.0)
    col_norm = col_filled - np.mean(col_filled, axis=1, keepdims=True)
    row_norm = row_filled - np.mean(row_filled, axis=1, keepdims=True)
    col_row_cov = np.sum(col_norm * row_norm, axis=1, dtype=np.float64)
    col_row_denom = np.sqrt(np.sum(col_norm**2, axis=1) * np.sum(row_norm**2, axis=1)) + 1e-8
    features["cen_col_row_corr"] = col_row_cov / col_row_denom

    # Flux vs Centroid correlation
    disp_norm = disp_filled - np.mean(disp_filled, axis=1, keepdims=True)
    disp_denom = np.sqrt(np.sum(disp_norm**2, axis=1, dtype=np.float64) * denom) + 1e-8
    features["flux_cen_corr"] = np.sum(f_norm * disp_norm, axis=1, dtype=np.float64) / disp_denom

    # Centroid jumps
    d_disp = np.abs(disp_filled[:, 1:] - disp_filled[:, :-1])
    features["cen_jump_max"] = np.max(d_disp, axis=1)
    features["cen_jump_mean"] = np.mean(d_disp, axis=1)

    # ==========================================
    # GROUP G — CADENCE QUALITY & INSTRUMENT ARTIFACTS
    # ==========================================
    if np.any(dump_mask):
        features["flux_mad_dump"] = np.nanmedian(np.abs(f[:, dump_mask]), axis=1)
        features["disp_mean_dump"] = np.nanmean(disp[:, dump_mask], axis=1)
    else:
        features["flux_mad_dump"] = np.zeros(B)
        features["disp_mean_dump"] = np.zeros(B)

    features["dump_flux_anomaly"] = features["flux_mad_dump"] / mad

    # ==========================================
    # GROUP H — STELLAR METADATA & ASTROPHYSICAL INTERACTIONS
    # ==========================================
    meta = stars_batch[["tmag", "teff", "logg", "radius", "contamination"]].copy().reset_index(drop=True)

    meta["teff_over_radius"] = meta["teff"] / (meta["radius"] + 1e-4)
    meta["logg_x_radius"] = meta["logg"] * meta["radius"]
    meta["expected_noise_proxy"] = 10.0 ** (0.2 * (meta["tmag"].clip(upper=20.0) - 10.0))
    meta["excess_noise"] = features["flux_std"] / (meta["expected_noise_proxy"] + 1e-8)

    feat_df = pd.DataFrame(features)
    full_df = pd.concat([feat_df, meta], axis=1)
    full_df = full_df.replace([np.inf, -np.inf], np.nan).fillna(0.0)

    return full_df

def extract_all_features(
    flux: np.ndarray,
    cen: np.ndarray,
    stars: pd.DataFrame,
    cad: pd.DataFrame,
    batch_size: int = 1500,
    desc: str = "Extracting features",
) -> pd.DataFrame:
    n_samples = len(stars)
    chunks = []

    for start_idx in tqdm(range(0, n_samples, batch_size), desc=desc):
        end_idx = min(start_idx + batch_size, n_samples)
        f_batch = np.asarray(flux[start_idx:end_idx], dtype=np.float32)
        c_batch = np.asarray(cen[start_idx:end_idx], dtype=np.float32)
        s_batch = stars.iloc[start_idx:end_idx]

        batch_feats = compute_batch_features(f_batch, c_batch, s_batch, cad)
        chunks.append(batch_feats)

    full_df = pd.concat(chunks, ignore_index=True)
    return full_df

def get_or_extract_features(cache_dir: Path = config.PROCESSED_DATA_DIR, force_recompute: bool = False):
    from src.data_loader import load_flux_arrays, load_centroid_arrays, load_stars_metadata, load_cadences

    train_feat_path = cache_dir / "train_features.parquet"
    test_feat_path = cache_dir / "test_features.parquet"

    if not force_recompute and train_feat_path.exists() and test_feat_path.exists():
        print(f"[CACHE] Loading cached features from {cache_dir}...")
        train_df = pd.read_parquet(train_feat_path)
        test_df = pd.read_parquet(test_feat_path)
        print(f"[CACHE] Loaded train: {train_df.shape}, test: {test_df.shape}")
        return train_df, test_df

    print("[EXTRACT] Extracting features with detrending & domain-shift adaptation...")
    train_flux, test_flux = load_flux_arrays()
    train_cen, test_cen = load_centroid_arrays()
    train_stars, test_stars = load_stars_metadata()
    train_cad, test_cad = load_cadences()

    train_df = extract_all_features(train_flux, train_cen, train_stars, train_cad, desc="Train features")
    test_df = extract_all_features(test_flux, test_cen, test_stars, test_cad, desc="Test features")

    print(f"[CACHE] Caching features to {cache_dir}...")
    train_df.to_parquet(train_feat_path, index=False)
    test_df.to_parquet(test_feat_path, index=False)
    print(f"[CACHE] Saved {train_feat_path} ({train_df.shape}) and {test_feat_path} ({test_df.shape})")

    return train_df, test_df

if __name__ == "__main__":
    get_or_extract_features(force_recompute=True)
