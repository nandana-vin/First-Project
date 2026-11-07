import sqlite3

import pandas as pd
import streamlit as st

from calculations import (
    calculate_weighted_grade,
    calculate_current_average,
    calculate_required_grade
)

from database import (
    create_tables,
    add_course,
    get_courses,
    update_course,
    delete_course,
    add_assessment,
    get_assessments,
    update_assessment,
    delete_assessment
)


# -----------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------

st.set_page_config(
    page_title="Student Grade Tracker",
    page_icon="🎓",
    layout="wide"
)

create_tables()

st.title("Student Grade Tracker")
st.write("Track your grades and calculate what you need to reach your goals.")


# -----------------------------------------
# CALCULATE COURSE RESULTS
# -----------------------------------------

def get_course_results(course_id):

    assessments = get_assessments(course_id)

    total_weighted_grade = 0
    total_weight = 0

    for assessment in assessments:

        assessment_id, course_id, name, grade, weight = assessment

        total_weighted_grade += calculate_weighted_grade(
            grade, weight
        )

        total_weight += weight

    if total_weight > 100:
        return None, total_weight, total_weighted_grade

    if total_weight > 0:

        average = calculate_current_average(
            total_weighted_grade,
            total_weight
        )

        return average, total_weight, total_weighted_grade

    return None, 0, 0


# -----------------------------------------
# SIDEBAR NAVIGATION
# -----------------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Course Tracker", "Manage Courses"]
)


# -----------------------------------------
# DASHBOARD
# -----------------------------------------

