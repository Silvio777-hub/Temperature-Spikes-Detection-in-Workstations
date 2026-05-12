import pandas as pd

class FeatureEngineer:
    """Derives advanced features from raw metrics."""
    
    @staticmethod
    def add_features(df):
        """Adds rate of change and rolling stats."""
        df = df.copy()
        
        # Temperature Change Rate (°C/sec)
        if 'temperature' in df.columns:
            df['temp_rate'] = df['temperature'].diff().fillna(0)
            
            # Rolling statistics (window=6 samples ~ 6 seconds)
            df['temp_roll_mean'] = df['temperature'].rolling(window=6, min_periods=1).mean()
            df['temp_roll_std'] = df['temperature'].rolling(window=6, min_periods=1).std().fillna(0)
            
        # Thermal Efficiency (CPU usage / Temp)
        if 'cpu_usage' in df.columns and 'temperature' in df.columns:
            # Add small epsilon to avoid div by zero
            df['thermal_efficiency'] = df['cpu_usage'] / (df['temperature'] + 1e-5)
            
        return df
