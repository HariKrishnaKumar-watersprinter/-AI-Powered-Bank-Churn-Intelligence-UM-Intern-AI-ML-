import pandas as pd
from src.data_loader import load_data

def create_features():
    df1=load_data()
    # Balance-Salary Ratio

    # Avoid division by zero
    df1['BalanceSalaryRatio'] = df1['Balance'] / (df1['EstimatedSalary'] + 1)

    # Product density
    df1['ProductDensity'] = df1['NumOfProducts'] / (df1['Tenure'] + 1)

    # Engagement feature
    df1['EngagementScore'] = df1['IsActiveMember'] * df1['NumOfProducts']

    # Age-Tenure interaction
    df1['AgeTenureRatio'] = df1['Age'] / (df1['Tenure'] + 1)

    return df1