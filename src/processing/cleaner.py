import pandas as pd
import numpy as np

class DataCleaner:
    """Handles missing values and smoothing."""
    def __init__(self, window_size=3):
        self.window_size = window_size

    def smooth(self, series):
        """Applies a moving average to smooth the signal."""
        return series.rolling(window=self.window_size, min_periods=1).mean()

    def interpolate(self, df):
        """Fills missing values using linear interpolation."""
        return df.interpolate(method='linear')
