import streamlit as st
import pandas as pd
from prediction.predict_model import predict_churn

#if not st.session_state.get('authentication_status'):
    #st.switch_page("app.py")

st.title("🎯 What-if Scenario Simulator")

col1, col2 = st.columns(2)
    

with col1:
    CustomerId=st.number_input('CustomerId',0,16000000,0)
    credit = st.number_input("Credit Score", 300, 900, 600)
    age = st.number_input("Age", 18, 80, 40)
    gender = st.selectbox("Gender", ["Male","Female"])
    geography = st.selectbox("Geography", ["France","Spain","Germany"])
    tenure = st.number_input("Tenure", 0, 10, 5)
        
  
with col2:
    products = st.selectbox("Products", [1,2,3,4])
    active = st.selectbox("Active Member", [0,1])
    HasCrCard = st.number_input('HasCrCard',0,1)
    balance = st.number_input("Balance", 0.0, 250000.0, 50000.0)
    salary = st.number_input("Salary", 5000.0, 200000.0, 50000.0)

data = pd.DataFrame([{
    "CreditScore": credit,
    "Geography": geography,
    "Gender": gender,
    "Age": age,
    "Tenure": tenure,
    "Balance": balance,
    "NumOfProducts": products,
    "HasCrCard": HasCrCard,
    "IsActiveMember": active,
    "EstimatedSalary": salary
}])
data['BalanceSalaryRatio'] = data['Balance'] / (data['EstimatedSalary'] + 1)
data['ProductDensity'] = data['NumOfProducts'] / (data['Tenure'] + 1)
data['EngagementScore'] = data['IsActiveMember'] * data['NumOfProducts']
data['AgeTenureRatio'] = data['Age'] / (data['Tenure'] + 1)
data = pd.get_dummies(data, columns=['Geography'], dtype=int)
expected_columns = ['Geography_France', 'Geography_Germany', 'Geography_Spain']
for col in expected_columns:
    if col not in data.columns:
        data[col] = 0
data = pd.get_dummies(data, columns=['Gender'], dtype=int)
expected_columns = ['Gender_Female','Gender_Male']
for col in expected_columns:
    if col not in data.columns:
        data[col] = 0
possible_cols = [
    'CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts',
    'HasCrCard', 'IsActiveMember', 'EstimatedSalary',
    'BalanceSalaryRatio', 'ProductDensity', 'EngagementScore', 'AgeTenureRatio','Geography_France',
    'Geography_Germany', 'Geography_Spain','Gender_Female','Gender_Male' ]
data = data.reindex(columns=possible_cols)
    
prob,_,_ = predict_churn(data)

st.metric("New Churn Probability", f"{prob:.2f}")