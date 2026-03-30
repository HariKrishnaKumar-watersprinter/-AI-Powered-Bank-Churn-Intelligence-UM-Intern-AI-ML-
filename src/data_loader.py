import pandas as pd

def load_data():
    path=r'F:\Project\unified mentor\Bank churn Prediction\data\European_Bank.csv'
    
    df = pd.read_csv(path)
    return df