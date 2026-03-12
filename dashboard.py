import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import random
import time


# ---------------- STATUS COLORS ----------------
def color_status(val):
    colors = {
        "Low": "color:#00FF9C;font-weight:700;",
        "Medium": "color:#FFD166;font-weight:700;",
        "Critical": "color:#FF4C4C;font-weight:700;",
        "Blocked": "color:#FF4C4C;font-weight:700;",
        "Warned": "color:#FFD166;font-weight:700;",
        "Notified": "color:#00FF9C;font-weight:700;",
        "Generated": "color:#A4FFCE;font-weight:700;",
        "Pending": "color:#E8FFF4;font-weight:700;"
    }
    return colors.get(val, "")


# ---------------- THREAT LEVEL ----------------
def threat_level_from_download(mb):
    if mb >= 600:
        return "Critical"
    elif mb >= 450:
        return "Medium"
    return "Low"


# ---------------- INCIDENT STATE ----------------
def initialize_actions(threats_df):
    if "incident_actions" not in st.session_state:
        st.session_state.incident_actions = {}

    for _, row in threats_df.iterrows():
        emp_id = str(row["employee_id"])

        if emp_id not in st.session_state.incident_actions:
            st.session_state.incident_actions[emp_id] = {
                "Admin Alert": "Pending",
                "Employee Notice": "Pending",
                "Access Control": "Pending",
                "Ticket ID": "Pending"
            }


