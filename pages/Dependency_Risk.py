import streamlit as st
import pandas as pd
import plotly.express as px
from src.feature_engineering import create_features
from utils.risk_metrics import dependency_risk

#if not st.session_state.get('authentication_status'):
    #st.switch_page("app.py")

def Dependency_Risk():
    st.header("📊 Customer Dependency Risk Analysis")

    df = create_features()
    df.drop([ 'Surname','Year'], axis=1, inplace=True)

    # Apply risk function
    df['Risk_Level'] = df.apply(dependency_risk, axis=1)

    # Pie chart
    risk_counts = df['Risk_Level'].value_counts().reset_index()
    risk_counts.columns = ['Risk_Level', 'Count']
    st.subheader("Distribution of Customer Risk Levels")
    fig = px.pie(
        risk_counts,
        values='Count',
        names='Risk_Level',
        color_discrete_map={
            "Balanced": "green",
            "Medium Risk": "orange",
            "High Risk": "red"
        }
    )
    
    st.plotly_chart(fig)

    # Show risk distribution by geography
    st.subheader("Risk Distribution by Geography")
    geo_risk = df.groupby(['Geography', 'Risk_Level']).size().reset_index(name='Count')
    fig2 = px.bar(
        geo_risk,
        x='Geography',
        y='Count',
        color='Risk_Level',barmode='group',
        color_discrete_map={
            "Balanced": "green",
            "Medium Risk": "orange",
            "High Risk": "red"
        }

    )
    fig2.update_traces(texttemplate='%{y:,.0f}', textposition='auto')
    st.plotly_chart(fig2)

    # Show risk distribution by products
    st.subheader("Risk Distribution by Number of Products")
    prod_risk = df.groupby(['NumOfProducts', 'Risk_Level']).size().reset_index(name='Count')
    fig3 = px.bar(
        prod_risk,
        x='NumOfProducts',
        y='Count',
        color='Risk_Level',barmode='group',
        color_discrete_map={
            "Balanced": "green",
            "Medium Risk": "orange",
            "High Risk": "red"
        }
    )
    fig3.update_traces(texttemplate='%{y:,.0f}', textposition='auto')
    st.plotly_chart(fig3)
    
    # Show sample customers
    st.subheader("Sample Customers by Risk Level")
    st.dataframe(df[['CustomerId','Risk_Level', 'Balance', 'NumOfProducts', 'IsActiveMember']])
Dependency_Risk()