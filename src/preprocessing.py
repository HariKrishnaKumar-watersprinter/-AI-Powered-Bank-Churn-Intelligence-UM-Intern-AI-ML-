import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from src.data_loader import load_data
from src.feature_engineering import create_features
from sklearn.pipeline import Pipeline

def preprocess_data():
    df = create_features()
    # Drop irrelevant columns
    df.drop(['CustomerId', 'Surname','Year'], axis=1, inplace=True)

    # One-hot encoding
    df = pd.get_dummies(df, columns=['Geography', 'Gender'],dtype=int)
    #splitting the data
    x=df.drop('Exited',axis=1)
    y=df['Exited']
    #train_test split
    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42,stratify=y)
    return x_train,x_test,y_train,y_test


def scale_features():
    # Scaling
    x_train,x_test,y_train,y_test=preprocess_data()
    numeric_pipeline = Pipeline([("scaler", StandardScaler())])
    x_train_scaled = numeric_pipeline.fit_transform(x_train)
    x_test_scaled = numeric_pipeline.transform(x_test)
    x_train_scaled=pd.DataFrame(x_train_scaled,columns=x_train.columns)
    x_test_scaled=pd.DataFrame(x_test_scaled,columns=x_test.columns)
    return (numeric_pipeline,x_train_scaled,x_test_scaled)
