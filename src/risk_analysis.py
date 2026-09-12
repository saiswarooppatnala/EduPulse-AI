import pandas as pd
import joblib


def analyze_all_students():
    data = pd.read_csv("data/student_data.csv")
    model = joblib.load("models/edupulse_model.pkl")
    features = joblib.load("models/features.pkl")

    predictions = model.predict(data[features])

    data["Student ID"] = [
        f"Student {i:03d}" for i in range(1, len(data) + 1)
    ]

    data["Predicted Score"] = predictions.round(2)

    data["Risk Level"] = data["Predicted Score"].apply(
        lambda score:
        "High Risk" if score < 50
        else "Medium Risk" if score < 75
        else "Low Risk"
    )

    return data