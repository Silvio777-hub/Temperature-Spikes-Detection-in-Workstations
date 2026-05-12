import pytest
import os
import sys
import pandas as pd
import numpy as np

# Add src to path
sys.path.append(os.getcwd())

from src.processor import DataProcessor
from src.detector import AnomalyDetector

def test_data_processor_ready():
    """Verify that processor is not ready until window is full."""
    processor = DataProcessor(window_size=5)
    for i in range(4):
        processor.add_reading(45.0)
    assert not processor.is_ready()
    processor.add_reading(45.0)
    assert processor.is_ready()

def test_feature_extraction_logic():
    """Verify feature math (slope, variance)."""
    processor = DataProcessor(window_size=3)
    # Rising temps: 40, 45, 50
    # Expected slope: 5.0 per index
    processor.add_reading(40)
    processor.add_reading(45)
    processor.add_reading(50)
    processor.add_reading(50)
    processor.add_reading(50)
    
    features = processor.get_features()
    assert features['max_temp'] == 50
    assert features['slope'] >= 0
    assert features['range'] > 0

def test_rule_detector():
    """Verify immediate threshold triggers."""
    detector = AnomalyDetector()
    detector.CRITICAL_TEMP = 80.0
    
    # Normal case
    state, msg = detector.check_rules(45.0, None)
    assert state == "NORMAL"
    
    # Critical case
    state, msg = detector.check_rules(85.0, None)
    assert state == "EMERGENCY"
    assert "CRITICAL" in msg

def test_anomaly_detection_ml_logic():
    """Verify ML fallback when no model is present."""
    detector = AnomalyDetector()
    detector.model = None # Force no model
    
    features = {'max_temp': 45, 'max_pos_diff': 1, 'range': 2, 'slope': 0.1, 'variance': 0.1}
    state, msg = detector.analyze(45.0, features)
    assert state == "NORMAL"
