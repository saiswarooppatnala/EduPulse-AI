import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


data = pd.read_csv("data/student_data.csv")

features = [
    "study_hours",
    "attendance",
    "previous_score",
    "sleep_hours",
    "assignments_completed",
    "quiz_average",
    "screen_time",
    "consistency_score"
]

X = data[features]
y = data["final_score"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

models = {
    "Linear Regression": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(
        max_depth=5,
        random_state=42
    ),
    "Random Forest": RandomForestRegressor(
        n_estimators=150,
        max_depth=8,
        random_state=42
    ),
    "Gradient Boosting": GradientBoostingRegressor(
        n_estimators=100,
        learning_rate=0.05,
        max_depth=3,
        random_state=42
    )
}

results = {}

for name, model in models.items():
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    results[name] = {
        "model": model,
        "mae": mean_absolute_error(y_test, predictions),
        "rmse": mean_squared_error(y_test, predictions) ** 0.5,
        "r2": r2_score(y_test, predictions)
    }

for name, result in results.items():
    print(
        f"{name}: "
        f"MAE={result['mae']:.2f}, "
        f"RMSE={result['rmse']:.2f}, "
        f"R²={result['r2']:.3f}"
    )

best_name = max(
    results,
    key=lambda name: results[name]["r2"]
)

best_model = results[best_name]["model"]

model_results = {
    name: {
        "mae": result["mae"],
        "rmse": result["rmse"],
        "r2": result["r2"]
    }
    for name, result in results.items()
}

joblib.dump(best_model, "models/edupulse_model.pkl")
joblib.dump(features, "models/features.pkl")
joblib.dump(model_results, "models/model_results.pkl")

print(f"\nBest model: {best_name}")
print(f"R² Score: {results[best_name]['r2']:.3f}")