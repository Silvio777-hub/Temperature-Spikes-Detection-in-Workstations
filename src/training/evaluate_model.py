import pandas as pd
import joblib
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
import os

def evaluate_model(test_csv, model_path="data/models/isolation_forest.pkl", scaler_path="data/models/scaler.pkl", features_path="data/models/feature_columns.pkl"):
    """
    Evaluates the model against labeled test data.
    Labeled data must have an 'anomaly' column (0 or 1).
    """
    if not all(os.path.exists(p) for p in [test_csv, model_path, scaler_path, features_path]):
        print("Evaluation files missing.")
        return
        
    df = pd.read_csv(test_csv)
    if 'anomaly' not in df.columns:
        print("Test data must be labeled with an 'anomaly' column (0 or 1).")
        return

    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    features = joblib.load(features_path)
    
    X = df[features]
    y_true = df['anomaly']
    
    X_scaled = scaler.transform(X)
    y_pred_raw = model.predict(X_scaled)
    # Isolation Forest: -1 (anomaly), 1 (normal) -> Map to 1 and 0
    y_pred = [1 if p == -1 else 0 for p in y_pred_raw]
    
    metrics = {
        "precision": precision_score(y_true, y_pred),
        "recall": recall_score(y_true, y_pred),
        "f1": f1_score(y_true, y_pred),
        "confusion_matrix": confusion_matrix(y_true, y_pred).tolist()
    }
    
    print("\n=== Model Evaluation Results ===")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall:    {metrics['recall']:.4f}")
    print(f"F1-Score:  {metrics['f1']:.4f}")
    print("================================\n")
    
    return metrics

if __name__ == "__main__":
    import sys
    test_path = sys.argv[1] if len(sys.argv) > 1 else "data/training/labeled_training_data.csv"
    evaluate_model(test_path)
