import streamlit as st
import pandas as pd
import io
import database


def show():

    st.title("🎓 CGPA Calculator")

    # -----------------------------
    # Session State
    # -----------------------------
    if "courses" not in st.session_state:
        st.session_state.courses = []

    # -----------------------------
    # Previous Record
    # -----------------------------
    st.subheader("Previous Academic Record")

    col1, col2 = st.columns(2)

    with col1:
        prev_cu = st.number_input(
            "Previous Credit Units",
            min_value=0,
            value=0
        )

    with col2:
        prev_qp = st.number_input(
            "Previous Quality Points",
            min_value=0.0,
            value=0.0
        )

    st.divider()

    grades = {
        "A": 5,
        "B": 4,
        "C": 3,
        "D": 2,
        "E": 1,
        "F": 0
    }

    # -----------------------------
    # Add Course
    # -----------------------------
    with st.form("course_form"):

        code = st.text_input("Course Code")

        c1, c2 = st.columns(2)

        with c1:
            cu = st.number_input(
                "Credit Units",
                1,
                6,
                3
            )

        with c2:
            grade = st.selectbox(
                "Grade",
                list(grades.keys())
            )

        add = st.form_submit_button("➕ Add Course")

        if add:

            code = code.strip().upper()

            if code == "":
                st.error("Enter a course code.")

            elif any(x["Course"] == code for x in st.session_state.courses):
                st.warning("Course already added.")

            else:

                st.session_state.courses.append({

                    "Course": code,
                    "Credit Units": cu,
                    "Grade": grade,
                    "GP": grades[grade],
                    "Quality Points": cu * grades[grade]

                })

                st.success(f"{code} added successfully.")

    # -----------------------------
    # Display Courses
    # -----------------------------
    if st.session_state.courses:

        df = pd.DataFrame(st.session_state.courses)

        total_cu = df["Credit Units"].sum()
        total_qp = df["Quality Points"].sum()

        semester_gpa = total_qp / total_cu

        grand_cu = prev_cu + total_cu
        grand_qp = prev_qp + total_qp

        cgpa = grand_qp / grand_cu

        st.divider()

        c1, c2 = st.columns(2)

        c1.metric(
            "Semester GPA",
            f"{semester_gpa:.2f}"
        )

        c2.metric(
            "Cumulative CGPA",
            f"{cgpa:.2f}"
        )

        # Classification
        if cgpa >= 4.50:
            st.success("🏆 First Class")
        elif cgpa >= 3.50:
            st.info("🥇 Second Class Upper")
        elif cgpa >= 2.40:
            st.info("🥈 Second Class Lower")
        elif cgpa >= 1.50:
            st.warning("🎓 Third Class")
        else:
            st.error("⚠️ Pass")

        st.divider()

        st.subheader("Courses")

        st.dataframe(
            df[
                [
                    "Course",
                    "Credit Units",
                    "Grade",
                    "Quality Points"
                ]
            ],
            use_container_width=True
        )

        # Delete Course
        course = st.selectbox(
            "Delete Course",
            df["Course"]
        )

        if st.button("Delete"):

            st.session_state.courses = [

                c for c in st.session_state.courses

                if c["Course"] != course

            ]

            st.rerun()

        st.divider()

        # Save History
        if st.button("💾 Save Result"):

            database.save_history(

                st.session_state.username,

                semester_gpa,

                cgpa,

                grand_cu,

                grand_qp

            )

            st.success("Calculation saved.")

        st.divider()

        # CSV Export
        csv = io.BytesIO()

        df.to_csv(
            csv,
            index=False
        )

        st.download_button(

            "📥 Download CSV",

            csv.getvalue(),

            "cgpa_result.csv",

            "text/csv"

        )

    else:

        st.info("No courses added yet.")
