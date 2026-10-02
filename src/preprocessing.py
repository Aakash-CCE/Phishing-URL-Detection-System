import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from src.feature_extraction import extract_features_array, FEATURE_NAMES

def load_and_preprocess(dataset_path: str = None) -> tuple:
    """
    Load dataset, extract features, encode labels, scale features, split data.
    Returns: X_train, X_test, y_train, y_test, scaler, label_encoder
    """
    if dataset_path is None:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        dataset_path = os.path.join(base_dir, 'data', 'dataset.csv')
        
    try:
        df = pd.read_csv(dataset_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Dataset not found at {dataset_path}")
        
    # Extract features
    X_raw = [extract_features_array(url) for url in df['url']]
    X = np.array(X_raw)
    
    # Encode labels
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(df['label'])
    
    # Train test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    # Save scaler and label encoder
    base_dir = os.path.dirname(os.path.dirname(__file__))
    models_dir = os.path.join(base_dir, 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    joblib.dump(scaler, os.path.join(models_dir, 'scaler.pkl'))
    joblib.dump(label_encoder, os.path.join(models_dir, 'label_encoder.pkl'))
    
    return X_train, X_test, y_train, y_test, scaler, label_encoder
