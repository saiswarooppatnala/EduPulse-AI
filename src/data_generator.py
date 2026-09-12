import pandas as pd
import numpy as np

np.random.seed(42)

students = 500

study_hours = np.random.uniform(1, 10, students)
attendance = np.random.uniform(50, 100, students)
previous_score = np.random.uniform(30, 100, students)
sleep_hours = np.random.uniform(3, 10, students)
assignments_completed = np.random.randint(0, 11, students)
quiz_average = np.random.uniform(30, 100, students)
screen_time = np.random.uniform(1, 12, students)

# Independent consistency measure
consistency_score = np.random.uniform(30, 100, students)

final_score = (
    study_hours * 3
    + attendance * 0.25
    + previous_score * 0.30
    + sleep_hours * 1.5
    + assignments_completed * 1.5
    + quiz_average * 0.20
    - screen_time * 0.8
    + consistency_score * 0.20
)

# Keep scores between 0 and 100
final_score = np.clip(final_score, 0, 100)

data = pd.DataFrame({
    "study_hours": study_hours,
    "attendance": attendance,
    "previous_score": previous_score,
    "sleep_hours": sleep_hours,
    "assignments_completed": assignments_completed,
    "quiz_average": quiz_average,
    "screen_time": screen_time,
    "consistency_score": consistency_score,
    "final_score": final_score
})

data.to_csv(
    "data/student_data.csv",
    index=False
)

print("Student dataset generated successfully.")
print(f"Number of students: {len(data)}")