import pandas as pd
import joblib

from src.recommendations import (
    get_risk_level,
    get_recommendations,
    get_student_insights,
    generate_performance_summary
)

model = joblib.load("models/edupulse_model.pkl")
features = joblib.load("models/features.pkl")

feature_labels = {
    "study_hours": "Study Hours",
    "attendance": "Attendance",
    "previous_score": "Previous Score",
    "sleep_hours": "Sleep Hours",
    "assignments_completed": "Assignments Completed",
    "quiz_average": "Quiz Average",
    "screen_time": "Screen Time",
    "consistency_score": "Consistency Score"
}


def analyze_student(
    study_hours,
    attendance,
    previous_score,
    sleep_hours,
    assignments_completed,
    quiz_average,
    screen_time,
    consistency_score
):
    student = pd.DataFrame([[
        study_hours,
        attendance,
        previous_score,
        sleep_hours,
        assignments_completed,
        quiz_average,
        screen_time,
        consistency_score
    ]], columns=features)

    prediction = model.predict(student)[0]

    score = round(
        max(0, min(100, float(prediction))),
        2
    )

    risk = get_risk_level(score)

    recommendations = get_recommendations(
        study_hours,
        attendance,
        assignments_completed,
        quiz_average,
        screen_time
    )

    strengths, attention = get_student_insights(
        study_hours,
        attendance,
        previous_score,
        sleep_hours,
        assignments_completed,
        quiz_average,
        screen_time
    )

    summary = generate_performance_summary(
        score,
        study_hours,
        attendance,
        previous_score,
        sleep_hours,
        assignments_completed,
        quiz_average,
        screen_time
    )

    explanations = get_feature_explanations(student)

    return (
        score,
        risk,
        recommendations,
        strengths,
        attention,
        summary,
        explanations
    )


def get_feature_explanations(student):
    training_data = pd.read_csv("data/student_data.csv")

    feature_means = training_data[features].mean()

    contributions = model.coef_ * (
        student.iloc[0].values - feature_means.values
    )

    explanations = []

    for feature, contribution in zip(features, contributions):

        contribution = float(contribution)

        if contribution > 0.5:
            impact = "Positive"
            direction = "helped"
            explanation = (
                f"{feature_labels[feature]} is contributing positively "
                f"to the predicted score."
            )

        elif contribution < -0.5:
            impact = "Negative"
            direction = "reduced"
            explanation = (
                f"{feature_labels[feature]} is reducing the predicted score "
                f"relative to the training-data average."
            )

        else:
            impact = "Neutral"
            direction = "neutral"
            explanation = (
                f"{feature_labels[feature]} has only a small influence "
                f"on the current prediction."
            )

        explanations.append({
            "feature": feature_labels[feature],
            "contribution": round(contribution, 2),
            "impact": impact,
            "direction": direction,
            "explanation": explanation
        })

    explanations.sort(
        key=lambda x: abs(x["contribution"]),
        reverse=True
    )

    return explanations


def what_if_analysis(
    study_hours,
    attendance,
    previous_score,
    sleep_hours,
    assignments_completed,
    quiz_average,
    screen_time,
    consistency_score,
    new_study_hours=None,
    new_attendance=None,
    new_screen_time=None
):
    current_score = analyze_student(
        study_hours,
        attendance,
        previous_score,
        sleep_hours,
        assignments_completed,
        quiz_average,
        screen_time,
        consistency_score
    )[0]

    updated_study_hours = (
        new_study_hours
        if new_study_hours is not None
        else study_hours
    )

    updated_attendance = (
        new_attendance
        if new_attendance is not None
        else attendance
    )

    updated_screen_time = (
        new_screen_time
        if new_screen_time is not None
        else screen_time
    )

    updated_consistency_score = (
        consistency_score
        + (updated_study_hours - study_hours) * 0.5
        + (updated_attendance - attendance) * 0.3
        - (updated_screen_time - screen_time) * 0.2
    )

    updated_consistency_score = max(
        0,
        min(100, updated_consistency_score)
    )

    new_score = analyze_student(
        updated_study_hours,
        updated_attendance,
        previous_score,
        sleep_hours,
        assignments_completed,
        quiz_average,
        updated_screen_time,
        updated_consistency_score
    )[0]

    improvement = round(
        new_score - current_score,
        2
    )

    return current_score, new_score, improvement