import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature
import joblib
from sklearn.metrics import accuracy_score, confusion_matrix, recall_score, precision_score, f1_score,classification_report
from sklearn.metrics import roc_auc_score
from src.preprocessing import preprocess_data,scale_features
from src.model_training1 import model_training
from prediction.predict_model import load_prediction_model 
import os
import streamlit as st
import subprocess
import time
def track_model():
    if "mlflow_server" not in st.session_state:
        try:
            st.session_state.mlflow_server = subprocess.Popen( ["mlflow", "server", "--host", "127.0.0.1", "--port", "5000"],
                                             stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            time.sleep(3)  # give it time to start
        except Exception as e:
            st.warning(f"Could not start MLflow server: {e}")
    model_path = os.path.join(os.getcwd(), "mlartifacts/2")
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
   
    mlflow.set_experiment("Bank churn model")
    with mlflow.start_run():
        x_train,x_test,y_train,y_test = preprocess_data()
        numeric_pipeline,x_train_scaled,x_test_scaled= scale_features()
        model = load_prediction_model()
        
        _,_,_,grad_params,_=model_training()
        y_pred = model.predict(x_test_scaled)
        y_pred_prob = model.predict_proba(x_test_scaled)[:, 1]
        auc = roc_auc_score(y_test, y_pred_prob)
        recall_sc = recall_score(y_test, y_pred)
        recall_sc0=recall_score(y_test,y_pred,pos_label=0)
        precision_sc = precision_score(y_test, y_pred)
        f1_sc = f1_score(y_test, y_pred)
        acc=accuracy_score(y_test, y_pred)
        

        mlflow.log_param("Params", grad_params)
        mlflow.log_metric("Accuracy", acc)
        mlflow.log_metric("Churn Recall", recall_sc)
        mlflow.log_metric('not Churn Recall',recall_sc0)
        mlflow.log_metric("Precision", precision_sc)
        mlflow.log_metric("F1 Score", f1_sc)
        mlflow.log_metric("ROC-AUC", auc)
        mlflow.log_artifact(model_path)
        mlflow.set_tag('Training Info', 'Gradient boosting model for bank customer churn prediction')
        signature = infer_signature(x_test_scaled, model.predict(x_test_scaled))
        mlflow.sklearn.log_model(sk_model=model, artifact_path="bank_model", 
                          signature=signature,input_example=x_train_scaled,registered_model_name="Bank churn model")
        print("Model logged in MLflow")
