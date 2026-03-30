import streamlit as st
import pandas as pd
import plotly.express as px
from src.feature_engineering import create_features
from src.data_loader import load_data

def show(df):
    df=create_features()
    st.header("📊 Bivariate Analysis")

    col1 = st.selectbox("Feature", df.columns)
    col2 = 'Exited'
    col3=df.groupby(col1)[col2].value_counts().reset_index(name='Count')
    
   
    if df[col1].dtype != 'object':
        fig = px.box(df, x=col2, y=col1, title=f"{col1} vs Churn")
    else:
        fig = px.bar(col3, x=col1,y="Count",color=col2,barmode="group",title=f"{col1} vs Churn")
        fig.update_traces(texttemplate='%{y:,.0f}', textposition='inside')

    st.plotly_chart(fig, use_container_width=True)