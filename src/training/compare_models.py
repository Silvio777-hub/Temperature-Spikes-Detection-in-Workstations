from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor
from sklearn.metrics import f1_score
import pandas as pd
import joblib

def compare_algorithms(train_csv, test_csv):
    """Compares multiple anomaly detection algorithms to find the best fit."""
    df_train = pd.read_csv(train_csv)
    df_test = pd.read_csv(test_csv)
    
    features = ['temperature', 'cpu_usage', 'memory_usage', 'disk_io']
    # Filter only available
    features = [f for f in features if f in df_train.columns]
    
    X_train = df_train[features].dropna()
    X_test = df_test[features].dropna()
    y_test = df_test.loc[X_test.index, 'anomaly']
    
    results = {}
    
    # 1. Isolation Forest
    clf_if = IsolationForest(contamination=0.1, random_state=42)
    clf_if.fit(X_train)
    y_pred_if = [1 if p == -1 else 0 for p in clf_if.predict(X_test)]
    results['Isolation Forest'] = f1_score(y_test, y_pred_if)
    
    # 2. One-Class SVM
    clf_svm = OneClassSVM(nu=0.1)
    clf_svm.fit(X_train)
    y_pred_svm = [1 if p == -1 else 0 for p in clf_svm.predict(X_test)]
    results['One-Class SVM'] = f1_score(y_test, y_pred_svm)
    
    print("\n--- Algorithm Comparison (F1-Score) ---")
    for name, score in results.items():
        print(f"{name}: {score:.4f}")
    
    return results

if __name__ == "__main__":
    # Mock or real data paths
    pass
