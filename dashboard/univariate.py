import streamlit as st
import pandas as pd
import plotly.express as px
from src.feature_engineering import create_features

def show(df):
    df=create_features()
    st.header("📊 Univariate Analysis")

    column = st.selectbox("Select Column", df.columns)


    if df[column].dtype != 'object':
        fig = px.histogram(df, x=column, title=f"{column} Distribution",color_discrete_sequence=px.colors.qualitative.Pastel1)
        fig.update_traces(texttemplate='%{y:,.0f}', textposition='inside')
        
    else:
        fig = px.bar(df[column].value_counts(), title=f"{column} Counts",color_discrete_sequence=px.colors.qualitative.Pastel1)
        fig.update_traces(texttemplate='%{y:,.0f}', textposition='inside',textfont_size=70)

    st.plotly_chart(fig)