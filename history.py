import streamlit as st
import pandas as pd
import io
import database


def show():

    st.title("📊 Calculation History")

    history = database.get_history(
        st.session_state.username
    )

    if not history:
        st.info("You haven't saved any calculations yet.")
        return

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

    # -----------------------------
    # Summary
    # -----------------------------
    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Saved Results",
        len(df)
    )

    c2.metric(
        "Highest CGPA",
        f"{df['CGPA'].max():.2f}"
    )

    c3.metric(
        "Average CGPA",
        f"{df['CGPA'].mean():.2f}"
    )

    st.divider()

    # -----------------------------
    # Search
    # -----------------------------
    search = st.text_input(
        "🔍 Search by Date"
    )

    if search:

        df = df[
            df["Date"]
            .astype(str)
            .str.contains(
                search,
                case=False
            )
        ]

    # -----------------------------
    # History Table
    # -----------------------------
    st.subheader("Saved Calculations")

    st.dataframe(
        df.drop(columns=["ID"]),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # -----------------------------
    # Delete Record
    # -----------------------------
    st.subheader("Delete a Record")

    record = st.selectbox(
        "Select Record",
        df["ID"]
    )

    if st.button(
        "🗑 Delete Record",
        use_container_width=True
    ):

        database.delete_history(
            int(record)
        )

        st.success(
            "Record deleted successfully."
        )

        st.rerun()

    st.divider()

    # -----------------------------
    # Download CSV
    # -----------------------------
    csv = io.BytesIO()

    df.drop(columns=["ID"]).to_csv(
        csv,
        index=False
    )

    st.download_button(
        "📥 Download History (CSV)",
        csv.getvalue(),
        file_name="cgpa_history.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.divider()

    # -----------------------------
    # CGPA Trend
    # -----------------------------
    st.subheader("📈 CGPA Trend")

    chart = df.iloc[::-1][["CGPA"]]

    st.line_chart(chart)