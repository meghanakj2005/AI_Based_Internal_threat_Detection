def add_engineered_features(df):
    # Login outside work hours (9AM-6PM)
    df["after_hours"] = df["login_hour"].apply(lambda x: 1 if x < 9 or x > 18 else 0)
    
    # High download flag
    df["high_download"] = df["download_mb"].apply(lambda x: 1 if x > 500 else 0)
    
    # Excess file access flag
    df["excess_files"] = df["files_accessed"].apply(lambda x: 1 if x > 40 else 0)
    
    return df