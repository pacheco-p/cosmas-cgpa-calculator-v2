import streamlit as st
import auth

st.set_page_config(
    page_title="Cosmas CGPA Calculator",
    page_icon="🎓",
    layout="wide"
)

# Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# -----------------------------
# LOGIN / SIGNUP PAGE
# -----------------------------
if not st.session_state.logged_in:

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        try:
            st.image("cosmas_banner.png", use_container_width=True)
        except:
            st.title("🏛 COSMAS AT SUG TOP SEAT")

        st.title("🎓 Cosmas CGPA Calculator")

        tab1, tab2 = st.tabs(["Login", "Create Account"])

        # LOGIN
        with tab1:

            st.subheader("Login")

            username = st.text_input(
                "Username",
                key="login_username"
            )

            password = st.text_input(
                "Password",
                type="password",
                key="login_password"
            )

            if st.button("Login"):

                if auth.login(username, password):

                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()

                else:

                    st.error("Invalid username or password.")

        # REGISTER
        with tab2:

            st.subheader("Create Account")

            username = st.text_input(
                "Username",
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

            if st.button("Create Account"):

                if password != confirm:

                    st.error("Passwords do not match.")

                elif len(password) < 6:

                    st.warning("Password must be at least 6 characters.")

                elif auth.register(username, email, password):

                    st.success(
                        "Account created successfully! Please login."
                    )

                else:

                    st.error(
                        "Username or Email already exists."
                    )

# -----------------------------
# HOME PAGE
# -----------------------------
else:

    st.sidebar.image("cosmas_banner.png", use_container_width=True)

    st.sidebar.success(
        f"Welcome, {st.session_state.username}"
    )

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "CGPA Calculator",
            "History",
            "Profile",
            "Settings"
        ]
    )

    if st.sidebar.button("🚪 Logout"):

        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    if page == "Dashboard":
        st.title("🏛 Dashboard")
        st.info("Dashboard coming in the next step.")

    elif page == "CGPA Calculator":
        st.title("🎓 CGPA Calculator")
        st.info("Calculator coming in the next step.")

    elif page == "History":
        st.title("📊 History")
        st.info("History coming in the next step.")

    elif page == "Profile":
        st.title("👤 Profile")
        st.info("Profile coming in the next step.")

    elif page == "Settings":
        st.title("⚙ Settings")
        st.info("Settings coming in the next step.")