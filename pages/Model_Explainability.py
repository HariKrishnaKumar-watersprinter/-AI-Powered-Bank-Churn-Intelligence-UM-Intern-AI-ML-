import shap
import pandas as pd
from src.explainability import get_shap_values
from src.feature_engineering import create_features
import streamlit as st
import matplotlib.pyplot as plt

#if not st.session_state.get('authentication_status'):
    #st.switch_page("app.py")

def model_explainability():
    st.title("Model Explainability")
    st.header("🧠 SHAP Explainability")
    df=create_features()
    X = df.drop("Exited", axis=1)
    sample = X.sample(200)

    shap_values = get_shap_values()

    st.subheader("Feature Importance")
    fig = shap.plots.bar(shap_values, show=False)
    fig = plt.gcf()
    st.pyplot(fig)
    plt.clf()
    
    st.subheader("Summary Plot")
    fig2 = shap.plots.beeswarm(shap_values, show=False)
    fig2 = plt.gcf()
    st.pyplot(fig2)
    plt.clf()
model_explainability()
