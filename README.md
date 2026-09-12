# EduPulse AI

## Student Success & Risk Intelligence System

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-orange)
![License](https://img.shields.io/badge/License-MIT-green)

EduPulse AI is a machine learning-based system that predicts student academic performance, identifies risk levels, explains prediction factors, and provides personalized recommendations.

## Features

- Student performance prediction
- Low, Medium, and High Risk detection
- Explainable AI insights
- Personalized recommendations
- What-If performance simulator
- At-Risk student detection
- Priority student identification
- Risk distribution analysis
- PDF student reports
- Machine learning model comparison

## Screenshots
### Student Profile

![Student Profile](screenshots/dashboard.png)

### Prediction Results

![Prediction Results](screenshots/results.png)
## Demo

EduPulse AI allows users to:

1. Enter student academic and lifestyle information
2. Predict final academic performance
3. Identify student risk level
4. Understand the factors influencing the prediction
5. Generate personalized recommendations
6. Simulate performance improvements using the What-If Simulator
7. Detect and prioritize at-risk students
8. Generate student performance reports

## Workflow

Student Data → ML Prediction → Risk Detection → Explainable AI → Recommendations → What-If Analysis → Student Report

## Machine Learning Models

- Linear Regression
- Decision Tree
- Random Forest
- Gradient Boosting

The best-performing model on the synthetic test dataset is Linear Regression with an R² score of 0.882.

## Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- Joblib
- ReportLab
- Matplotlib

## Project Structure

```text
EduPulse-AI/
├── data/
├── models/
├── src/
├── screenshots/
├── app.py
├── train_model.py
├── generate_report.py
└── README.md