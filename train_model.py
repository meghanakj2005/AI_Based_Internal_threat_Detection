import os
import pickle
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from data_preprocessing import preprocess_data
from feature_engineering import add_engineered_features

def train_models():
    
    df = pd.read_csv("../data/employee_logs.csv")
    df = add_engineered_features(df)
    
    X_scaled, scaler = preprocess_data(df)
    
    # --------- Anomaly Detection Model ---------
    anomaly_model = IsolationForest(contamination=0.3, random_state=42)
    anomaly_model.fit(X_scaled)
    
    # Generate anomaly labels
    anomaly_labels = anomaly_model.predict(X_scaled)
    anomaly_labels = [1 if x == -1 else 0 for x in anomaly_labels]
    
    # --------- Classification Model ---------
    classifier = RandomForestClassifier()
    classifier.fit(X_scaled, anomaly_labels)
    
    # Save models
    os.makedirs("../models", exist_ok=True)
    
    with open("../models/anomaly_model.pkl", "wb") as f:
        pickle.dump(anomaly_model, f)
    
    with open("../models/classifier_model.pkl", "wb") as f:
        pickle.dump(classifier, f)
    
    print("Models Trained and Saved Successfully!")

if __name__ == "__main__":
    train_models()