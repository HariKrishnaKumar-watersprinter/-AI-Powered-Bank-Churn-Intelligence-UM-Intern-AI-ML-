# 🏦 AI-Powered Bank Customer Churn Prediction & Risk Intelligence System
Deployed link : https://ai-powered-bank-churn-intelligence.streamlit.app/
---

## 🚀 Overview

This project is a **full-stack, production-ready AI application** designed to predict customer churn in the banking sector and provide **actionable insights, explainability, and retention strategies**.

It goes beyond traditional ML by integrating:

* 🔮 Predictive Modeling
* 🧠 Explainable AI (SHAP)
* 👥 Customer Segmentation
* 🎯 Personalized Retention Engine
* 📊 Interactive Streamlit Dashboard
* 🔐 Secure Authentication System (Login / Signup / Password Recovery)
* 📊 Automated report generation (PDF)
---

## 🎯 Problem Statement

Customer churn leads to:

* 💸 Loss of Customer Lifetime Value (CLV)
* 📉 Revenue instability
* ⚠️ Inefficient retention strategies

Traditional systems are **reactive**.
This project builds a **proactive churn intelligence platform**.

---

## 🧠 Key Features

### 🔮 Predictive Modeling

* Logistic Regression (Baseline)
* Decision Tree
* Random Forest
* Gradient Boosting
* XGBoost

✔ Hyperparameter tuning
✔ Pipeline-based architecture
✔ Class imbalance handling:

* SMOTE
* ADASYN
* SMOTEENN
* Tomek Links
* AllKNN

---

### 📊 Exploratory Data Analysis (EDA)

* ✅ Univariate Analysis
* ✅ Bivariate Analysis
* ✅ Multivariate Analysis
* ✅ Statistical/Numerical Analysis

---

### 🧠 Explainable AI

* SHAP Feature Importance
* SHAP Summary Plots
* Model Transparency & Interpretability

---

### 🎯 Retention Intelligence Engine

* Personalized recommendations based on:

  * Churn probability
  * Customer behavior
  * Product usage

---

### 📄 Executive Summary Module

* Government-ready insights
* Business impact analysis
* Policy-level recommendations
* Downloadable reports

---

### 🔐 Authentication System

* Login
* Signup
* Forgot Password Recovery

Ensures **secure and role-based access** to the application.

---

## 🖥️ Streamlit Dashboard

Interactive modules:

* 📄 Executive Summary
* 📊 EDA Dashboard
* 🔮 Churn Prediction
* 📈 Model Comparison
* 🧠 Explainability
* 👥 Segmentation
* 🎯 What-if Scenario Simulator

---

## 🧪 Tech Stack

### 👨‍💻 Backend / ML

* Python
* Scikit-learn
* XGBoost
* Imbalanced-learn
* SHAP
* pandas
* numpy
* reportlab
* mlflow

### 💾 Database
* SQLAlchemy (PostgreSQL)

### 📊 Visualization

* Plotly
* Matplotlib
* Seaborn

### 🌐 Frontend

* Streamlit

### 🔐 Authentication

* Custom Authentication System (Login/Signup/Recovery)

---
## 📁 Project Structure

```text
├── Authentication/           # Security & User Management
│   ├── config.py             # Authentication configuration & YAML loader
│   ├── config.yaml           # Hashed credentials and session settings
│   ├── main.py               # Authentication entry point (Login/Signup/Forgot PW)
│   └── signup.py             # New user registration logic
│
├── data/                     # Data Storage
│   ├── European_Bank.csv     # Raw dataset
│   └── results.csv           # Performance metrics from the training pipeline
│
├── database/                 # Persistence Layer
│   ├── bank_data.db          # SQLite database (Local storage)
│   ├── database_content.py   # Streamlit view for exploring saved records
│   └── database_create.py    # SQLAlchemy models and DB connection logic
│
├── model_tracking/           # Experiment Tracking
│   └── mlflow_tracking.py    # Integration with MLflow for logging runs and models
│
├── pages/                    # Streamlit Multi-page UI
│   ├── Churn_Risk_Distribution_Dashboard.py # Risk segmentation & Geo-analysis
│   ├── Cost_Analysis.py      # Business cost vs. threshold optimization
│   ├── Data_Quality.py       # Data health and outlier detection reports
│   ├── Dependency_Risk.py    # Customer dependency risk metrics
│   ├── EDA_Dashboard.py      # Tabbed Exploratory Data Analysis
│   ├── Executive Summary for Government Stakeholders.py # High-level summary & PDF export
│   ├── Model_Explainability.py # SHAP-based feature importance visuals
│   ├── ModelComparison.py    # Model selection and retraining interface
│   ├── ThresholdOptimization.py # Precision-Recall curve analysis
│   └── What_If_Simulator.py  # Interactive churn probability calculator
│
├── src/                      # Core Machine Learning Pipeline
│   ├── data_loader.py        # Dataset ingestion
│   ├── data_quality.py       # Statistical checks and quality reporting
│   ├── eda.py                # Analytical functions for dashboards
│   ├── executive_summary.py  # Business logic for the executive report
│   ├── explainability.py     # SHAP value generation logic
│   ├── feature_engineering.py # Derived metrics (BalanceSalaryRatio, etc.)
│   ├── model_training.py     # GridSearch & Hyperparameter tuning pipeline
│   ├── model_training1.py    # Optimized training loop with sampling techniques
│   ├── preprocessing.py      # Scaling, Encoding, and Train-Test splitting
│   └── segmentation.py       # KMeans clustering for customer segmentation
│
├── utils/                    # Helper Utilities & Business Logic
│   ├── cost.py               # Financial cost function for predictions
│   ├── helpers.py            # General risk mapping helpers
│   ├── recommendation.py     # Retention action logic
│   ├── report_generator.py   # PDF generation using ReportLab
│   ├── retention_engine.py   # Personalized strategy logic
│   ├── risk_metrics.py       # Customer risk scoring algorithms
│   └── threshold.py          # Metric calculations across various thresholds
│
├── best model/               # Production-ready .pkl model artifacts
├── app.py                    # Main Streamlit application entry point
└── requirements.txt          # Project dependencies
```
```

---

## ⚙️ Installation

```bash
git clone https://github.com/your-username/bank-churn-ai.git
cd bank-churn-ai

pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

---

## 📊 Model Performance

* 🎯 ROC-AUC: ~0.87+
* 📈 Turn a churn recall rate from 50% t0 71%+
* ⚖️ Balanced Precision-Recall

---

## 💡 Key Insights

* 📌 Inactive customers have highest churn risk
* 📌 Low product usage strongly drives churn
* 📌 Age & geography influence behavior
* 📌 Engagement is the strongest predictor

---

## 🏦 Business Impact

* 📉 Reduced churn rate
* 💰 Increased customer retention
* 📊 Optimized marketing & retention cost
* 🎯 Data-driven decision making

---

## 🏛️ Government & Policy Impact

* ✔ Promotes Responsible AI
* ✔ Ensures transparency via explainability
* ✔ Supports financial system stability
* ✔ Enables data-driven governance

---

## 🧠 Future Enhancements

* 📡 Real-time prediction API
* 🤖 Deep Learning models
* ☁️ Cloud deployment (AWS / Azure)

---

## 🎤 Author

**Hari Krishna Kumar -AI,ML,Data Science & Analytics Enthusiast**

---

## ⭐ Final Note

> This project is not just a machine learning model —
> it is a **complete AI-powered decision intelligence system** for banking.

---

