import shap
import pandas as pd
from src.explainability import get_shap_values
from src.feature_engineering import create_features
import streamlit as st
import matplotlib.pyplot as plt
from src.preprocessing import scale_features
from prediction.predict_model import load_prediction_model
#if not st.session_state.get('authentication_status'):
    #st.switch_page("app.py")

def model_explainability():
    st.title("Model Explainability")
    st.header("🧠 SHAP Explainability")
    model = load_prediction_model()
    _,x_train_scaled,_= scale_features()
    sample = x_train_scaled.sample(200)

    # Using the generic Explainer to support multi-class GradientBoosting
    explainer = shap.Explainer(model.named_steps['model'].predict, sample)
    shap_values = explainer(sample)


    st.subheader("Feature Importance")
    fig = shap.plots.bar(shap_values, show=False)
    fig = plt.gcf()
    st.pyplot(fig)
    plt.clf()
    st.subheader("Global Feature Importance")

    fig, ax = plt.subplots()
    shap.summary_plot(shap_values, sample, show=False, class_names=model.classes_)
    st.pyplot(fig)
    plt.clf()
