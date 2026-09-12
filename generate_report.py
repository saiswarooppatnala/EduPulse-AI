from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from datetime import datetime


def create_report(
    output,
    score,
    risk,
    performance_level,
    student_data,
    strengths,
    attention,
    summary,
    recommendations,
    explanations,
    best_model,
    r2
):
    document = SimpleDocTemplate(
        output,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=24,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=12,
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        "ReportHeading",
        parent=styles["Heading2"],
        fontSize=15,
        spaceBefore=15,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["Normal"],
        fontSize=10,
        leading=15
    )

    small_style = ParagraphStyle(
        "ReportSmall",
        parent=styles["Normal"],
        fontSize=8,
        leading=11
    )

    story = []

    story.append(
        Paragraph("EduPulse AI", title_style)
    )

    story.append(
        Paragraph(
            "Student Success & Risk Intelligence Report",
            subtitle_style
        )
    )

    story.append(
        Paragraph(
            datetime.now().strftime("Report generated on %d %B %Y"),
            small_style
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph("Student Performance Overview", heading_style)
    )

    result_data = [
        ["Predicted Final Score", f"{score}/100"],
        ["Risk Level", risk],
        ["Performance Level", performance_level],
        ["Best Model", best_model],
        ["Model R² Score", f"{r2:.3f}"]
    ]

    result_table = Table(result_data, colWidths=[220, 220])

    result_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
            ("PADDING", (0, 0), (-1, -1), 8)
        ])
    )

    story.append(result_table)

    story.append(
        Paragraph("Student Profile", heading_style)
    )

    profile_data = [
        ["Metric", "Value"],
        ["Study Hours", f"{student_data['study_hours']:.1f} hours"],
        ["Attendance", f"{student_data['attendance']:.1f}%"],
        ["Previous Score", f"{student_data['previous_score']:.1f}"],
        ["Sleep Hours", f"{student_data['sleep_hours']:.1f} hours"],
        ["Assignments Completed", str(student_data["assignments_completed"])],
        ["Quiz Average", f"{student_data['quiz_average']:.1f}"],
        ["Screen Time", f"{student_data['screen_time']:.1f} hours"]
    ]

    profile_table = Table(profile_data, colWidths=[220, 220])

    profile_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("PADDING", (0, 0), (-1, -1), 7)
        ])
    )

    story.append(profile_table)

    story.append(
        Paragraph("Student Strengths", heading_style)
    )

    for item in strengths:
        story.append(
            Paragraph(f"- {item}", body_style)
        )

    story.append(
        Paragraph("Areas to Improve", heading_style)
    )

    for item in attention:
        story.append(
            Paragraph(f"- {item}", body_style)
        )

    story.append(
        Paragraph("AI Performance Summary", heading_style)
    )

    story.append(
        Paragraph(summary, body_style)
    )

    story.append(
        Paragraph("Explainable AI Insights", heading_style)
    )

    for item in explanations[:5]:
        story.append(
            Paragraph(
                f"<b>{item['feature']}</b> — "
                f"{item['impact']} impact ({item['contribution']:+.2f}). "
                f"{item['explanation']}",
                body_style
            )
        )

    story.append(
        Paragraph("Personalized Recommendations", heading_style)
    )

    for item in recommendations:
        story.append(
            Paragraph(f"- {item}", body_style)
        )

    story.append(
        Paragraph("Model Information", heading_style)
    )

    story.append(
        Paragraph(
            f"EduPulse AI evaluated multiple machine learning models "
            f"and selected {best_model} based on the highest test-set "
            f"R² score of {r2:.3f}.",
            body_style
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "Note: This system was evaluated using a synthetic dataset. "
            "Real-world student data would be required for real-world validation.",
            small_style
        )
    )

    document.build(story)