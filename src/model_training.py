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
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import RandomOverSampler, SMOTE, ADASYN
from imblearn.under_sampling import RandomUnderSampler, TomekLinks, AllKNN
from imblearn.combine import SMOTEENN, SMOTETomek
import warnings
warnings.filterwarnings('ignore')
import streamlit as st

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
    "AllKNN": AllKNN(sampling_strategy='auto')}

# MODELS
    models = {
    "Logistic": LogisticRegression(max_iter=1000),
    "DecisionTree": DecisionTreeClassifier(),
    "RandomForest": RandomForestClassifier(),
    "GradientBoosting": GradientBoostingClassifier(),
    "XGBoost": XGBClassifier(eval_metric="logloss")}


# HYPERPARAMETERS
    param_grids = {
    "Logistic": {
    'model__C': [0.001, 0.01, 0.1, 1, 10, 100, 1000],
    'model__penalty': ['l2'],
    'model__solver': ['lbfgs', 'sag', 'saga'],
    'model__l1_ratio': [0.1,0.3, 0.5,0.7, 0.9,1.0],  
    'model__max_iter': [50,100, 300,500],
    'model__fit_intercept': [True, False],
    },
    "DecisionTree": {
    'model__criterion': ['gini', 'entropy'],
    'model__max_depth': [None, 3, 5, 7, 10],
    'model__min_samples_split': [2, 5, 10],
    'model__min_samples_leaf': [1, 2, 4],
    'model__max_features': [ 'sqrt', 'log2'],
    'model__class_weight': ['balanced', None],
    'model__splitter': ['best', 'random']},
    
    "RandomForest": {
    'model__n_estimators': [50, 100, 200,300],
    'model__max_depth': [None, 3, 5, 7, 10],
    'model__min_samples_split': [2, 5, 10],
    'model__min_samples_leaf': [1, 2, 4],
    'model__max_features': [ 'sqrt', 'log2'],
    'model__class_weight': ['balanced', None],
    'model__criterion': ['gini', 'entropy'],
    'model__bootstrap': [True, False]},
    
    "GradientBoosting": {
    'model__n_estimators': [50, 100, 200,300],
    'model__max_depth': [3, 5, 7],
    'model__learning_rate': [0.01, 0.1, 0.2],
    'model__subsample': [0.8, 0.9, 1.0],
    'model__min_samples_split': [2, 5, 10],
    'model__min_samples_leaf': [1, 2, 4],
    'model__criterion': ['friedman_mse', 'squared_error']},
    
    "XGBoost": {
    'model__n_estimators': [50, 100, 200,300],
    'model__learning_rate': [0.1, 0.2, 0.3],
    'model__max_depth': [ 3, 5, 7, 10],
    'model__min_child_weight': [ 3, 5, 7, 10], 
    'model__subsample': [0.8, 0.9, 1.0],
    'model__colsample_bytree': [0.8, 0.9, 1.0],
    'model__gamma': [1, 2, 3, 4],
    'model__reg_lambda':[1,2,3,4,5]}}


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

            params = param_grids.get(model_name, {})

            grid = GridSearchCV(
                pipeline,
                params,
                cv=5,
                scoring="roc_auc",
                n_jobs=-1)

            model=grid.fit(x_train_scaled, y_train)

            y_pred = grid.predict(x_test_scaled)
            y_pred_prob = grid.predict_proba(x_test_scaled)[:, 1]
            auc = roc_auc_score(y_test, y_pred_prob)
            cm = confusion_matrix(y_test, y_pred)
            recall_sc = recall_score(y_test, y_pred)
            precision_sc = precision_score(y_test, y_pred)
            f1_sc = f1_score(y_test, y_pred)
            acc=accuracy_score(y_test, y_pred)
            class_rep = classification_report(y_test, y_pred)
        
            results.append({
            "Model": model_name,
            'class imbalance technique':sampler_name,
            "ROC-AUC": auc,
            "Best Params": grid.best_params_,
            "Recall": recall_sc,
            "Precision": precision_sc,
            "F1 Score": f1_sc,
            "Confusion Matrix": cm,
            "Accuracy": acc})


            print(f"✅ {model_name} AUC: {auc:.4f}")
            print(f"Best Params: {grid.best_params_}")
            print(f"Recall: {recall_sc}")
            print(f"Precision: {precision_sc}")
            print(f"F1 Score: {f1_sc}")
            print(f"Confusion Matrix: {cm}")
            print(f"Accuracy: {acc}")
            print(f'classification report: {class_rep}')
            joblib.dump(model, f"F:/Project/unified mentor/Bank churn Prediction/model/{model_name}_{sampler_name}.pkl")
            if auc > best_score:
                best_score = auc
                best_model = grid.best_estimator_


# RESULTS
    results_df = pd.DataFrame(results).sort_values(by="ROC-AUC", ascending=False).reindex()

    print("\n🏆 FINAL RESULTS")
    print(results_df.head(10))

# SAVE BEST MODEL
    print("\n💾 Best model with sampling saved!")
