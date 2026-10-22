import numpy as np
import pandas as pd
from typing import Tuple, Optional
from src import config

def load_stars_metadata() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Loads train and test stars metadata CSVs."""
    train_stars = pd.read_csv(config.TRAIN_STARS_FILE)
    test_stars = pd.read_csv(config.TEST_STARS_FILE)
    return train_stars, test_stars

def load_cadences() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Loads train and test cadences CSVs."""
    train_cad = pd.read_csv(config.TRAIN_CADENCES_FILE)
    test_cad = pd.read_csv(config.TEST_CADENCES_FILE)
    return train_cad, test_cad

def load_flux_arrays(mmap_mode: Optional[str] = "r") -> Tuple[np.ndarray, np.ndarray]:
    """Loads train and test flux arrays."""
    train_flux = np.load(config.TRAIN_FLUX_FILE, mmap_mode=mmap_mode)
    test_flux = np.load(config.TEST_FLUX_FILE, mmap_mode=mmap_mode)
    return train_flux, test_flux

def load_centroid_arrays(mmap_mode: Optional[str] = "r") -> Tuple[np.ndarray, np.ndarray]:
    """Loads train and test centroid arrays."""
    train_cen = np.load(config.TRAIN_CENTROID_FILE, mmap_mode=mmap_mode)
    test_cen = np.load(config.TEST_CENTROID_FILE, mmap_mode=mmap_mode)
    return train_cen, test_cen
