import joblib
import pandas as pd
from src.preprocessing import scale_features
import streamlit as st
import os

@st.cache_resource
def load_prediction_model():
    model_path = os.path.join(os.getcwd(), "best model", "GradientBoosting_AllKNN.pkl")
    return joblib.load(model_path)

def predict_churn(input_df):
    model = load_prediction_model()
    numeric_pipeline, _,_= scale_features() 
    input_df=numeric_pipeline.transform(input_df)
    prob = model.predict_proba(input_df)[0][1]
    pred = 1 if prob > 0.5 else 0
    return prob,pred,model