import os
import json
import joblib
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from src.preprocessing import load_and_preprocess
from src.feature_extraction import FEATURE_NAMES

def main():
    print("Loading and preprocessing data...")
    try:
        X_train, X_test, y_train, y_test, scaler, label_encoder = load_and_preprocess()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please ensure you have generated the dataset first.")
        return
        
    print(f"Training set size: {X_train.shape[0]}")
    print(f"Test set size: {X_test.shape[0]}")
    
    print("Training RandomForestClassifier...")
    model = RandomForestClassifier(
        n_estimators=200, 
        max_depth=20, 
        random_state=42, 
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    
    print("Evaluating model...")
    y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    cm = confusion_matrix(y_test, y_pred)
    
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision (weighted): {precision:.4f}")
    print(f"Recall (weighted): {recall:.4f}")
    print(f"F1 Score (weighted): {f1:.4f}")
    
    base_dir = os.path.dirname(os.path.dirname(__file__))
    models_dir = os.path.join(base_dir, 'models')
    reports_dir = os.path.join(base_dir, 'reports')
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)
    
    # Save model
    model_path = os.path.join(models_dir, 'phishing_model.pkl')
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")
    
    # Get feature importances
    importances = model.feature_importances_
    feature_importance_dict = {name: float(imp) for name, imp in zip(FEATURE_NAMES, importances)}
    
    # Save metrics
    metrics = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'confusion_matrix': cm.tolist(),
        'feature_importances': feature_importance_dict
    }
    metrics_path = os.path.join(models_dir, 'metrics.json')
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=4)
    print(f"Metrics saved to {metrics_path}")
    
    # Setup dark theme for plots
    plt.style.use('dark_background')
    colors = ['#00ff88', '#ffaa00', '#ff4444'] # Green, Amber, Red for classes (0,1,2 typically)
    
    # Plot feature importances
    plt.figure(figsize=(10, 8))
    sorted_idx = np.argsort(importances)
    plt.barh(np.array(FEATURE_NAMES)[sorted_idx], importances[sorted_idx], color='#00ff88')
    plt.title('Feature Importances')
    plt.xlabel('Relative Importance')
    plt.tight_layout()
    fi_plot_path = os.path.join(reports_dir, 'feature_importance.png')
    plt.savefig(fi_plot_path)
    plt.close()
    
    # Plot confusion matrix
    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Greens)
    plt.title('Confusion Matrix')
    plt.colorbar()
    
    classes = label_encoder.classes_
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    
    thresh = cm.max() / 2.
    for i, j in np.ndindex(cm.shape):
        plt.text(j, i, format(cm[i, j], 'd'),
                 horizontalalignment="center",
                 color="black" if cm[i, j] > thresh else "white")
                 
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()
    cm_plot_path = os.path.join(reports_dir, 'confusion_matrix.png')
    plt.savefig(cm_plot_path)
    plt.close()
    
    print(f"Plots saved to {reports_dir}")

if __name__ == "__main__":
    main()
