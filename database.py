import streamlit as st
import auth
import dashboard
import calculator
import history
import profile

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
# LOGIN / SIGNUP
# -----------------------------
if not st.session_state.logged_in:

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        try:
            st.image("cosmas_banner.png", use_container_width=True)
        except:
            st.title("🏛️ COSMAS AT SUG TOP SEAT")

        st.title("🎓 Cosmas CGPA Calculator")
        st.caption("Support • Pray • Canvass")

        login_tab, signup_tab = st.tabs(
            ["🔑 Login", "📝 Create Account"]
        )

        # LOGIN
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

            if st.button(
                "Login",
                use_container_width=True
            ):

                if auth.login(
                    username,
                    password
                ):

                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()

                else:
                    st.error("Invalid username or password.")

        # SIGNUP
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

            if st.button(
                "Create Account",
                use_container_width=True
            ):

                if password != confirm:
                    st.error("Passwords do not match.")

                elif len(password) < 6:
                    st.warning("Password must contain at least 6 characters.")

                elif auth.register(
                    username,
                    email,
                    password
                ):
                    st.success(
                        "Account created successfully! Please login."
                    )

                else:
                    st.error(
                        "Username or Email already exists."
                    )

# -----------------------------
# MAIN APP
# -----------------------------
else:

    try:
        st.sidebar.image(
            "cosmas_banner.png",
            use_container_width=True
        )
    except:
        pass

    st.sidebar.success(
        f"Welcome {st.session_state.username}"
    )

    page = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "🎓 CGPA Calculator",
            "📊 History",
            "👤 Profile"
        ]
    )

    st.sidebar.divider()

    if st.sidebar.button("🚪 Logout"):

        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    if page == "🏠 Dashboard":
        dashboard.show()

    elif page == "🎓 CGPA Calculator":
        calculator.show()

    elif page == "📊 History":
        history.show()

    elif page == "👤 Profile":
        profile.show()
