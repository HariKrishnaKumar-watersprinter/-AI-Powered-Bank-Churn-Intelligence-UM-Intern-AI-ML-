import sys
sys.path.append('.')

import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
from src.data_loader import load_data
from src.data_quality import data_quality_report, detect_outliers
from src.feature_engineering import create_features
from utils.retention_engine import personalized_strategy
from prediction import predict_ch
from database import database_content
from Authentication import main
# -----------------------------
# ⚙️ CONFIG
# -----------------------------
st.set_page_config(
    page_title="Churn Intelligence System",
    layout="wide",page_icon='🏦',initial_sidebar_state="collapsed"
)

# -----------------------------
# 🎨 CUSTOM UI (SaaS STYLE)
# -----------------------------
# Custom CSS
st.markdown("""
<style>
.main {
    background-color: #0E1117;
    color: white;
}
h1, h2, h3 {
    color: #00C6FF;
}
.metric-container {
    background-color: #1E222A;
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)
# -----------------------------
# 📂 LOAD DATA + MODEL
# -----------------------------
@st.cache_data
def get_processed_data():
    df = load_data()
    df = create_features()
    return df

# --- Internal Page Functions ---
def home_page():
    st.title("🏦 AI-Powered Bank Customer Churn Intelligence")
    st.markdown("""
### 🚀 Predict • Analyze • Explain • Prevent Customer Churn
""")
    st.markdown("## 📊 Overview")
    col1, col2, col3,col4 = st.columns(4)
    col1.metric("Total Customers", len(df))
    col2.metric("Churn Rate", f"{df['Exited'].mean():.2%}")
    col3.metric("Avg Balance", f"{df['Balance'].mean():,.0f}")
    col4.metric("Active Users", f"{df['IsActiveMember'].mean():.2%}")
    st.markdown("""
    ### 💡 Business Problem
    Banks lose customers due to lack of proactive churn prediction.
    ### 🎯 Solution
    This platform predicts churn and provides actionable insights.
    """)

def prediction_page():
    predict_ch.prediction_churn()

def database_page():
    database_content.database_content_view()

# --- Navigation Definition ---
# This list defines the exact order and grouping of your pages
pages = {
    "Main": [
        st.Page(home_page, title="Home", icon="🏠", default=True),
        st.Page(prediction_page, title="Customer Churn Prediction", icon="🔮"),
        st.Page(database_page, title="Database Content", icon="💾"),
    ],
    "Data Insights": [
        st.Page("pages/Data_Quality.py", title="Data Quality", icon="🧹"),
        st.Page("pages/EDA_Dashboard.py", title="Exploratory Analysis", icon="📊"),
        st.Page("pages/Churn_Risk_Distribution_Dashboard.py", title="churn Risk Distribution", icon="📈"),
    ],
    "Model Analysis": [
        st.Page("pages/ModelComparison.py", title="Model Selection and comparison", icon="⚖️"),
        st.Page("pages/ThresholdOptimization.py", title="Thresholds", icon="🎯"),
        st.Page("pages/Model_Explainability.py", title="Explainability", icon="🧠"),
    ],
    "Strategy & Risk": [
        st.Page("pages/What_If_Simulator.py", title="What-if Simulator", icon="🎲"),
        st.Page("pages/Cost_Analysis.py", title="Cost Analysis", icon="💰"),
        st.Page("pages/Dependency_Risk.py", title="Dependency Risk", icon="⚠️"),
    ],
    "Government": [
        st.Page("pages/Executive Summary for Government Stakeholders.py", title="Executive Summary", icon="🏛️"),
    ]
}

if __name__ == "__main__":
    # 1. Handle Authentication First
   auth_status = main.user_auth()

   if auth_status:
        df = get_processed_data()
        
        # Initialize and run Navigation
        pg = st.navigation(pages)
        pg.run()
