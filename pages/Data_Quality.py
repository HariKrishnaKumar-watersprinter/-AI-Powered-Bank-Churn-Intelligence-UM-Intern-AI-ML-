import streamlit as st
from src.data_quality import data_quality_report, detect_outliers
from src.data_loader import load_data
from src.feature_engineering import create_features

#if not st.session_state.get('authentication_status'):
#    st.switch_page("app.py")

def data_quality():
    df=create_features()
    st.header("🧹 Data Quality Assessment")

    quality = data_quality_report()
    st.dataframe(quality)

    st.subheader("⚠️ Outliers")
    outliers = detect_outliers(df)
    st.dataframe(outliers)
data_quality()