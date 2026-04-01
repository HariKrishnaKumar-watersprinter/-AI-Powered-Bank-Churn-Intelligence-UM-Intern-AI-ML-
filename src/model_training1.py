import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, recall_score, precision_score, f1_score,classification_report
from sklearn.metrics import roc_auc_score

from xgboost import XGBClassifier
import joblib
from src.data_loader import load_data
from src.preprocessing import preprocess_data,scale_features
import warnings
warnings.filterwarnings('ignore')
import streamlit as st
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import RandomOverSampler, SMOTE, ADASYN
from imblearn.under_sampling import RandomUnderSampler, TomekLinks, AllKNN
from imblearn.combine import SMOTEENN, SMOTETomek
import os
st.cache_data()
def model_training():
    x_train,x_test,y_train,y_test = preprocess_data()
    numeric_pipeline,x_train_scaled,x_test_scaled = scale_features()

# SAMPLING METHODS
    sampling_methods = {
    "None": None,
    "OverSampling": RandomOverSampler(),
    "UnderSampling": RandomUnderSampler(),
    "SMOTE": SMOTE(random_state=42,k_neighbors=5),
    "ADASYN": ADASYN(sampling_strategy=0.8, random_state=42),
    "SMOTEENN": SMOTEENN(random_state=42),
    "SMOTETomek": SMOTETomek(sampling_strategy='auto'),
    "TomekLinks": TomekLinks(sampling_strategy='majority'),
    "AllKNN": AllKNN(sampling_strategy='auto') }

#Params
    logistic_params = {'C': 0.1, 'fit_intercept': False, 'l1_ratio': 0.1, 'max_iter': 50, 'penalty': 'l2', 'solver': 'saga'}
    decision_tree_params = {'class_weight': None, 'criterion': 'entropy', 'max_depth': 7, 'max_features': 'log2', 'min_samples_leaf': 4, 'min_samples_split': 2, 'splitter': 'best'}
    random_forest_params = {'bootstrap': True, 'class_weight': None, 'criterion': 'entropy', 'max_depth': 10, 'max_features': 'sqrt', 'min_samples_leaf': 4, 'min_samples_split': 10, 'n_estimators': 300}
    gradient_boosting_params = {'criterion': 'friedman_mse', 'learning_rate': 0.1, 'max_depth': 3, 'min_samples_leaf': 4, 'min_samples_split': 10, 'n_estimators': 100, 'subsample': 0.8}
    xgboost_params = {'eval_metric':"logloss",'colsample_bytree': 0.9, 'gamma': 4, 'learning_rate': 0.1, 'max_depth': 10, 'min_child_weight': 3, 'n_estimators': 300, 'reg_lambda': 1, 'subsample': 0.9}


# MODELS
    models = {
    "Logistic": LogisticRegression(**logistic_params),
    "DecisionTree": DecisionTreeClassifier(**decision_tree_params),
    "RandomForest": RandomForestClassifier(**random_forest_params),
    "GradientBoosting": GradientBoostingClassifier(**gradient_boosting_params),
    "XGBoost": XGBClassifier(**xgboost_params)}

# TRAIN LOOP
    results = []
    best_model = None
    best_score = 0

    for sampler_name, sampler in sampling_methods.items():
        for model_name, model in models.items():
            print(f"\n🚀 Training {model_name} with {sampler_name}")

            steps = []

            if sampler:
                steps.append(("class imbalance technique", sampler))

            steps.append(("model", model))

            pipeline = Pipeline(steps)

            model=pipeline.fit(x_train_scaled, y_train)

            y_pred = model.predict(x_test_scaled)
            y_pred_prob = model.predict_proba(x_test_scaled)[:, 1]
            auc = roc_auc_score(y_test, y_pred_prob)
            cm = confusion_matrix(y_test, y_pred)
            recall_sc = recall_score(y_test, y_pred,pos_label=1)
            recall_sc0 = recall_score(y_test, y_pred,pos_label=0)
            precision_sc = precision_score(y_test, y_pred)
            f1_sc = f1_score(y_test, y_pred)
            acc=accuracy_score(y_test, y_pred)
            class_rep = classification_report(y_test, y_pred)
        
            results.append({
            "Model": model_name,
            'class imbalance technique':sampler_name,
            "ROC-AUC": auc,
            "churn Recall-1": recall_sc,
            "Non-churn Recall-0": recall_sc0,
            "Precision": precision_sc,
            "F1 Score": f1_sc,
            "Confusion Matrix": cm,
            "Accuracy": acc})


            print(f"✅ {model_name} AUC: {auc:.4f}")
            print(f"churn Recall: {recall_sc}")
            print(f"Non-churn Recall: {recall_sc0}")
            print(f"Precision: {precision_sc}")
            print(f"F1 Score: {f1_sc}")
            print(f"Confusion Matrix: {cm}")
            print(f"Accuracy: {acc}")
            print(f'classification report: {class_rep}')
           
            if auc > best_score:
                best_score = auc
            #save the models
            os.makedirs("model", exist_ok=True)
            filename = f"model/{model_name}_{sampler_name}.pkl"
            joblib.dump(model, filename)

# RESULTS
    results_df = pd.DataFrame(results).sort_values(by="ROC-AUC", ascending=False).reset_index(drop=True)
    os.cwd("data")
    filename = f"data/results.csv'"
    results_df.to_csv(data,filename)
    print("\n🏆 FINAL RESULTS")
    print(results_df.head(10))

    print("\n💾 Best model with sampling saved!")
    return logistic_params, decision_tree_params, random_forest_params, gradient_boosting_params, xgboost_params
