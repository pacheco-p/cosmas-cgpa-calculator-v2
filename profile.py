import streamlit as st
import pandas as pd
import database


def show():

    st.title("👤 My Profile")

    st.subheader("Account Information")

    user = database.get_user(st.session_state.username)

    if user:
        st.write(f"**Username:** {user[1]}")
        st.write(f"**Email:** {user[2]}")

    st.divider()

    # -----------------------------
    # Statistics
    # -----------------------------
    stats = database.get_statistics(st.session_state.username)

    total_saved = stats[0] if stats[0] else 0
    highest = stats[1] if stats[1] else 0.00
    average = stats[2] if stats[2] else 0.00

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Saved Results",
        total_saved
    )

    col2.metric(
        "Highest CGPA",
        f"{highest:.2f}"
    )

    col3.metric(
        "Average CGPA",
        f"{average:.2f}"
    )

    st.divider()

    # -----------------------------
    # Recent Results
    # -----------------------------
    st.subheader("📋 Recent Calculations")

    history = database.get_history(
        st.session_state.username
    )

    if history:

        df = pd.DataFrame(
            history,
            columns=[
                "ID",
                "Semester GPA",
                "CGPA",
                "Credit Units",
                "Quality Points",
                "Date"
            ]
        )

        st.dataframe(
            df.drop(columns=["ID"]).head(5),
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.subheader("📈 CGPA Progress")

        chart = df.iloc[::-1][["CGPA"]]

        st.line_chart(chart)

    else:

        st.info("No saved calculations yet.")

    st.divider()

    # -----------------------------
    # Logout
    # -----------------------------
    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()