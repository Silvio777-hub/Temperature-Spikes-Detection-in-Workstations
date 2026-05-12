import pytest
from Code.state_model import HealthStateModel, CPSState
from Code.data_validation import DataValidator

def test_state_transitions():
    """Verifies that the CPS health state machine transitions correctly."""
    model = HealthStateModel(critical_temp=90, alert_temp=80)
    
    # Test Normal
    state, msg = model.classify({"temperature": 45}, 1)
    assert state == CPSState.NORMAL
    
    # Test Alert (High temp)
    state, msg = model.classify({"temperature": 85}, 1)
    assert state == CPSState.ALERT
    
    # Test Critical (Overheating)
    state, msg = model.classify({"temperature": 95}, 1)
    assert state == CPSState.CRITICAL
    
    # Test Recovery
    state, msg = model.classify({"temperature": 50}, 1)
    assert state == CPSState.STABLE

def test_data_validation():
    """Verifies that the validator filters out dangerous or noisy sensor data."""
    validator = DataValidator(temp_bounds=(10, 100))
    
    # Test Valid
    metrics = {"temperature": 50, "cpu_usage": 50}
    validated = validator.validate_metrics(metrics)
    assert validated["temperature"] == 50
    
    # Test Out of Bounds (Too high)
    metrics = {"temperature": 150} # Impossible reading
    validated = validator.validate_metrics(metrics)
    assert validated["temperature"] < 100 # Should use fallback
    
    # Test Missing Data
    metrics = {"cpu_usage": 50} # Temperature missing
    validated = validator.validate_metrics(metrics)
    assert "temperature" in validated
    assert isinstance(validated["temperature"], float)

if __name__ == "__main__":
    pytest.main([__file__])
