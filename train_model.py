import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

data = pd.read_csv("dataset/safety_data.csv")

X = data[["crime_rate","crowd_density","lighting","time"]]
y = data["safety"]

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X,y)

joblib.dump(model,"model/safety_model.pkl")

print("Model saved successfully!")