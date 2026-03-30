import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go
from utils.helpers import risk_segment
from src.feature_engineering import create_features
import os
#if not st.session_state.get('authentication_status'):
#    st.switch_page("app.py")

st.title("📊 Churn Risk Distribution Dashboard")


df=create_features()
df1=df.copy()
pipeline = os.path.join(os.getcwd(), "best model", "GradientBoosting_AllKNN.pkl")

df1.drop(['CustomerId', 'Surname','Year'], axis=1, inplace=True)

    # One-hot encoding
df1 = pd.get_dummies(df1, columns=['Geography', 'Gender'],dtype=int)
    #splitting the data

x=df1.drop('Exited',axis=1)
y=df1['Exited']
probs = pipeline.predict_proba(x)[0][1]

df1["ChurnProbability"] = probs
df1["RiskSegment"] = df1["ChurnProbability"].apply(risk_segment)
df["ChurnProbability"] = probs
df["RiskSegment"] = df["ChurnProbability"].apply(risk_segment)
# Histogram
st.write("Churn Probability Distribution")
fig = px.histogram(df1, x="ChurnProbability", nbins=50, title="Churn Probability Distribution",)
fig.update_traces(texttemplate='%{y:,.0f}', textposition='auto')
st.plotly_chart(fig)
# Risk Segmentation
# Segment count

seg_fig = px.pie(df, names="RiskSegment", title="Risk Segmentation")
st.plotly_chart(seg_fig)

# Geography analysis
geo_data=df.groupby('Geography')['RiskSegment'].value_counts().reset_index(name='Count')

geo_fig = px.bar(geo_data, x='Geography',y="Count",color="RiskSegment", title="Risk by Geography",barmode='group')
geo_fig.update_traces(texttemplate='%{y:,.0f}', textposition='auto')
st.plotly_chart(geo_fig)
# Age analysis
# Gender analysis   
gender_data=df.groupby('Gender')['RiskSegment'].value_counts().reset_index(name='Count')
gender_fig = px.bar(
    gender_data, 
    x='Gender', 
    y="Count", 
    color="RiskSegment", 
    title="Risk by Gender",barmode='group'
)
gender_fig.update_traces(texttemplate='%{y:,.0f}', textposition='auto')
st.plotly_chart(gender_fig)