# ---------------- DASHBOARD ----------------
def show_dashboard():
    df = st.session_state.get("analysis")

    if df is None:
        st.warning("Upload log file first from the Upload Logs page.")
        return

    total = len(df)
    threats = len(df[df["Anomaly"] == "Threat"])
    safe = total - threats
    after_hours = int(df["after_hours"].sum()) if "after_hours" in df.columns else 0

    threats_df = df[df["Anomaly"] == "Threat"].copy()
    initialize_actions(threats_df)

    # ---------------- ALERT BANNER ----------------
    if threats > 0:
        st.markdown(
            f"""
            <div style="
            background:#FF4C4C;
            padding:12px;
            border-radius:10px;
            color:white;
            font-weight:700;
            text-align:center;
            animation:blink 1.5s infinite;">
            ⚠ CRITICAL THREAT DETECTED ({threats})
            </div>

            <style>
            @keyframes blink {{
            0% {{opacity:1;}}
            50% {{opacity:0.4;}}
            100% {{opacity:1;}}
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

    # ---------------- HEADER ----------------
    st.markdown(
        f"<h1>Hello {st.session_state.get('user','User').title()}</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='color:#A4FFCE;'>Cybersecurity monitoring overview</p>",
        unsafe_allow_html=True
    )

    # ---------------- TOP ACTIONS ----------------
    col1, col2 = st.columns([4, 1])

    with col2:
        if st.button("🔔 Check Alerts", use_container_width=True):
            if threats > 0:
                st.error(f"{threats} suspicious activities detected")
            else:
                st.success("No threats detected")

    # ---------------- METRICS ----------------
    c0, c1, c2, c3 = st.columns([0.9, 1, 1, 1])

    with c0:
        st.markdown(
            """
            <div class="panel" style="display:flex;align-items:center;justify-content:center;height:100%">
            <div style="font-size:2rem;">🛡</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c1:
        st.metric("Total Alerts", total)

    with c2:
        st.metric("Critical Incidents", threats)

    with c3:
        st.metric("Analysts Online", safe)

    # ---------------- ROW 1 ----------------
    r1c1, r1c2, r1c3 = st.columns([1.1, 1.1, 1.2])

    with r1c1:
        st.markdown('<div class="section-title">Firewall Activity</div>', unsafe_allow_html=True)

        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=after_hours,
            gauge={
                "axis": {"range": [0, max(after_hours + 10, 50)]},
                "bar": {"color": "#C8FF63"}
            }
        ))

        gauge.update_layout(
            paper_bgcolor="#121816",
            font_color="#E8FFF4",
            height=260
        )

        st.plotly_chart(gauge, use_container_width=True)

    with r1c2:
        st.markdown('<div class="section-title">Alert Volume</div>', unsafe_allow_html=True)

        plot_df = df.copy()
        plot_df["time_index"] = range(len(plot_df))

        bar = px.bar(
            plot_df,
            x="time_index",
            y="download_mb",
            color="Anomaly",
            color_discrete_map={"Threat": "#FF4C4C", "Normal": "#C8FF63"}
        )

        bar.update_layout(
            paper_bgcolor="#121816",
            plot_bgcolor="#121816",
            font_color="#E8FFF4",
            legend_title_text="",
            xaxis_title="",
            yaxis_title=""
        )

        st.plotly_chart(bar, use_container_width=True)

    with r1c3:
        st.markdown('<div class="section-title">Breakdown</div>', unsafe_allow_html=True)

        line = px.line(
            plot_df,
            x="time_index",
            y="download_mb",
            color="Anomaly",
            color_discrete_map={"Threat": "#FFD166", "Normal": "#C8FF63"}
        )

        line.update_layout(
            paper_bgcolor="#121816",
            plot_bgcolor="#121816",
            font_color="#E8FFF4",
            legend_title_text="",
            xaxis_title="",
            yaxis_title=""
        )

        st.plotly_chart(line, use_container_width=True)

    # ---------------- ALERT QUEUE ----------------
    st.markdown('<div class="section-title">Alert Queue</div>', unsafe_allow_html=True)

    if len(threats_df) > 0:
        queue_df = threats_df[["employee_id", "login_hour", "download_mb"]].copy()
        queue_df["Status"] = queue_df["download_mb"].apply(threat_level_from_download)
        queue_df.columns = ["Employee ID", "Login Hour", "Download MB", "Status"]

        styled = queue_df.style.map(color_status, subset=["Status"])
        st.dataframe(styled, use_container_width=True, height=280)
    else:
        st.success("No active threats detected")

    # ---------------- LIVE SOC CONSOLE ----------------
    st.markdown('<div class="section-title">Threat Monitoring Console</div>', unsafe_allow_html=True)

    logs = [
        "> Connecting to network nodes...",
        "> Monitoring login behaviours...",
        "> Detecting abnormal downloads...",
        "> Running AI anomaly detection..."
    ]

    for log in logs:
        st.code(log)

    if threats > 0:
        for _, row in threats_df.head(5).iterrows():
            st.code(
                f"> ALERT: Employee {row['employee_id']} | "
                f"Login Hour: {row['login_hour']} | "
                f"Download: {row['download_mb']} MB"
            )
    else:
        st.code("> System secure")

    # ---------------- CYBER NETWORK + MAP ----------------
    n1, n2 = st.columns(2)

    with n1:
        st.markdown('<div class="section-title">Cyber Network</div>', unsafe_allow_html=True)

        n = len(df)
        x = np.random.rand(n)
        y = np.random.rand(n)
        z = np.random.rand(n)

        colors = ["#FF4C4C" if a == "Threat" else "#C8FF63" for a in df["Anomaly"]]

        fig3d = go.Figure(data=[go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode="markers",
            marker=dict(size=6, color=colors),
            text=df["employee_id"]
        )])

        fig3d.update_layout(
            height=350,
            paper_bgcolor="#121816",
            font_color="#E8FFF4"
        )

        st.plotly_chart(fig3d, use_container_width=True)

    with n2:
        st.markdown('<div class="section-title">Global Cyber Attack Map</div>', unsafe_allow_html=True)

        attack_df = pd.DataFrame({
            "lat": np.random.uniform(-60, 60, 40),
            "lon": np.random.uniform(-180, 180, 40)
        })

        st.map(attack_df)

    # ---------------- TOP SUSPICIOUS EMPLOYEES ----------------
    st.markdown('<div class="section-title">Top Suspicious Employees</div>', unsafe_allow_html=True)

    if len(threats_df) > 0:
        leaderboard = (
            threats_df.groupby("employee_id")
            .size()
            .reset_index(name="Threat Count")
            .sort_values("Threat Count", ascending=False)
        )
        st.dataframe(leaderboard, use_container_width=True, height=220)
    else:
        st.info("No suspicious employees found")

    # ---------------- ACTION CENTER ----------------
    st.markdown('<div class="section-title">Action Center</div>', unsafe_allow_html=True)

    if len(threats_df) > 0:
        for _, row in threats_df.head(5).iterrows():
            emp_id = str(row["employee_id"])
            lvl = threat_level_from_download(row["download_mb"])
            action = st.session_state.incident_actions[emp_id]

            st.markdown(
                f"""
                <div class="panel">
                <b>Employee {emp_id}</b><br>
                Threat Level: <b>{lvl}</b><br>
                Login Hour: <b>{row['login_hour']}</b><br>
                Download: <b>{row['download_mb']} MB</b><br><br>
                Admin Alert: <b>{action['Admin Alert']}</b> |
                Employee Notice: <b>{action['Employee Notice']}</b> |
                Access Control: <b>{action['Access Control']}</b> |
                Ticket ID: <b>{action['Ticket ID']}</b>
                </div>
                """,
                unsafe_allow_html=True
            )

            b1, b2, b3, b4 = st.columns(4)

            with b1:
                if st.button(f"Notify {emp_id}", key=f"notify_{emp_id}"):
                    action["Admin Alert"] = "Notified"
                    st.success("Admin notified")

            with b2:
                if st.button(f"Warn {emp_id}", key=f"warn_{emp_id}"):
                    action["Employee Notice"] = "Warned"
                    st.warning("Warning sent")

            with b3:
                if st.button(f"Block {emp_id}", key=f"block_{emp_id}"):
                    action["Access Control"] = "Blocked"
                    st.error("Access blocked")

            with b4:
                if st.button(f"Ticket {emp_id}", key=f"ticket_{emp_id}"):
                    ticket = f"INC-{random.randint(1000,9999)}"
                    action["Ticket ID"] = ticket
                    st.info(f"Ticket {ticket} created")

        # Incident summary
        st.markdown('<div class="section-title">Incident Response Summary</div>', unsafe_allow_html=True)

        summary_rows = []
        for _, row in threats_df.head(5).iterrows():
            emp_id = str(row["employee_id"])
            action = st.session_state.incident_actions[emp_id]

            summary_rows.append({
                "Employee ID": emp_id,
                "Threat Level": threat_level_from_download(row["download_mb"]),
                "Admin Alert": action["Admin Alert"],
                "Employee Notice": action["Employee Notice"],
                "Access Control": action["Access Control"],
                "Ticket ID": action["Ticket ID"]
            })

        summary_df = pd.DataFrame(summary_rows)
        styled_summary = summary_df.style.map(
            color_status,
            subset=["Threat Level", "Admin Alert", "Employee Notice", "Access Control"]
        )

        st.dataframe(styled_summary, use_container_width=True, height=260)

    else:
        st.success("No incident response actions required.")

    # ---------------- EXPORT REPORT ----------------
    st.markdown('<div class="section-title">Export Threat Report</div>', unsafe_allow_html=True)

    st.download_button(
        "Download Threat Report",
        threats_df.to_csv(index=False),
        file_name="threat_report.csv",
        mime="text/csv"
    )

    # ---------------- MANUAL REFRESH ----------------
    if st.button("🔄 Refresh Dashboard", use_container_width=True):
        st.rerun()