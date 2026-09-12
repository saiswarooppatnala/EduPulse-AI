import streamlit as st
import joblib
import pandas as pd
from io import BytesIO

from src.predictor import analyze_student, what_if_analysis
from src.risk_analysis import analyze_all_students
from generate_report import create_report


st.set_page_config(
    page_title="EduPulse AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

model_results = joblib.load("models/model_results.pkl")


if "analysis" not in st.session_state:
    st.session_state.analysis = None


st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

.main-title {
    font-size: 44px;
    font-weight: 800;
    letter-spacing: -1px;
    margin-bottom: 0;
}

.subtitle {
    font-size: 17px;
    opacity: 0.65;
    margin-top: 5px;
    margin-bottom: 25px;
}

.section-title {
    font-size: 25px;
    font-weight: 700;
    margin-top: 10px;
    margin-bottom: 5px;
}

.section-description {
    opacity: 0.65;
    margin-bottom: 20px;
}

div[data-testid="stMetric"] {
    padding: 18px;
    border-radius: 14px;
    border: 1px solid rgba(128, 128, 128, 0.25);
}

[data-testid="stSidebar"] {
    border-right: 1px solid rgba(128, 128, 128, 0.2);
}

.stButton > button {
    border-radius: 10px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.markdown("## 🎓 EduPulse AI")
    st.caption("Student Success & Risk Intelligence")

    st.divider()

    st.markdown("### Navigation")
    st.markdown("📊 Student Analysis")
    st.markdown("🔍 Explainable AI")
    st.markdown("🔮 What-If Simulator")
    st.markdown("📄 Student Report")
    st.markdown("🤖 Model Analytics")

    st.divider()

    st.markdown("### System")
    st.success("AI Model Online")
    st.caption("EduPulse AI v1.0")


st.markdown(
    '<div class="main-title">🎓 EduPulse AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Student Success & Risk Intelligence System</div>',
    unsafe_allow_html=True
)

st.write(
    "Analyze learning behaviour, predict academic performance, "
    "identify risk factors, and generate personalized recommendations."
)


st.markdown(
    '<div class="section-title">👨‍🎓 Student Profile</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    "Enter the student's current academic and lifestyle information."
    "</div>",
    unsafe_allow_html=True
)


academic_col, lifestyle_col = st.columns(2)


with academic_col:

    with st.container(border=True):

        st.markdown("### 📚 Academic Factors")

        study_hours = st.slider(
            "Daily Study Hours",
            1.0,
            10.0,
            5.0,
            0.5
        )

        attendance = st.slider(
            "Attendance (%)",
            50.0,
            100.0,
            85.0,
            1.0
        )

        previous_score = st.slider(
            "Previous Score",
            0.0,
            100.0,
            75.0,
            1.0
        )

        quiz_average = st.slider(
            "Quiz Average",
            0.0,
            100.0,
            80.0,
            1.0
        )


with lifestyle_col:

    with st.container(border=True):

        st.markdown("### 🌱 Lifestyle & Engagement")

        sleep_hours = st.slider(
            "Sleep Hours",
            3.0,
            10.0,
            7.0,
            0.5
        )

        assignments_completed = st.slider(
            "Assignments Completed",
            0,
            10,
            8
        )

        screen_time = st.slider(
            "Daily Screen Time",
            0.0,
            12.0,
            4.0,
            0.5
        )


consistency_score = (
    study_hours * 4
    + attendance * 0.3
    + quiz_average * 0.2
    + sleep_hours * 1.5
)

consistency_score = max(
    0,
    min(100, consistency_score / 2)
)


st.write("")


analyze_col1, analyze_col2, analyze_col3 = st.columns(
    [1.2, 1.2, 4]
)


with analyze_col1:

    analyze_button = st.button(
        "🔍 Analyze Student",
        type="primary",
        use_container_width=True
    )


with analyze_col2:

    reset_button = st.button(
        "↻ Reset Analysis",
        use_container_width=True
    )

    if reset_button:
        st.session_state.analysis = None
        st.rerun()


if analyze_button:

    result = analyze_student(
        study_hours,
        attendance,
        previous_score,
        sleep_hours,
        assignments_completed,
        quiz_average,
        screen_time,
        consistency_score
    )

    st.session_state.analysis = {
        "result": result,
        "study_hours": study_hours,
        "attendance": attendance,
        "previous_score": previous_score,
        "sleep_hours": sleep_hours,
        "assignments_completed": assignments_completed,
        "quiz_average": quiz_average,
        "screen_time": screen_time,
        "consistency_score": consistency_score
    }


analysis = st.session_state.analysis


if analysis is not None:

    (
        score,
        risk,
        recommendations,
        strengths,
        attention,
        summary,
        explanations
    ) = analysis["result"]

    study_hours = analysis["study_hours"]
    attendance = analysis["attendance"]
    previous_score = analysis["previous_score"]
    sleep_hours = analysis["sleep_hours"]
    assignments_completed = analysis["assignments_completed"]
    quiz_average = analysis["quiz_average"]
    screen_time = analysis["screen_time"]
    consistency_score = analysis["consistency_score"]


    if score >= 85:
        performance_level = "Excellent"
        performance_message = (
            "The student is performing at an excellent level."
        )
    elif score >= 70:
        performance_level = "Good"
        performance_message = (
            "The student is showing good academic performance."
        )
    elif score >= 50:
        performance_level = "Moderate"
        performance_message = (
            "The student has moderate academic performance."
        )
    else:
        performance_level = "Needs Improvement"
        performance_message = (
            "The student needs additional academic support."
        )


    best_model_name = max(
        model_results,
        key=lambda name: model_results[name]["r2"]
    )

    best_model_r2 = model_results[best_model_name]["r2"]


    st.divider()

    st.markdown(
        '<div class="section-title">📊 Student Risk Overview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        "AI-generated assessment based on the student profile."
        "</div>",
        unsafe_allow_html=True
    )


    result_col1, result_col2, result_col3 = st.columns(3)


    with result_col1:

        st.metric(
            "Predicted Final Score",
            f"{score}/100"
        )


    with result_col2:

        st.metric(
            "Risk Level",
            risk
        )


    with result_col3:

        st.metric(
            "Performance",
            performance_level
        )


    st.write("")


    progress_col1, progress_col2 = st.columns([2, 1])


    with progress_col1:

        with st.container(border=True):

            st.markdown(
                f"## 🎯 {performance_level}"
            )

            st.markdown(
                f"### Predicted Score: {score}/100"
            )

            st.progress(
                score / 100
            )

            st.write(
                performance_message
            )


    with progress_col2:

        with st.container(border=True):

            st.markdown("### 🤖 AI Status")

            st.success("Prediction Complete")

            st.write(
                f"Best Model: **{best_model_name}**"
            )

            st.write(
                f"R² Score: **{best_model_r2:.3f}**"
            )


    st.divider()

    st.markdown(
        '<div class="section-title">🧠 Student Insights</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        "Key strengths and areas that may require attention."
        "</div>",
        unsafe_allow_html=True
    )


    insight_col1, insight_col2 = st.columns(2)


    with insight_col1:

        with st.container(border=True):

            st.markdown("### ✅ Strengths")

            if strengths:

                for strength in strengths:
                    st.write(f"• {strength}")

            else:
                st.write("No major strengths detected.")


    with insight_col2:

        with st.container(border=True):

            st.markdown("### ⚠️ Areas to Improve")

            if attention:

                for item in attention:
                    st.write(f"• {item}")

            else:
                st.write("No major warning areas detected.")


    st.write("")


    st.markdown(
        '<div class="section-title">🧠 AI Performance Summary</div>',
        unsafe_allow_html=True
    )

    st.info(summary)


    st.divider()

    st.markdown(
        '<div class="section-title">🔍 Explainable AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        "Understand which student factors influenced the prediction."
        "</div>",
        unsafe_allow_html=True
    )


    for explanation in explanations:

        feature = explanation["feature"]
        contribution = explanation["contribution"]
        impact = explanation["impact"]
        explanation_text = explanation["explanation"]

        with st.container(border=True):

            explanation_col1, explanation_col2 = st.columns(
                [3, 1]
            )

            with explanation_col1:

                st.markdown(
                    f"### {feature}"
                )

            with explanation_col2:

                if impact == "Positive":

                    st.success(
                        f"📈 +{contribution:.2f}"
                    )

                elif impact == "Negative":

                    st.error(
                        f"📉 {contribution:.2f}"
                    )

                else:

                    st.info(
                        f"➖ {contribution:.2f}"
                    )

            st.write(
                f"**Impact:** {impact}"
            )

            st.write(
                explanation_text
            )


    st.subheader("📊 Feature Influence")


    explanation_chart = pd.DataFrame({
        "Factor": [
            explanation["feature"]
            for explanation in explanations
        ],
        "Influence": [
            explanation["contribution"]
            for explanation in explanations
        ]
    })


    st.bar_chart(
        explanation_chart,
        x="Factor",
        y="Influence"
    )


    st.divider()

    st.markdown(
        '<div class="section-title">📈 Performance Analytics</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        "Overview of the student's academic and lifestyle factors."
        "</div>",
        unsafe_allow_html=True
    )


    analytics_col1, analytics_col2 = st.columns(2)


    with analytics_col1:

        with st.container(border=True):

            st.markdown("### 📚 Academic Factors")

            learning_data = pd.DataFrame({
                "Factor": [
                    "Study Hours",
                    "Attendance",
                    "Previous Score",
                    "Quiz Average"
                ],
                "Value": [
                    study_hours,
                    attendance,
                    previous_score,
                    quiz_average
                ]
            })

            st.bar_chart(
                learning_data,
                x="Factor",
                y="Value"
            )


    with analytics_col2:

        with st.container(border=True):

            st.markdown("### 🌱 Lifestyle Factors")

            lifestyle_data = pd.DataFrame({
                "Factor": [
                    "Sleep Hours",
                    "Assignments",
                    "Screen Time"
                ],
                "Value": [
                    sleep_hours,
                    assignments_completed,
                    screen_time
                ]
            })

            st.bar_chart(
                lifestyle_data,
                x="Factor",
                y="Value"
            )


    st.divider()

    st.markdown(
        '<div class="section-title">💡 Personalized Recommendations</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        "Actionable suggestions based on the student's current profile."
        "</div>",
        unsafe_allow_html=True
    )


    with st.container(border=True):

        for recommendation in recommendations:

            st.write(
                f"💡 {recommendation}"
            )


    st.divider()

    st.markdown(
        '<div class="section-title">🔮 What-If Simulator</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        "Explore how changes in student behaviour could affect predicted performance."
        "</div>",
        unsafe_allow_html=True
    )


    with st.container(border=True):

        whatif_col1, whatif_col2, whatif_col3 = st.columns(3)


        with whatif_col1:

            new_study_hours = st.slider(
                "Study Hours",
                1.0,
                10.0,
                min(10.0, study_hours + 1),
                0.5,
                key="whatif_study"
            )


        with whatif_col2:

            new_attendance = st.slider(
                "Attendance (%)",
                50.0,
                100.0,
                min(100.0, attendance + 5),
                1.0,
                key="whatif_attendance"
            )


        with whatif_col3:

            new_screen_time = st.slider(
                "Screen Time",
                0.0,
                12.0,
                max(0.0, screen_time - 1),
                0.5,
                key="whatif_screen"
            )


        current_score, new_score, improvement = what_if_analysis(
            study_hours,
            attendance,
            previous_score,
            sleep_hours,
            assignments_completed,
            quiz_average,
            screen_time,
            consistency_score,
            new_study_hours,
            new_attendance,
            new_screen_time
        )


        st.write("")


        whatif_result_col1, whatif_result_col2, whatif_result_col3 = st.columns(3)


        with whatif_result_col1:

            st.metric(
                "Current Score",
                f"{current_score:.2f}"
            )


        with whatif_result_col2:

            st.metric(
                "What-If Score",
                f"{new_score:.2f}"
            )


        with whatif_result_col3:

            st.metric(
                "Potential Change",
                f"{improvement:+.2f}"
            )


    st.divider()

    st.markdown(
        '<div class="section-title">📄 Student Report</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        "Generate a professional PDF containing the complete student analysis."
        "</div>",
        unsafe_allow_html=True
    )


    student_data = {
        "study_hours": study_hours,
        "attendance": attendance,
        "previous_score": previous_score,
        "sleep_hours": sleep_hours,
        "assignments_completed": assignments_completed,
        "quiz_average": quiz_average,
        "screen_time": screen_time
    }


    report_buffer = BytesIO()


    create_report(
        report_buffer,
        score,
        risk,
        performance_level,
        student_data,
        strengths,
        attention,
        summary,
        recommendations,
        explanations,
        best_model_name,
        best_model_r2
    )


    report_buffer.seek(0)


    with st.container(border=True):

        st.markdown("### 📑 EduPulse AI Student Report")

        st.write(
            "Your complete AI-generated student performance report is ready."
        )

        st.download_button(
            label="📄 Download Student Report",
            data=report_buffer.getvalue(),
            file_name="edupulse_student_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )


else:

    st.divider()

    with st.container(border=True):

        st.markdown("### 🚀 Ready to Analyze")

        st.write(
            "Enter the student's information above and click "
            "**Analyze Student** to generate the AI assessment."
        )


st.divider()

st.markdown(
    '<div class="section-title">🤖 Model Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    "Comparison of the machine learning models evaluated by EduPulse AI."
    "</div>",
    unsafe_allow_html=True
)


model_rows = []


for name, result in model_results.items():

    model_rows.append({
        "Model": name,
        "MAE": round(result["mae"], 2),
        "RMSE": round(result["rmse"], 2),
        "R² Score": round(result["r2"], 3)
    })


model_table = pd.DataFrame(model_rows)


with st.container(border=True):

    st.dataframe(
        model_table,
        use_container_width=True,
        hide_index=True
    )


best_model_name = max(
    model_results,
    key=lambda name: model_results[name]["r2"]
)


best_model_r2 = model_results[best_model_name]["r2"]


model_col1, model_col2 = st.columns(2)


with model_col1:

    st.metric(
        "🏆 Best Model",
        best_model_name
    )


with model_col2:

    st.metric(
        "R² Score",
        f"{best_model_r2:.3f}"
    )


model_chart_data = pd.DataFrame({
    "Model": list(model_results.keys()),
    "R² Score": [
        result["r2"]
        for result in model_results.values()
    ]
})


st.bar_chart(
    model_chart_data,
    x="Model",
    y="R² Score"
)


st.caption(
    "EduPulse AI was evaluated using a synthetic dataset. "
    "Real-world student data would be required for real-world validation."
)
st.divider()

st.markdown("## 🚨 At-Risk Student Detection")

risk_data = analyze_all_students()

total_students = len(risk_data)
high_risk = len(risk_data[risk_data["Risk Level"] == "High Risk"])
medium_risk = len(risk_data[risk_data["Risk Level"] == "Medium Risk"])
low_risk = len(risk_data[risk_data["Risk Level"] == "Low Risk"])

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Students", total_students)
col2.metric("🔴 High Risk", high_risk)
col3.metric("🟠 Medium Risk", medium_risk)
col4.metric("🟢 Low Risk", low_risk)

st.markdown("### Students Requiring Attention")

at_risk = risk_data[
    risk_data["Risk Level"] != "Low Risk"
].sort_values(
    ["Risk Level", "Predicted Score"],
    ascending=[True, True]
)
st.dataframe(
    at_risk[
        [
            "Student ID",
            "Predicted Score",
            "Risk Level",
            "attendance",
            "study_hours",
            "quiz_average",
            "screen_time"
        ]
    ],
    use_container_width=True,
    hide_index=True
)
st.markdown("### 🔎 Top Risk Factors")

risk_factors = []

if (risk_data["attendance"] < 75).sum() > 0:
    risk_factors.append("Low Attendance")

if (risk_data["study_hours"] < 4).sum() > 0:
    risk_factors.append("Low Study Hours")

if (risk_data["quiz_average"] < 60).sum() > 0:
    risk_factors.append("Low Quiz Performance")

if (risk_data["screen_time"] > 6).sum() > 0:
    risk_factors.append("High Screen Time")

if (risk_data["sleep_hours"] < 6).sum() > 0:
    risk_factors.append("Low Sleep")

for factor in risk_factors:
    st.write(f"⚠️ {factor}")
    st.markdown("### 📊 Risk Distribution")
    st.markdown("### 🚨 Priority Students")

priority_students = risk_data[
    risk_data["Risk Level"] != "Low Risk"
].sort_values("Predicted Score").head(10)

st.dataframe(
    priority_students[
        [
            "Student ID",
            "Predicted Score",
            "Risk Level",
            "attendance",
            "study_hours",
            "quiz_average"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

risk_chart = pd.DataFrame({
    "Risk Level": ["High Risk", "Medium Risk", "Low Risk"],
    "Students": [high_risk, medium_risk, low_risk]
})

st.bar_chart(
    risk_chart,
    x="Risk Level",
    y="Students"
)