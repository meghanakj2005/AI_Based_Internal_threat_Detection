import streamlit as st
import pandas as pd
import plotly.express as px
import random
import time
import os
import sys
from datetime import datetime

# Try importing your advanced model pipeline if it exists
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

MODEL_AVAILABLE = True
try:
    from model.role_anomaly import detect_role_violation
    from model.ml_anomaly import detect_ml_anomaly
    from model.behavior_profile import employee_behavior_profile
    from model.exfiltration import detect_exfiltration
    from risk.risk_engine import calculate_risk
except Exception:
    MODEL_AVAILABLE = False


roles = ["developer", "manager", "analyst", "tester", "hr", "admin"]
files = ["dev_code", "manager_report", "analytics_data", "test_cases"]
locations = ["office", "remote", "vpn"]


def fetch_live_log():
    log = {
        "employee": random.randint(1000, 2000),
        "role": random.choice(roles),
        "files_accessed_name": random.choice(files),
        "login_attempts": random.randint(1, 5),
        "failed_logins": random.randint(0, 3),
        "pages_accessed": random.randint(10, 120),
        "session_duration": random.randint(5, 60),
        "usb_usage": random.randint(0, 1),
        "download_mb": random.randint(1, 200),
        "location": random.choice(locations),
        "time": datetime.now().strftime("%H:%M:%S")
    }
    return log


def fallback_process_log(log: dict) -> dict:
    risk_score = 0

    if log["failed_logins"] >= 2:
        risk_score += 20
    if log["pages_accessed"] >= 80:
        risk_score += 15
    if log["usb_usage"] == 1:
        risk_score += 15
    if log["download_mb"] >= 150:
        risk_score += 35
    elif log["download_mb"] >= 100:
        risk_score += 20
    if log["session_duration"] >= 45:
        risk_score += 10

    role_violation = 0
    if log["role"] == "hr" and log["files_accessed_name"] == "dev_code":
        role_violation = 1
        risk_score += 15
    if log["role"] == "tester" and log["files_accessed_name"] == "manager_report":
        role_violation = 1
        risk_score += 15

    risk_score = min(risk_score, 100)
    status = "🚨 Threat Detected" if risk_score > 70 else "✅ Normal"

    result = {
        "time": log["time"],
        "employee": log["employee"],
        "role": log["role"],
        "download_mb": log["download_mb"],
        "files_accessed_name": log["files_accessed_name"],
        "failed_logins": log["failed_logins"],
        "usb_usage": log["usb_usage"],
        "pages_accessed": log["pages_accessed"],
        "session_duration": log["session_duration"],
        "location": log["location"],
        "role_violation": role_violation,
        "risk_score": risk_score,
        "status": status,
    }
    return result


def model_process_log(log: dict) -> dict:
    df = pd.DataFrame([log])

    # If your custom pipeline exists, use it
    df = detect_role_violation(df)
    df = detect_ml_anomaly(df)
    df = employee_behavior_profile(df)
    df = detect_exfiltration(df)
    df = calculate_risk(df)

    df["status"] = df["risk_score"].apply(
        lambda x: "🚨 Threat Detected" if x > 70 else "✅ Normal"
    )

    return df.to_dict(orient="records")[0]


def process_log(log: dict) -> dict:
    if MODEL_AVAILABLE:
        try:
            return model_process_log(log)
        except Exception:
            return fallback_process_log(log)
    return fallback_process_log(log)


def init_live_state():
    if "live_logs" not in st.session_state:
        st.session_state.live_logs = []

    if "live_running" not in st.session_state:
        st.session_state.live_running = False


def add_new_live_log():
    log = fetch_live_log()
    processed = process_log(log)
    st.session_state.live_logs.insert(0, processed)

    if len(st.session_state.live_logs) > 20:
        st.session_state.live_logs = st.session_state.live_logs[:20]


def show_live_monitoring():
    init_live_state()

    st.markdown("<h1>Live Monitoring</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#A4FFCE;'>Real-time employee activity stream with live risk scoring</p>",
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns([1, 1, 1])

    with c1:
        if st.button("▶ Start Live Monitoring", use_container_width=True):
            st.session_state.live_running = True
            st.rerun()

    with c2:
        if st.button("⏹ Stop Live Monitoring", use_container_width=True):
            st.session_state.live_running = False
            st.rerun()

    with c3:
        if st.button("🗑 Clear Logs", use_container_width=True):
            st.session_state.live_logs = []
            st.rerun()

    if st.session_state.live_running:
        add_new_live_log()

    logs = st.session_state.live_logs
    logs_df = pd.DataFrame(logs) if logs else pd.DataFrame()

    total_logs = len(logs_df)
    threat_count = len(logs_df[logs_df["status"].astype(str).str.contains("Threat", na=False)]) if not logs_df.empty else 0
    normal_count = total_logs - threat_count
    avg_risk = round(logs_df["risk_score"].mean(), 2) if not logs_df.empty else 0

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Live Events", total_logs)
    m2.metric("Threats", threat_count)
    m3.metric("Normal", normal_count)
    m4.metric("Average Risk", avg_risk)

    if not logs_df.empty:
        st.markdown('<div class="section-title">Live Activity</div>', unsafe_allow_html=True)

        display_cols = [
            col for col in ["time", "employee", "role", "risk_score", "status"]
            if col in logs_df.columns
        ]
        st.dataframe(logs_df[display_cols], use_container_width=True, height=360)

        ch1, ch2 = st.columns(2)

        with ch1:
            st.markdown('<div class="section-title">Risk Bar Chart</div>', unsafe_allow_html=True)
            bar_df = logs_df.head(10).copy()
            bar_df["employee"] = bar_df["employee"].astype(str)

            bar = px.bar(
                bar_df.iloc[::-1],
                x="employee",
                y="risk_score",
                color="status",
                color_discrete_map={
                    "🚨 Threat Detected": "#FF4C4C",
                    "✅ Normal": "#C8FF63"
                }
            )
            bar.update_layout(
                paper_bgcolor="#121816",
                plot_bgcolor="#121816",
                font_color="#E8FFF4",
                legend_title_text="Status",
                xaxis_title="Employee",
                yaxis_title="Risk Score"
            )
            st.plotly_chart(bar, use_container_width=True)

        with ch2:
            st.markdown('<div class="section-title">Threat Distribution</div>', unsafe_allow_html=True)

            pie = px.pie(
                names=["Normal", "Threat"],
                values=[normal_count, threat_count],
                color=["Normal", "Threat"],
                color_discrete_map={
                    "Normal": "#C8FF63",
                    "Threat": "#FF4C4C"
                },
                hole=0.55
            )
            pie.update_layout(
                paper_bgcolor="#121816",
                plot_bgcolor="#121816",
                font_color="#E8FFF4"
            )
            st.plotly_chart(pie, use_container_width=True)

        st.markdown('<div class="section-title">Live Monitoring Console</div>', unsafe_allow_html=True)

        latest = logs_df.iloc[0]
        st.code(f"> New Event @ {latest.get('time', '-')}")
        st.code(f"> Employee {latest.get('employee', '-')}")
        st.code(f"> Role: {latest.get('role', '-')}")
        st.code(f"> Risk Score: {latest.get('risk_score', '-')}")
        st.code(f"> Status: {latest.get('status', '-')}")
    else:
        st.info("Start live monitoring to generate real-time activity logs.")

    # Auto-loop without external packages
    if st.session_state.live_running:
        time.sleep(2)
        st.rerun()