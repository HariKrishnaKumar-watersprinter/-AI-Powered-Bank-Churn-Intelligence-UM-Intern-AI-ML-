import streamlit as st
import pandas as pd
import plotly.express as px
from dashboard import univariate
from dashboard import bivariate
from dashboard import multivariate
from dashboard import numerical
from src.data_loader import load_data
from src.feature_engineering import create_features

#if not st.session_state.get('authentication_status'):
#    st.switch_page("app.py")

df=load_data()
df=create_features()
st.header("📊 Exploratory Data Analysis")
tabs = st.tabs([
        "Univariate",
        "Bivariate",
        "Multivariate",
        "Numerical"
    ])

    # -------------------------
    # UNIVARIATE
    # -------------------------
with tabs[0]:
        univariate.show(df)

    # -------------------------
    # BIVARIATE
    # -------------------------
with tabs[1]:
        bivariate.show(df)

       

    # -------------------------
    # MULTIVARIATE
    # -------------------------
with tabs[2]:
        multivariate.show(df)

    # -------------------------
    # NUMERICAL
    # -------------------------
with tabs[3]:
        numerical.show(df)