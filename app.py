import streamlit as st
from dashboard import show_dashboard
from upload_logs import upload_page
from live_monitoring import show_live_monitoring

st.set_page_config(
    page_title="AI Insider Threat Detection",
    layout="wide",
    page_icon="🔐"
)

with open("style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Session state
if "auth" not in st.session_state:
    st.session_state.auth = False

if "role" not in st.session_state:
    st.session_state.role = None

if "user" not in st.session_state:
    st.session_state.user = None

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "page" not in st.session_state:
    st.session_state.page = "Home"

# Users
users = {
    "admin": {"password": "admin123", "role": "Admin"},
    "developer": {"password": "dev123", "role": "Developer"},
    "analyst": {"password": "analyst123", "role": "Analyst"}
}


def login():
    # Background image only for login page
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("image copy.png");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }

        .stApp::before {
            content: "";
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.65);
            z-index: 0;
        }

        .main .block-container {
            position: relative;
            z-index: 1;
        }

        .login-card {
            background: rgba(18, 24, 22, 0.88);
            backdrop-filter: blur(6px);
            -webkit-backdrop-filter: blur(6px);
            padding: 28px;
            border-radius: 16px;
            border: 1px solid rgba(164,255,206,0.15);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<h1 style='text-align:left;'>Hello User</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#A4FFCE;'>AI-Based Insider Threat Detection System</p>",
        unsafe_allow_html=True
    )

    _, center, _ = st.columns([1, 1.3, 1])

    with center:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.text_input("Username", key="login_username")
        st.text_input("Password", type="password", key="login_password")

        if st.button("Login", use_container_width=True):
            username = st.session_state.login_username
            password = st.session_state.login_password

            if username in users and users[username]["password"] == password:
                st.session_state.auth = True
                st.session_state.role = users[username]["role"]
                st.session_state.user = username
                st.session_state.page = "Home"
                st.rerun()
            else:
                st.error("Invalid credentials")

        st.markdown("</div>", unsafe_allow_html=True)



# ADD THIS BLOCK HERE
st.markdown(
    """
    <style>
    header[data-testid="stHeader"] {
        display: none;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    .block-container {
        padding-top: 0rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Session state

if st.session_state.auth:
    st.sidebar.markdown("## Dashboard")
    st.sidebar.markdown("---")
    st.sidebar.write(f"👤 **{st.session_state.user}**")
    st.sidebar.write(f"🛡 **{st.session_state.role}**")
    st.sidebar.markdown("---")

    if st.session_state.role in ["Admin", "Developer"]:
        pages = ["Home", "Upload Logs", "Threat Dashboard", "Live Monitoring"]
    else:
        pages = ["Home", "Threat Dashboard", "Live Monitoring"]

    if st.session_state.page not in pages:
        st.session_state.page = pages[0]

    selected_page = st.sidebar.radio(
        "Navigation",
        pages,
        index=pages.index(st.session_state.page)
    )
    st.session_state.page = selected_page

    if selected_page == "Home":
        st.markdown("<h1 style='margin-bottom:0.2rem;'>Hello {}</h1>".format(
            st.session_state.user.title()
        ), unsafe_allow_html=True)
        st.markdown(
            "<p style='color:#A4FFCE; margin-top:0; margin-bottom:1.5rem;'>Cybersecurity monitoring overview</p>",
            unsafe_allow_html=True
        )

        top_left, top_right = st.columns([4, 1])
        with top_right:
            if st.button("Check Alerts", use_container_width=True):
                st.session_state.page = "Threat Dashboard"
                st.rerun()

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Alerts (Today)", 4372)
        c2.metric("Critical Incident", 3568)
        c3.metric("Analysts Online", 5120)

        st.markdown(
            f"""
            <div class="panel">
                <h3>Welcome {st.session_state.user.title()}</h3>
                <p>This dashboard helps monitor insider threat activity, alert volume, suspicious users, and AI detection results.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    elif selected_page == "Upload Logs":
        upload_page()

    elif selected_page == "Threat Dashboard":
        show_dashboard()

    elif selected_page == "Live Monitoring":
        show_live_monitoring()

    st.sidebar.markdown("---")
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.auth = False
        st.session_state.role = None
        st.session_state.user = None
        st.session_state.analysis = None
        st.session_state.page = "Home"
        st.rerun()

else:
    login()