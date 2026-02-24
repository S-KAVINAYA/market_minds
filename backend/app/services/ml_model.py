from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
import numpy as np

# Dummy training example (replace with real features later)

risk_model = RandomForestClassifier()
segment_model = KMeans(n_clusters=3)

def predict_risk(features):
    return risk_model.predict([features])[0]

def segment_client(features):
    return segment_model.predict([features])[0]
