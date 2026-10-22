import numpy as np
from typing import Tuple

def normalize_flux(flux: np.ndarray) -> np.ndarray:
    """
    Computes relative flux: relative_flux = flux / nanmedian(flux) - 1.
    Handles zero or invalid medians safely.
    Works for 1D or 2D arrays (N, T).
    """
    if flux.ndim == 1:
        med = np.nanmedian(flux)
        if np.isnan(med) or med <= 0:
            med = 1.0
        return (flux / med) - 1.0
    else:
        med = np.nanmedian(flux, axis=1, keepdims=True)
        med = np.where(np.isnan(med) | (med <= 0), 1.0, med)
        return (flux / med) - 1.0

def process_centroids(cen: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Extracts centered column, centered row, and Euclidean displacement in millipixels.
    cen shape: (N, 2, T) or (2, T)
    Returns:
        col_rel: (N, T), row_rel: (N, T), disp: (N, T)
    """
    if cen.ndim == 2: # (2, T)
        col = cen[0]
        row = cen[1]
        col_med = np.nanmedian(col)
        row_med = np.nanmedian(row)
        col_rel = col - (0.0 if np.isnan(col_med) else col_med)
        row_rel = row - (0.0 if np.isnan(row_med) else row_med)
        disp = np.sqrt(col_rel**2 + row_rel**2)
        return col_rel, row_rel, disp
    else: # (N, 2, T)
        col = cen[:, 0, :]
        row = cen[:, 1, :]
        col_med = np.nanmedian(col, axis=1, keepdims=True)
        row_med = np.nanmedian(row, axis=1, keepdims=True)
        col_med = np.where(np.isnan(col_med), 0.0, col_med)
        row_med = np.where(np.isnan(row_med), 0.0, row_med)
        col_rel = col - col_med
        row_rel = row - row_med
        disp = np.sqrt(col_rel**2 + row_rel**2)
        return col_rel, row_rel, disp
