import unittest
import pandas as pd
import os
import shutil
from src.train import prepare_data, train_model

class TestTrain(unittest.TestCase):
    def setUp(self):
        self.test_csv = "test_train_data.csv"
        self.test_model = "test_models/model.pkl"
        
        # Create dummy data
        df = pd.DataFrame({
            'timestamp': pd.date_range(start='2023-01-01', periods=10, freq='S').isoformat(),
            'temperature': [40, 41, 40, 42, 40, 41, 40, 42, 40, 90], # One spike
            'cpu_usage': [10] * 10
        })
        df.to_csv(self.test_csv, index=False)

    def tearDown(self):
        if os.path.exists(self.test_csv):
            os.remove(self.test_csv)
        if os.path.exists("test_models"):
            shutil.rmtree("test_models")

    def test_train_pipeline(self):
        X, df = prepare_data(self.test_csv)
        self.assertEqual(len(X), 10)
        
        model = train_model(X, self.test_model)
        self.assertTrue(os.path.exists(self.test_model))

if __name__ == '__main__':
    unittest.main()