if page == "Dashboard":

    st.header("Academic Dashboard")

    courses = get_courses()

    dashboard_data = []

    for course_id, name, target_grade in courses:

        average, completed_weight, _ = get_course_results(
            course_id
        )

        dashboard_data.append({
            "Course": name,
            "Current Average": average,
            "Completed Weight": completed_weight,
            "Target Grade": target_grade
        })

    if dashboard_data:

        df = pd.DataFrame(dashboard_data)

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Total Courses", len(courses))

        with col2:
            st.metric(
                "Courses With Grades",
                int(df["Current Average"].notna().sum())
            )

        st.divider()

        st.subheader("Course Overview")

        display_df = df.copy()

        display_df["Current Average"] = display_df[
            "Current Average"
        ].apply(
            lambda x: f"{x:.2f}%" if pd.notna(x) else "No grades"
        )

        display_df["Completed Weight"] = display_df[
            "Completed Weight"
        ].apply(
            lambda x: f"{x:.2f}%"
        )

        display_df["Target Grade"] = display_df[
            "Target Grade"
        ].apply(
            lambda x: f"{x:.2f}%"
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Grade Comparison")

        chart_df = df.dropna(
            subset=["Current Average"]
        )

        if not chart_df.empty:

            st.bar_chart(
                chart_df.set_index("Course")["Current Average"]
            )

        else:
            st.info("Add assessments to see your grade chart.")

    else:
        st.info(
            "No courses found. Go to Manage Courses to add one."
        )


# -----------------------------------------
# MANAGE COURSES
# -----------------------------------------

elif page == "Manage Courses":

    st.header("Manage Courses")

    st.subheader("Add a New Course")

    with st.form("add_course_form"):

        course_name = st.text_input(
            "Course Name",
            placeholder="Example: CISC 121"
        )

        target_grade = st.number_input(
            "Target Grade (%)",
            min_value=0.0,
            max_value=100.0,
            value=85.0
        )

        submitted = st.form_submit_button("Add Course")

        if submitted:

            if not course_name.strip():
                st.error("Please enter a course name.")

            else:
                try:
                    add_course(
                        course_name.strip(),
                        target_grade
                    )

                    st.success("Course added successfully!")
                    st.rerun()

                except sqlite3.IntegrityError:
                    st.error(
                        "This course already exists or contains invalid data."
                    )

    st.divider()

    st.subheader("Existing Courses")

    courses = get_courses()

    for course_id, name, target_grade in courses:

        with st.expander(name):

            with st.form(f"edit_course_{course_id}"):

                new_name = st.text_input(
                    "Course Name",
                    value=name
                )

                new_target = st.number_input(
                    "Target Grade (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(target_grade)
                )

                if st.form_submit_button("Save Changes"):

                    try:
                        update_course(
                            course_id,
                            new_name.strip(),
                            new_target
                        )

                        st.success("Course updated!")
                        st.rerun()

                    except sqlite3.IntegrityError:
                        st.error("Unable to update course.")

            st.warning(
                "Deleting a course will also delete its assessments."
            )

            confirm_delete = st.checkbox(
                "I understand this will delete the course",
                key=f"confirm_course_{course_id}"
            )

            if st.button(
                "Delete Course",
                key=f"delete_course_{course_id}",
                disabled=not confirm_delete
            ):

                # Explicitly remove assessments first.
                # This also works with the original database schema.
                with sqlite3.connect("grades.db") as connection:
                    connection.execute(
                        "DELETE FROM assessments WHERE course_id = ?",
                        (course_id,)
                    )

                    connection.execute(
                        "DELETE FROM courses WHERE id = ?",
                        (course_id,)
                    )

                st.success("Course deleted.")
                st.rerun()


# -----------------------------------------
# COURSE TRACKER
# -----------------------------------------

elif page == "Course Tracker":

    st.header("Course Grade Tracker")

    courses = get_courses()

    if not courses:

        st.info(
            "No courses available. Add a course under Manage Courses."
        )

    else:

        course_options = {
            name: (course_id, target)
            for course_id, name, target in courses
        }

        selected_course = st.selectbox(
            "Select a Course",
            list(course_options.keys())
        )

        course_id, target_grade = course_options[
            selected_course
        ]

        st.subheader("Add Assessment")

        with st.form("add_assessment_form"):

            assessment_name = st.text_input(
                "Assessment Name",
                placeholder="Example: Midterm 1"
            )

            grade = st.number_input(
                "Grade (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.0
            )

            weight = st.number_input(
                "Weight (%)",
                min_value=0.01,
                max_value=100.0,
                value=10.0
            )

            submitted = st.form_submit_button(
                "Add Assessment"
            )

            if submitted:

                _, current_weight, _ = get_course_results(
                    course_id
                )

                if not assessment_name.strip():
                    st.error("Enter an assessment name.")

                elif current_weight + weight > 100.000001:
                    st.error(
                        "Total assessment weight cannot exceed 100%."
                    )

                else:

                    try:
                        add_assessment(
                            course_id,
                            assessment_name.strip(),
                            grade,
                            weight
                        )

                        st.success("Assessment saved!")
                        st.rerun()

                    except sqlite3.IntegrityError:
                        st.error("Unable to save assessment.")

        st.divider()

        st.subheader("Your Assessments")

        assessments = get_assessments(course_id)

        if not assessments:

            st.info("No assessments added yet.")

        for assessment in assessments:

            assessment_id, _, name, grade, weight = assessment

            with st.expander(name):

                with st.form(f"edit_assessment_{assessment_id}"):

                    new_name = st.text_input(
                        "Assessment Name",
                        value=name
                    )

                    new_grade = st.number_input(
                        "Grade (%)",
                        min_value=0.0,
                        max_value=100.0,
                        value=float(grade)
                    )

                    new_weight = st.number_input(
                        "Weight (%)",
                        min_value=0.01,
                        max_value=100.0,
                        value=float(weight)
                    )

                    if st.form_submit_button("Save Changes"):

                        _, current_weight, _ = get_course_results(
                            course_id
                        )

                        updated_total = (
                            current_weight - weight + new_weight
                        )

                        if not new_name.strip():
                            st.error("Enter an assessment name.")

                        elif updated_total > 100.000001:
                            st.error(
                                "Total assessment weight cannot exceed 100%."
                            )

                        else:

                            update_assessment(
                                assessment_id,
                                new_name.strip(),
                                new_grade,
                                new_weight
                            )

                            st.success("Assessment updated!")
                            st.rerun()

                if st.button(
                    "Delete Assessment",
                    key=f"delete_assessment_{assessment_id}"
                ):

                    delete_assessment(assessment_id)

                    st.success("Assessment deleted.")
                    st.rerun()

        st.divider()

        st.subheader("Your Results")

        average, total_weight, total_weighted = (
            get_course_results(course_id)
        )

        if total_weight > 100:

            st.error(
                "Assessment weights exceed 100%. "
                "Please correct your saved assessments."
            )

        elif average is not None:

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Current Average",
                    f"{average:.2f}%"
                )

            with col2:
                st.metric(
                    "Completed Course Weight",
                    f"{total_weight:.2f}%"
                )

            st.subheader("Target Grade Calculator")

            st.write(
                f"Your target final grade: {target_grade:.2f}%"
            )

            if total_weight < 100:

                required_average = calculate_required_grade(
                    target_grade,
                    total_weighted,
                    total_weight
                )

                if required_average is not None:

                    st.metric(
                        "Required Average on Remaining Assessments",
                        f"{required_average:.2f}%"
                    )

                    if required_average > 100:
                        st.error(
                            "Your target is not achievable."
                        )

                    elif required_average <= 0:
                        st.success(
                            "You have already earned enough points "
                            "to reach your target!"
                        )

                    else:
                        st.success(
                            "Your target is mathematically achievable!"
                        )

            else:
                st.info("All assessments have been completed.")

        else:
            st.info(
                "Add assessments to calculate your current average."
            )