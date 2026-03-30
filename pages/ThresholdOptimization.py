import streamlit as st
from src.preprocessing import preprocess_data,scale_features
from utils.threshold import evaluate_thresholds
from sklearn.model_selection import train_test_split
import joblib
import pandas as pd
import plotly.express as px
from prediction.predict_model import predict_churn

#if not st.session_state.get('authentication_status'):
    #st.switch_page("app.py")

def ThresholdOptimization():
    st.header("🎯 Precision-Recall Optimization")



    _,_,_,y_test = preprocess_data()
    _,_,x_test_scaled= scale_features()
    _,_,model = predict_churn(x_test_scaled)
    probs = model.predict_proba(x_test_scaled)[:,1]

    results = pd.DataFrame(evaluate_thresholds(y_test, probs))

    fig = px.line(
        results,
        x="threshold",
        y=["precision", "recall", "f1"],
        title="Threshold Optimization Curve"
    )

    st.plotly_chart(fig)
    st.dataframe(results)
ThresholdOptimization()