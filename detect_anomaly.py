import pickle
import pandas as pd
from data_preprocessing import preprocess_data
from feature_engineering import add_engineered_features


def detect(df):

    # Add engineered features
    df = add_engineered_features(df)

    # Preprocess data
    X_scaled, scaler = preprocess_data(df)

    # Load trained AI model
    with open("../models/anomaly_model.pkl", "rb") as f:
        anomaly_model = pickle.load(f)

    # Predict anomalies
    predictions = anomaly_model.predict(X_scaled)

    # Convert predictions to labels
    df["Anomaly"] = predictions
    df["Anomaly"] = df["Anomaly"].apply(
        lambda x: "Threat" if x == -1 else "Normal"
    )

    return df