import shap
import pandas as pd
import joblib
from src.feature_engineering import create_features
from src.preprocessing import scale_features,preprocess_data

def get_shap_values():
    df=create_features()
    numeric_pipeline,x_train_scaled,x_test_scaled=scale_features()
    
    pipeline = joblib.load("F:/Project/unified mentor/Bank churn Prediction/model/GradientBoosting_AllKNN.pkl")
    model = pipeline.named_steps["model"]
    
    

    explainer = shap.Explainer(model)
    shap_values = explainer(x_train_scaled)

    return shap_values