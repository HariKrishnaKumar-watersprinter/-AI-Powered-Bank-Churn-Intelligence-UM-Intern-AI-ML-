import pandas as pd

def load_data():
    path=r'https://raw.github.com/HariKrishnaKumar-watersprinter/-AI-Powered-Bank-Churn-Intelligence-UM-Intern-AI-ML-/main/data/European_Bank.csv'
    
    df = pd.read_csv(path)
    return df
