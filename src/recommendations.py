def get_risk_level(score):
    if score >= 75:
        return "Low Risk"
    elif score >= 50:
        return "Medium Risk"
    else:
        return "High Risk"


def get_recommendations(
    study_hours,
    attendance,
    assignments_completed,
    quiz_average,
    screen_time
):
    recommendations = []

    if study_hours < 4:
        recommendations.append("Increase daily study time.")

    if attendance < 75:
        recommendations.append("Improve attendance.")

    if assignments_completed < 7:
        recommendations.append("Complete more assignments.")

    if quiz_average < 60:
        recommendations.append("Practice more quiz questions.")

    if screen_time > 6:
        recommendations.append("Reduce daily screen time.")

    if not recommendations:
        recommendations.append("Keep up your current learning routine.")

    return recommendations


def get_student_insights(
    study_hours,
    attendance,
    previous_score,
    sleep_hours,
    assignments_completed,
    quiz_average,
    screen_time
):
    strengths = []
    attention = []

    if study_hours >= 6:
        strengths.append("Strong daily study commitment.")

    if attendance >= 85:
        strengths.append("Excellent attendance.")

    if previous_score >= 75:
        strengths.append("Strong previous academic performance.")

    if sleep_hours >= 7:
        strengths.append("Healthy sleep routine.")

    if assignments_completed >= 8:
        strengths.append("Good assignment completion.")

    if quiz_average >= 75:
        strengths.append("Strong quiz performance.")

    if screen_time <= 5:
        strengths.append("Good control of screen time.")

    if study_hours < 4:
        attention.append("Study time is below the recommended level.")

    if attendance < 75:
        attention.append("Attendance needs improvement.")

    if previous_score < 60:
        attention.append("Previous academic performance is a concern.")

    if sleep_hours < 6:
        attention.append("Sleep duration may be affecting learning.")

    if assignments_completed < 7:
        attention.append("More assignments should be completed.")

    if quiz_average < 60:
        attention.append("Quiz performance needs improvement.")

    if screen_time > 6:
        attention.append("High screen time may affect study consistency.")

    if not strengths:
        strengths.append("The student has several areas that can be improved.")

    if not attention:
        attention.append("No major warning areas detected.")

    return strengths, attention
def generate_performance_summary(
    score,
    study_hours,
    attendance,
    previous_score,
    sleep_hours,
    assignments_completed,
    quiz_average,
    screen_time
):
    if score >= 85:
        performance = "strong"
    elif score >= 70:
        performance = "good"
    elif score >= 50:
        performance = "moderate"
    else:
        performance = "needs improvement"

    strengths = []

    if previous_score >= 75:
        strengths.append("previous academic performance")

    if quiz_average >= 75:
        strengths.append("quiz performance")

    if attendance >= 85:
        strengths.append("attendance")

    if study_hours >= 6:
        strengths.append("study consistency")

    if sleep_hours >= 7:
        strengths.append("sleep routine")

    if not strengths:
        strength_text = "There are currently no major strengths detected."
    elif len(strengths) == 1:
        strength_text = f"The main strength is {strengths[0]}."
    else:
        strength_text = (
            "The strongest areas are "
            + ", ".join(strengths[:-1])
            + " and "
            + strengths[-1]
            + "."
        )

    improvements = []

    if study_hours < 4:
        improvements.append("increasing study time")

    if attendance < 75:
        improvements.append("improving attendance")

    if quiz_average < 60:
        improvements.append("improving quiz performance")

    if assignments_completed < 7:
        improvements.append("completing more assignments")

    if sleep_hours < 6:
        improvements.append("maintaining a better sleep routine")

    if screen_time > 6:
        improvements.append("reducing screen time")

    if not improvements:
        improvement_text = "Maintaining the current learning routine should help sustain performance."
    elif len(improvements) == 1:
        improvement_text = f"The student could focus on {improvements[0]} to improve further."
    else:
        improvement_text = (
            "The student could focus on "
            + ", ".join(improvements[:-1])
            + " and "
            + improvements[-1]
            + " to improve further."
        )

    summary = (
        f"The student is currently showing {performance} predicted academic performance "
        f"with an estimated score of {score}/100. "
        f"{strength_text} "
        f"{improvement_text}"
    )

    return summary