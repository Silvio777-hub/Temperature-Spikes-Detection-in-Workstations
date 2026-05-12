import unittest
import os
import pandas as pd
from src.predict import AnomalyPredictor
from src.train import prepare_data, train_model

class TestPredict(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_csv = "test_predict_data.csv"
        cls.test_model = "test_predict_models/model.pkl"
        os.makedirs("test_predict_models", exist_ok=True)
        
        # Create dummy data with many normal points and one extreme spike
        temps = [40] * 100 + [100]
        cpu = [10] * 101
        df = pd.DataFrame({
            'timestamp': pd.date_range(start='2023-01-01', periods=101, freq='S').isoformat(),
            'temperature': temps,
            'cpu_usage': cpu
        })
        df.to_csv(cls.test_csv, index=False)
        
        X, _ = prepare_data(cls.test_csv)
        train_model(X, cls.test_model)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists("test_predict_data.csv"):
            os.remove("test_predict_data.csv")
        import shutil
        if os.path.exists("test_predict_models"):
            shutil.rmtree("test_predict_models")

    def test_prediction(self):
        predictor = AnomalyPredictor(self.test_model)
        
        # Normal case
        normal_metrics = {'temperature': 40.0, 'cpu_usage': 10.0}
        self.assertFalse(predictor.predict(normal_metrics))
        
        # Anomaly case (extreme spike)
        anomaly_metrics = {'temperature': 110.0, 'cpu_usage': 95.0}
        self.assertTrue(predictor.predict(anomaly_metrics))

if __name__ == '__main__':
    unittest.main()
