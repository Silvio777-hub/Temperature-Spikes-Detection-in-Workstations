import numpy as np

class DataValidator:
    """
    Data Processing Layer: Data Validation.
    Handles noisy, incomplete, and inconsistent sensor data to ensure ML robustness.
    """
    def __init__(self, temp_bounds=(0, 110), cpu_bounds=(0, 100)):
        self.temp_bounds = temp_bounds
        self.cpu_bounds = cpu_bounds
        self.last_valid_temp = 45.0 # Default starting temp

    def validate_metrics(self, metrics):
        """
        Cleans and validates a dictionary of raw metrics.
        Implements fallback logic for missing or out-of-bounds sensor readings.
        """
        validated = {}
        
        # 1. Temperature Validation (Filter out sensor jitter/errors)
        temp = metrics.get("temperature")
        if temp is None or not (self.temp_bounds[0] <= temp <= self.temp_bounds[1]):
            # Use last valid temperature as fallback (Smoothing)
            validated["temperature"] = self.last_valid_temp
        else:
            validated["temperature"] = temp
            self.last_valid_temp = temp

        # 2. CPU Usage Validation
        cpu = metrics.get("cpu_usage", 0)
        validated["cpu_usage"] = np.clip(cpu, self.cpu_bounds[0], self.cpu_bounds[1])

        # 3. RAM Usage Validation
        validated["memory_usage"] = np.clip(metrics.get("memory_usage", 0), 0, 100)

        # 4. Frequency & Other Metrics
        validated["freq_mhz"] = max(0, metrics.get("freq_mhz", 0))
        
        return validated
