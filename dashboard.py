import streamlit as st
import pandas as pd
import database


def show():

    st.title("🏠 Dashboard")

    st.success(f"Welcome back, {st.session_state.username}! 👋")

    # -----------------------------
    # Statistics
    # -----------------------------
    stats = database.get_statistics(st.session_state.username)

    total_saved = stats[0] if stats[0] else 0
    highest = stats[1] if stats[1] else 0.00
    average = stats[2] if stats[2] else 0.00

    history = database.get_history(st.session_state.username)

    latest = history[0][2] if history else 0.00

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Saved Results",
        total_saved
    )

    c2.metric(
        "Latest CGPA",
        f"{latest:.2f}"
    )

    c3.metric(
        "Highest CGPA",
        f"{highest:.2f}"
    )

    c4.metric(
        "Average CGPA",
        f"{average:.2f}"
    )

    st.divider()

    # -----------------------------
    # Recent Activity
    # -----------------------------
    st.subheader("📋 Recent Calculations")

    if history:

        recent = pd.DataFrame(
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
            recent.head(5).drop(columns=["ID"]),
            use_container_width=True
        )

    else:

        st.info("No saved calculations yet.")

    st.divider()

    # -----------------------------
    # CGPA Trend
    # -----------------------------
    if history:

        chart = recent.iloc[::-1][["CGPA"]]

        st.subheader("📈 CGPA Progress")

        st.line_chart(chart)

    st.divider()

    # -----------------------------
    # Motivation
    # -----------------------------
    st.subheader("🎯 Academic Goal")

    if latest >= 4.50:
        st.success("Excellent work! You're maintaining a First Class. Keep it up! 🏆")

    elif latest >= 3.50:
        st.info("You're in Second Class Upper. A little extra effort can get you to First Class.")

    elif latest >= 2.40:
        st.warning("You're in Second Class Lower. Stay focused—you can still improve your CGPA.")

    elif latest >= 1.50:
        st.warning("You're currently in Third Class. Every semester is a chance to climb higher.")

    else:
        st.error("Your CGPA needs serious attention. Stay determined and improve one course at a time.")
