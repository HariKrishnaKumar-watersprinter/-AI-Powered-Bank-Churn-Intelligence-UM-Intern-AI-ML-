import pandas as pd
from src.data_loader import load_data
def churn_distribution(df):
    return df["Exited"].value_counts()

def churn_by_category(df, column):
    return pd.crosstab(df[column], df["Exited"]) 

def correlation_matrix(df):
    return df.corr(numeric_only=True)


def univariate_summary(df):
    summary = df.describe(include='all')
    return summary

def bivariate_analysis(df, col1, col2):
    return pd.crosstab(df[col1], df[col2], normalize='index')

def multivariate_corr(df):
    return df.corr(numeric_only=True)

def numerical_stats(df):
    stats = {}

    num_cols = df.select_dtypes(include=['int64','float64']).columns
    num_cols=num_cols.drop(['CustomerId','Year'])
    for col in num_cols:
        
        stats[col] = {
            "mean": df[col].mean(),
            "median": df[col].median(),
            "std": df[col].std(),
            'max':df[col].max(),
            'min':df[col].min(),
            "25%": df[col].quantile(0.25),
            "75%": df[col].quantile(0.75),
            "skew": df[col].skew(),
            "kurtosis": df[col].kurt()
        }

    return pd.DataFrame(stats).T