import pandas as pd
from sklearn.preprocessing import StandardScaler

def load_data(path):
    return pd.read_csv(path)

def preprocess_data(df):
    scaler = StandardScaler()
    
    features = df.drop("employee_id", axis=1)
    scaled_features = scaler.fit_transform(features)
    
    return scaled_features, scaler