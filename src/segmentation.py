from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from src.feature_engineering import create_features
def create_segments():
    df=create_features()

    features = df[["Age", "Balance", "EstimatedSalary",'Exited']]
  
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features)

    kmeans = KMeans(n_clusters=4, random_state=42)
    df["Segment"] = kmeans.fit_predict(X_scaled)

    return df,features