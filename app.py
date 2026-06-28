import streamlit as st
import auth
import dashboard

st.set_page_config(
    page_title="Cosmas CGPA Calculator",
    page_icon="🎓",
    layout="wide"
)

# -----------------------------
# Session State
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# -----------------------------
# LOGIN / SIGNUP PAGE
# -----------------------------
if not st.session_state.logged_in:

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        try:
            st.image("cosmas_banner.png", use_container_width=True)
        except Exception:
            st.title("🏛️ COSMAS AT SUG TOP SEAT")

        st.title("🎓 Cosmas CGPA Calculator")
        st.caption("Support • Pray • Canvass")

        login_tab, signup_tab = st.tabs(["🔑 Login", "📝 Create Account"])

        # ---------------- LOGIN ---------------- #
        with login_tab:

            username = st.text_input(
                "Username",
                key="login_username"
            )

            password = st.text_input(
                "Password",
                type="password",
                key="login_password"
            )

            if st.button("Login", use_container_width=True):

                if auth.login(username, password):

                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()

                else:
                    st.error("Invalid username or password.")

        # ---------------- SIGNUP ---------------- #
        with signup_tab:

            username = st.text_input(
                "Choose Username",
                key="signup_username"
            )

            email = st.text_input(
                "Email Address"
            )

            password = st.text_input(
                "Password",
                type="password",
                key="signup_password"
            )

            confirm = st.text_input(
                "Confirm Password",
                type="password"
            )
