import streamlit as st
import pandas as pd
import database

grades = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2,
    "E": 1,
    "F": 0
}


def show():

    st.title("🎓 CGPA Calculator")

    if "courses" not in st.session_state:
        st.session_state.courses = []

    st.subheader("Previous Record")

    prev_cu = st.number_input(
        "Previous Total Credit Units",
        min_value=0,
        value=0
    )

    prev_qp = st.number_input(
        "Previous Total Quality Points",
        min_value=0.0,
        value=0.0
    )

    st.divider()

    with st.form("course_form"):

        course = st.text_input("Course Code")

        col1, col2 = st.columns(2)

        with col1:
            cu = st.number_input(
                "Credit Units",
                1,
                6,
                3
            )

        with col2:
            grade = st.selectbox(
                "Grade",
                list(grades.keys())
            )

        add = st.form_submit_button("Add Course")

        if add:

            if course.strip() == "":
                st.error("Enter a course code.")

            else:

                st.session_state.courses.append({

                    "Course": course.upper(),

                    "Credit Units": cu,

                    "Grade": grade,

                    "GP": grades[grade],

                    "Quality Points": cu * grades[grade]

                })

                st.success(f"{course.upper()} added.")

    if st.session_state.courses:

        df = pd.DataFrame(st.session_state.courses)

        st.subheader("Courses")

        st.dataframe(
            df,
            use_container_width=True
        )

        total_cu = df["Credit Units"].sum()

        total_qp = df["Quality Points"].sum()

        gpa = total_qp / total_cu

        grand_cu = prev_cu + total_cu

        grand_qp = prev_qp + total_qp

        cgpa = grand_qp / grand_cu

        st.divider()

        c1, c2 = st.columns(2)

        c1.metric(
            "Semester GPA",
            f"{gpa:.2f}"
        )

        c2.metric(
            "CGPA",
            f"{cgpa:.2f}"
        )

        if cgpa >= 4.50:
            st.success("🏆 First Class")

        elif cgpa >= 3.50:
            st.info("🥇 Second Class Upper")

        elif cgpa >= 2.40:
            st.info("🥈 Second Class Lower")

        elif cgpa >= 1.50:
            st.warning("🎓 Third Class")

        else:
            st.error("⚠ Pass")

        col1, col2 = st.columns(2)

        if col1.button("💾 Save Result"):

            database.save_history(

                st.session_state.username,

                float(gpa),

                float(cgpa),

                int(grand_cu),

                float(grand_qp)

            )

            st.success("Result saved successfully.")

        if col2.button("🗑 Clear Courses"):

            st.session_state.courses = []

            st.rerun()