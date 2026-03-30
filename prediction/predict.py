import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go
from utils.helpers import risk_segment
from src.feature_engineering import create_features
from prediction.predict_model import predict_churn
from utils.recommendation import retention_action
from utils.retention_engine import personalized_strategy
from utils.recommendation import retention_action
from database.database_create import  BankCustomer,save_data


def prediction():
    st.header("🔮 Customer Churn Prediction")
    st.markdown("### Enter the customer details to predict churn risk")
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
        
        

    input_df = pd.DataFrame([{
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
    
      # Avoid division by zero
    input_df['BalanceSalaryRatio'] = input_df['Balance'] / (input_df['EstimatedSalary'] + 1)

    # Product density
    input_df['ProductDensity'] = input_df['NumOfProducts'] / (input_df['Tenure'] + 1)

    # Engagement feature
    input_df['EngagementScore'] = input_df['IsActiveMember'] * input_df['NumOfProducts']

    # Age-Tenure interaction
    input_df['AgeTenureRatio'] = input_df['Age'] / (input_df['Tenure'] + 1)
    
    input_df = pd.get_dummies(input_df, columns=['Geography'], dtype=int)
    expected_columns = ['Geography_France', 'Geography_Germany', 'Geography_Spain']
    for col in expected_columns:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = pd.get_dummies(input_df, columns=['Gender'], dtype=int)
    expected_columns = ['Gender_Female','Gender_Male']
    for col in expected_columns:
        if col not in input_df.columns:
            input_df[col] = 0
    possible_cols = [
        'CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts',
        'HasCrCard', 'IsActiveMember', 'EstimatedSalary',
        'BalanceSalaryRatio', 'ProductDensity', 'EngagementScore', 'AgeTenureRatio','Geography_France',
        'Geography_Germany', 'Geography_Spain',
        'Gender_Female','Gender_Male'
    ]
    input_df = input_df.reindex(columns=possible_cols)
   
    
    if st.button("Predict"):
        prob,pred,_ = predict_churn(input_df)
        segment = risk_segment(prob)
        action = retention_action(prob)
        st.write(f"# Customer ID: {int(CustomerId)}")
        st.write(f"#### Churn Prediction: {pred}")
        st.write(f"#### Churn Probability: {prob:.2f}")
        if pred == 1 and prob > 0.5:
            st.error("⚠️ customer is churn")
        else:
            st.success("✅ customer is not churn:")
        st.write('## Risk condition and Retention strategy:')
        st.write(f"#### Risk Segment: {segment}")
        st.write(f"#### Recommended Action: {action}")
        

        strategy = personalized_strategy(input_df.iloc[0], prob)

        st.write(f"#### Personalized Strategy: {strategy}") 
        save_data(CustomerId,credit,geography,gender,age,tenure,balance,products,HasCrCard,active,salary)
        st.success("Data saved successfully")
        return input_df
if __name__ == "__main__":
    prediction()
