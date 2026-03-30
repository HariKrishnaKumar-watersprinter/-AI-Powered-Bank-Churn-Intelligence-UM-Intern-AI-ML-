from utils.cost import cost_function
import streamlit as st
import joblib
import pandas as pd
import plotly.express as px
from src.feature_engineering import create_features
from prediction.predict_model import load_prediction_model
#if not st.session_state.get('authentication_status'):
#    st.switch_page("app.py")

def Cost_Analysis():
    st.header("💰 Business Cost Optimization")

    df = create_features()
    df.drop(['CustomerId', 'Surname','Year'], axis=1, inplace=True)

    # One-hot encoding
    df = pd.get_dummies(df, columns=['Geography', 'Gender'],dtype=int)
    x=df.drop('Exited',axis=1)
    y=df['Exited']
    model = load_prediction_model()
    probs = model.predict_proba(x)[:,1]

    thresholds = [0.3, 0.4, 0.5, 0.6, 0.7]
    costs = []

    for t in thresholds:
        preds = (probs >= t).astype(int)
        cost = cost_function(y, preds)
        costs.append(cost)

    cost_df = pd.DataFrame({
        "threshold": thresholds,
        "cost": costs
    })

    fig = px.line(cost_df, x="threshold", y="cost", title="Cost vs Threshold")

    st.plotly_chart(fig)
    st.dataframe(cost_df)
Cost_Analysis()
