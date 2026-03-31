import streamlit as st
import pandas as pd
import plotly.express as px
from src.feature_engineering import create_features

def show(df):
    df=create_features()
    df=df.drop(['CustomerId', 'Surname','Year'],axis=1,inplace=False)
    st.header("📊 Multivariate Analysis")

    corr = df.corr(numeric_only=True)

    fig = px.imshow(corr, text_auto=True,title="Correlation Matrix")
    fig.update_layout(height=1000, width=1000,font=dict(size=15))
    st.plotly_chart(fig)


    #fig = px.scatter_matrix(df,
        #dimensions=["Age", "Balance", "EstimatedSalary"], color="Exited")
    #st.plotly_chart(fig)
