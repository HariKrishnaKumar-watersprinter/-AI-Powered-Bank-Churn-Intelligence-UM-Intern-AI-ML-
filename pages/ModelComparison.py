import os
import pandas as pd
import joblib
from src.model_training1 import model_training
from model_tracking.mlflow_track import track_model
from pathlib import Path
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
# Authentication Guard 
#if not st.session_state.get('authentication_status'):
    #st.switch_page("app.py")

# Using relative path to prevent app from hanging/crashing on different machines
BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_FOLDER = BASE_DIR / "best model"
RESULTS_CSV = BASE_DIR / "data/results.csv"

def init_session_state():
    """Initializes session state variables if they don't exist."""
    if 'loaded_model' not in st.session_state:
        st.session_state['loaded_model'] = None
    if 'selected_model_name' not in st.session_state:
        st.session_state['selected_model_name'] = None

# Model selection
def render_model_selection():
    """UI for picking and loading a saved model."""
    st.subheader("🗂️ Model Selection")

    if MODEL_FOLDER.exists() and MODEL_FOLDER.is_dir():
        model_files = [f for f in os.listdir(MODEL_FOLDER) if f.endswith('.pkl')]
        
        if not model_files:
            st.warning(f"No .pkl models found in {MODEL_FOLDER}")
            return

        # Determine current index for the selectbox
        current_sel = st.session_state.get('selected_model_name')
        default_idx = model_files.index(current_sel) if current_sel in model_files else 0
        
        selected = st.selectbox("Choose a trained model for active prediction:", model_files, index=default_idx)

        # Logic to load model if selection changes
        if selected != st.session_state['selected_model_name']:
            try:
                with st.spinner(f"Loading {selected}..."):
                    model_path = MODEL_FOLDER / selected
                    st.session_state['loaded_model'] = joblib.load(model_path)
                    st.session_state['selected_model_name'] = selected
                st.toast(f"Active model updated: {selected}", icon="✅")
            except Exception as e:
                st.error(f"Failed to load model: {e}")
    else:
        st.error(f"Model directory not found: {MODEL_FOLDER}")
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Model Accuracy", "82%+")
    col2.metric("ROC-AUC", "86%+")
    col3.metric("Churn Detection Recall", "71%+")
    col4.metric("Cost Reduction", "Significant")
    
def render_performance_dashboard():
    """Displays retraining options and evaluation charts."""
    st.subheader("📊 Performance Comparison")
    
    results = None
    if RESULTS_CSV.exists():
        try:
            results = pd.read_csv(RESULTS_CSV)
        except Exception:
            results = None

    # Check if results dataframe was actually loaded, not just the path object
    if results is not None:
        # Plotly Comparison Chart
        fig = px.bar(
            results,
            x="Model",
            y='ROC-AUC',
            color="class imbalance technique",
            barmode="group",
            title="ROC-AUC Scores by Model and Sampling Technique",
            template="plotly_dark"
        )
        st.plotly_chart(fig, width='stretch')

        # Data Table
        st.write("### Detailed Metrics")
        st.dataframe(results.sort_values(by="ROC-AUC", ascending=False))
        
        if st.button('🔄 Retrain All Models'):
            with st.spinner("Executing training pipeline..."):
                model_training()
                st.success("Training Complete!")
                st.rerun()
    else:
        st.warning("No training results found in data/results.csv.")
        if st.button('🚀 Start Initial Training'):
            with st.spinner("Training initial models..."):
                model_training()
            st.rerun()

def render_tracking_section():
    """UI for MLflow tracking."""
    st.subheader("📈 Experiment Tracking")
    st.info("Log the current best model performance to MLflow for versioning and auditing.")
    if st.button('📤 Push to MLflow'):
        with st.spinner("Logging to MLflow..."):
            track_model()
            st.success("Experiment logged successfully!")

# Main Page Execution 
def main():
    st.title("🏆 Model Selection & Analysis")
    init_session_state()

    with st.container(border=True):
        render_model_selection()

    st.divider()
    render_performance_dashboard()

    st.divider()
    render_tracking_section()

if __name__ == "__main__":
    main()
