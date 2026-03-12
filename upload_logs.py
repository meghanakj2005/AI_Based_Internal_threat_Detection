import streamlit as st
import pandas as pd
import sys
import os

# Add src folder to Python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "src"))
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

from detect_anomaly import detect


def upload_page():
    st.title("📡 Upload Security Logs")

    # Optional role restriction
    role = st.session_state.get("role")
    if role == "Analyst":
        st.warning("Analyst role does not have permission to upload logs.")
        return

    st.markdown(
        """
        <div class="panel">
            <h3>Upload Employee Activity Logs</h3>
            <p>Upload a CSV file to run AI-based insider threat detection.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    file = st.file_uploader("Upload CSV Log File", type=["csv"])

    if file is not None:
        try:
            df = pd.read_csv(file)

            st.session_state.uploaded_filename = file.name

            st.success(f"Log file uploaded successfully: {file.name}")

            st.subheader("📄 Uploaded Log Preview")
            st.dataframe(df, use_container_width=True)

            required_columns = [
                "employee_id",
                "login_hour",
                "download_mb",
                "files_accessed"
            ]

            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                st.error(
                    "Missing required columns: "
                    + ", ".join(missing_columns)
                )
                st.info(
                    "Required columns are: employee_id, login_hour, download_mb, files_accessed"
                )
                return

            st.subheader("✅ File Validation")
            st.write(f"Rows: **{len(df)}**")
            st.write(f"Columns: **{len(df.columns)}**")

            if st.button("Run AI Threat Detection", use_container_width=True):
                with st.spinner("Running AI threat detection model..."):
                    result = detect(df)

                st.session_state.analysis = result

                st.success("Analysis completed successfully.")
                st.info("Now open the Threat Dashboard from the sidebar.")

        except Exception as e:
            st.error(f"Error reading or processing file: {e}")