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

    def validate(self, metrics):
        """
        Cleans and validates a dictionary of raw metrics.
        Renamed to 'validate' to match real_time_detector expectation.
        """
        validated = {}
        
        # 1. Temperature Validation
        temp = metrics.get("temperature")
        if temp is None or not (self.temp_bounds[0] <= temp <= self.temp_bounds[1]):
            validated["temperature"] = self.last_valid_temp
        else:
            validated["temperature"] = temp
            self.last_valid_temp = temp

        # 2. CPU Usage Validation
        cpu = metrics.get("cpu_usage", 0)
        validated["cpu_usage"] = np.clip(cpu, self.cpu_bounds[0], self.cpu_bounds[1])

        # 3. Memory Usage
        validated["memory_usage"] = np.clip(metrics.get("memory_usage", 0), 0, 100)

        # 4. Pass through others
        validated["freq_mhz"] = metrics.get("freq_mhz", 0)
        validated["gpu_temp"] = metrics.get("gpu_temp")
        validated["fan_speed"] = metrics.get("fan_speed", 0)
        validated["throttling"] = metrics.get("throttling", "NO")
        validated["disk_io_rate"] = metrics.get("disk_io_rate", 0)
        
        return validated
