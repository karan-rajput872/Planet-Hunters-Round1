"""
Phase 5 Astronomy Cotrending Module (Co-trending Basis Vectors / Channel Median Subtraction)
Author: Senior ML Research Engineer & Computational Astrophysicist

Removes common detector systematics (pointing jitter, temperature swings, scattered light)
per (camera, ccd) channel as recommended by PROBLEM_STATEMENT.md Section 8.
"""

import numpy as np
import pandas as pd
from typing import Tuple, Dict

def cotrend_lightcurves_and_centroids(
    flux_norm: np.ndarray,      # (N, T) normalized relative flux
    col_rel: np.ndarray,        # (N, T) relative column centroids
    row_rel: np.ndarray,        # (N, T) relative row centroids
    stars_df: pd.DataFrame,     # DataFrame with 'camera' and 'ccd' columns
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, Dict[str, np.ndarray]]:
    """
    Subtracts the instantaneous common systematic trend for each (camera, ccd) channel.
    Returns:
        f_clean: (N, T) cotrended relative flux
        col_clean: (N, T) cotrended column centroids
        row_clean: (N, T) cotrended row centroids
        disp_clean: (N, T) cotrended centroid displacement
        channel_trends: dict mapping channel name to the common trend array
    """
    N, T = flux_norm.shape
    f_clean = flux_norm.copy()
    col_clean = col_rel.copy()
    row_clean = row_rel.copy()
    
    channel_trends = {}
    
    cameras = stars_df['camera'].values
    ccds = stars_df['ccd'].values
    
    for cam in np.unique(cameras):
        for ccd in np.unique(ccds):
            mask = (cameras == cam) & (ccds == ccd)
            idxs = np.where(mask)[0]
            if len(idxs) == 0:
                continue
            
            chan_name = f"cam{cam}_ccd{ccd}"
            
            # 1. Flux common trend: nanmedian across all stars in this detector channel
            flux_chan = flux_norm[idxs]
            med_trend = np.nanmedian(flux_chan, axis=0) # (T,)
            # If all nan at some cadence, replace with 0.0
            med_trend = np.nan_to_num(med_trend, nan=0.0)
            channel_trends[chan_name + "_flux"] = med_trend
            f_clean[idxs] = flux_chan - med_trend[None, :]
            
            # 2. Centroid common drift: telescope pointing jitter moves all stars simultaneously
            col_chan = col_rel[idxs]
            row_chan = row_rel[idxs]
            med_col = np.nan_to_num(np.nanmedian(col_chan, axis=0), nan=0.0)
            med_row = np.nan_to_num(np.nanmedian(row_chan, axis=0), nan=0.0)
            
            channel_trends[chan_name + "_col"] = med_col
            channel_trends[chan_name + "_row"] = med_row
            
            col_clean[idxs] = col_chan - med_col[None, :]
            row_clean[idxs] = row_chan - med_row[None, :]
            
    disp_clean = np.hypot(col_clean, row_clean)
    
    return f_clean, col_clean, row_clean, disp_clean, channel_trends
