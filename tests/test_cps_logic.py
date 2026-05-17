import unittest
import os
from thermal_system.data_validation import DataValidator
from thermal_system.feature_engineering import FeatureEngineer
from thermal_system.state_model import HealthStateModel, CPSState

class TestCPSLogic(unittest.TestCase):
    def test_data_validation_bounds(self):
        """Tests that invalid inputs are correctly clipped and defaults are applied."""
        validator = DataValidator()
        metrics = {
            "temperature": 150.0, # Out of bounds -> should fall back to 45.0
            "cpu_usage": 120.0,   # Out of bounds -> should clip to 100.0
            "memory_usage": -5.0, # Out of bounds -> should clip to 0.0
            "gpu_temp": 65.0      # Valid -> should pass through
        }
        validated = validator.validate(metrics)
        self.assertEqual(validated["temperature"], 45.0)
        self.assertEqual(validated["cpu_usage"], 100.0)
        self.assertEqual(validated["memory_usage"], 0.0)
        self.assertEqual(validated["gpu_temp"], 65.0)

    def test_feature_engineering_temporal_logic(self):
        """Tests calculation of gradient, ratio, and rolling standard deviation."""
        engineer = FeatureEngineer(window_size=3)
        
        # Step 1: Base Load
        m1 = engineer.extract_features({"temperature": 50.0, "cpu_usage": 10.0})
        self.assertEqual(m1["temp_gradient"], 0.0)
        self.assertEqual(m1["load_to_temp_ratio"], 5.0)
        
        # Step 2: Immediate Load Spike
        m2 = engineer.extract_features({"temperature": 55.0, "cpu_usage": 20.0})
        self.assertEqual(m2["temp_gradient"], 5.0)
        self.assertEqual(m2["load_to_temp_ratio"], 55.0 / 20.0)
        self.assertGreater(m2["temp_rolling_std"], 0)

    def test_health_state_transitions(self):
        """Tests rule-based state transition tracking without ML interference."""
        model = HealthStateModel(state_file="test_dummy_state.json")
        model.critical_temp = 85
        model.alert_temp = 75
        
        # Scenario 1: Normal Operation
        state, _ = model.classify({"temperature": 40.0, "throttling": "NO"}, anomaly_score=1)
        self.assertEqual(state, CPSState.NORMAL)
        
        # Scenario 2: High Temperature Alert
        state, _ = model.classify({"temperature": 76.0, "throttling": "NO"}, anomaly_score=1)
        self.assertEqual(state, CPSState.ALERT)
        
        # Scenario 3: Hardware Throttling Triggers Alert (Even if Temp is OK)
        state, _ = model.classify({"temperature": 70.0, "throttling": "YES"}, anomaly_score=1)
        self.assertEqual(state, CPSState.ALERT)
        
        # Scenario 4: Critical Overheating (Clear last metrics to prevent rapid rise alert override)
        model.last_metrics = None
        state, _ = model.classify({"temperature": 90.0, "throttling": "NO"}, anomaly_score=1)
        self.assertEqual(state, CPSState.CRITICAL)

        # Cleanup dummy state file if created
        if os.path.exists("test_dummy_state.json"):
            try:
                os.remove("test_dummy_state.json")
            except Exception:
                pass

if __name__ == "__main__":
    unittest.main()
