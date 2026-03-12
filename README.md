# AI Insider Threat Detection System

## Project Overview

The AI-Based Insider Threat Detection System is a cybersecurity solution that uses Machine Learning to detect suspicious employee behavior inside an organization.

Unlike traditional rule-based systems, this project uses anomaly detection techniques to automatically identify unusual activities such as:

- Login during unusual hours
- Excessive file access
- Large data downloads
- USB misuse
- Foreign IP logins

The system helps organizations reduce internal security risks using intelligent behavioral analysis.

---

## Problem Statement

Insider threats are one of the major causes of data breaches in organizations. Traditional security systems mainly focus on external attacks and use fixed rule-based monitoring, which often fails to detect unknown or evolving threats.

This project aims to build an AI-driven system that learns normal employee behavior and detects abnormal patterns automatically.

---

## Machine Learning Models Used

- **Isolation Forest** → For anomaly detection
- **Random Forest Classifier** → For threat classification

---

## Project Structure

```
AI_Insider_Threat_Detection/
│
├── data/
│ ├── employee_logs.csv
│
├── models/
│ ├── anomaly_model.pkl
│ ├── classifier_model.pkl
│
├── src/
│ ├── data_preprocessing.py
│ ├── feature_engineering.py
│ ├── train_model.py
│ ├── detect_anomaly.py
│ ├── alert_system.py
│
├── app/
│ ├── app.py
│
├── requirements.txt
├── README.md

```
---
## Features
- Behavioral anomaly detection
- Threat classification
- Risk flag generation
- Streamlit dashboard

---

## ⚙️ Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- Pickle

---
## How to Run

1. Install dependencies
   ```
   pip install -r requirements.txt
   
   ```

3. Train model
   ```
   cd src
   python train_model.py

   ```

4. Run dashboard
   ```
   cd ../app
   streamlit run app.pyv
   ```
   ---
