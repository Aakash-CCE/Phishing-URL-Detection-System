import os
import json
import joblib
import numpy as np
from src.feature_extraction import extract_features, extract_features_array, FEATURE_NAMES

def get_model_metrics() -> dict:
    """Load and return models/metrics.json"""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    metrics_path = os.path.join(base_dir, 'models', 'metrics.json')
    try:
        with open(metrics_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def validate_url(url: str) -> tuple:
    """Returns (is_valid: bool, cleaned_url: str, error_msg: str)"""
    if not isinstance(url, str) or not url.strip():
        return False, "", "URL cannot be empty"
        
    cleaned_url = url.strip()
    if not cleaned_url.startswith(('http://', 'https://')):
        cleaned_url = 'http://' + cleaned_url
        
    return True, cleaned_url, ""

def predict_url(url: str) -> dict:
    """
    Returns dict with prediction details, applying hybrid rule-based + ML approach.
    """
    is_valid, cleaned_url, error_msg = validate_url(url)
    
    if not is_valid:
        return {
            'url': url,
            'is_valid': False,
            'error': error_msg
        }
        
    base_dir = os.path.dirname(os.path.dirname(__file__))
    models_dir = os.path.join(base_dir, 'models')
    
    model_path = os.path.join(models_dir, 'phishing_model.pkl')
    scaler_path = os.path.join(models_dir, 'scaler.pkl')
    label_encoder_path = os.path.join(models_dir, 'label_encoder.pkl')
    
    # Extract features
    features_dict = extract_features(cleaned_url)
    features_array = extract_features_array(cleaned_url)
    
    # Load ML models if available
    ml_prediction = None
    ml_probabilities = None
    label_classes = ['legitimate', 'suspicious', 'phishing']
    
    try:
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        label_encoder = joblib.load(label_encoder_path)
        label_classes = label_encoder.classes_
        
        X = scaler.transform([features_array])
        ml_prediction = model.predict(X)[0]
        ml_probabilities = model.predict_proba(X)[0]
        
        class_str = label_encoder.inverse_transform([ml_prediction])[0].capitalize()
        confidence = float(np.max(ml_probabilities)) * 100
        
        # Get importances if available
        metrics = get_model_metrics()
        importances = metrics.get('feature_importances', {})
    except Exception as e:
        class_str = "Unknown"
        confidence = 0.0
        importances = {}
        
    red_flags = []
    
    # Rule-based overrides/flags
    if features_dict.get('has_ip_address') == 1 and features_dict.get('has_https') == 0:
        red_flags.append("Uses IP address instead of domain without HTTPS (High Risk)")
        class_str = "Phishing"
        confidence = max(confidence, 95.0)
        
    if features_dict.get('has_at_symbol') == 1:
        red_flags.append("Contains '@' symbol, often used to hide the true domain")
        
    if features_dict.get('is_shortened') == 1:
        red_flags.append("Uses a URL shortener, which can hide the final destination")
        if class_str == "Legitimate":
            class_str = "Suspicious"
            confidence = max(confidence, 70.0)
            
    if features_dict.get('has_suspicious_keywords') == 1 and features_dict.get('url_length', 0) > 75:
        red_flags.append("Long URL containing suspicious keywords commonly used in phishing")
        if class_str == "Legitimate":
            class_str = "Phishing"
            confidence = max(confidence, 85.0)
            
    # Determine Risk Level based on final classification
    risk_level_map = {
        "Legitimate": "Low",
        "Suspicious": "Medium",
        "Phishing": "High"
    }
    risk_level = risk_level_map.get(class_str, "Unknown")
    
    # Generate Explanation
    explanation = f"This URL is classified as {class_str} with {confidence:.1f}% confidence."
    if red_flags:
        explanation += " The system detected several red flags: " + "; ".join(red_flags) + "."
    else:
        if class_str == "Legitimate":
            explanation += " No significant red flags were detected, and its feature profile aligns with safe websites."
        else:
            explanation += " Based on its structural features, it exhibits characteristics common to unsafe sites."
            
    # Calculate Important Features
    important_features = []
    if importances:
        # Sort features by importance
        sorted_features = sorted(importances.items(), key=lambda x: x[1], reverse=True)
        for name, imp in sorted_features[:5]:
            important_features.append({
                'name': name,
                'value': features_dict[name],
                'importance': float(imp)
            })
            
    return {
        'url': cleaned_url,
        'is_valid': True,
        'classification': class_str,
        'risk_level': risk_level,
        'confidence': float(confidence),
        'features': features_dict,
        'important_features': important_features,
        'explanation': explanation,
        'red_flags': red_flags
    }
