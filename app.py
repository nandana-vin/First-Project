import streamlit as st
import pandas as pd

from calculations import (
    calculate_weighted_grade,
    calculate_current_average,
    calculate_required_grade
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Student Grade Tracker",
    page_icon="🎓",
    layout="wide"
)

st.title("Student Grade Tracker")
st.write("Track your academic performance and calculate your target grades.")


# --------------------------------------------------
# INITIALIZE SESSION STATE
# --------------------------------------------------

COURSE_NAMES = ["CISC 121", "CISC 171", "MATH 121"]

if "courses" not in st.session_state:
    st.session_state.courses = {
        name: {} for name in COURSE_NAMES
    }


# --------------------------------------------------
# SAVE FUNCTIONS
# --------------------------------------------------

def save_grade(course_name, assessment_number):

    grade_key = f"{course_name}_grade_{assessment_number}"
    weight_key = f"{course_name}_weight_{assessment_number}"

    course_data = st.session_state.courses[course_name]

    if grade_key in st.session_state:
        course_data[grade_key] = st.session_state[grade_key]

    if weight_key in st.session_state:
        course_data[weight_key] = st.session_state[weight_key]


def save_assessment_count(course_name):

    count_key = f"{course_name}_num_assignments"

    st.session_state.courses[course_name]["num_assignments"] = (
        st.session_state[count_key]
    )


def save_target(course_name):

    target_key = f"{course_name}_target_grade"

    st.session_state.courses[course_name]["target_grade"] = (
        st.session_state[target_key]
    )


# --------------------------------------------------
# CALCULATE COURSE RESULTS
# --------------------------------------------------

def get_course_results(course_name):

    course_data = st.session_state.courses[course_name]

    num_assignments = course_data.get("num_assignments", 3)

    total_weighted_grade = 0
    total_weight = 0

    for i in range(num_assignments):

        grade_key = f"{course_name}_grade_{i}"
        weight_key = f"{course_name}_weight_{i}"

        grade = course_data.get(grade_key, 0.0)
        weight = course_data.get(weight_key, 0.0)

        total_weighted_grade += calculate_weighted_grade(
            grade, weight
        )

        total_weight += weight

    if total_weight > 100:
        return None, total_weight

    if total_weight > 0:

        average = calculate_current_average(
            total_weighted_grade,
            total_weight
        )

        return average, total_weight

    return None, 0


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Course Tracker"]
)


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if page == "Dashboard":

    st.header("Academic Dashboard")

    dashboard_data = []

    for course_name in COURSE_NAMES:

        average, completed_weight = get_course_results(
            course_name
        )

        target = st.session_state.courses[course_name].get(
            "target_grade", 85.0
        )

        dashboard_data.append({
            "Course": course_name,
            "Current Average": average,
            "Completed Weight": completed_weight,
            "Target Grade": target
        })

    df = pd.DataFrame(dashboard_data)

    # Summary metrics
    total_courses = len(COURSE_NAMES)

    active_courses = df["Current Average"].notna().sum()

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Courses", total_courses)

    with col2:
        st.metric("Courses With Grades", active_courses)

    st.divider()

    # Course overview table
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

    # Grade comparison chart
    st.subheader("Grade Comparison")

    chart_df = df.dropna(
        subset=["Current Average"]
    )

    if not chart_df.empty:

        st.bar_chart(
            chart_df.set_index("Course")["Current Average"]
        )

    else:
        st.info(
            "Enter grades in the Course Tracker to see your chart."
        )


# --------------------------------------------------
# COURSE TRACKER
# --------------------------------------------------

elif page == "Course Tracker":

    st.header("Course Grade Tracker")

    course = st.selectbox(
        "Select a course",
        COURSE_NAMES
    )

    course_data = st.session_state.courses[course]

    # Assessment count
    count_key = f"{course}_num_assignments"

    if count_key not in st.session_state:
        st.session_state[count_key] = course_data.get(
            "num_assignments", 3
        )

    num_assignments = st.number_input(
        "Number of graded assessments",
        min_value=1,
        max_value=20,
        step=1,
        key=count_key,
        on_change=save_assessment_count,
        args=(course,)
    )

    total_weighted_grade = 0
    total_weight = 0

    st.subheader("Your Assessments")

    for i in range(num_assignments):

        st.write(f"Assessment {i + 1}")

        grade_key = f"{course}_grade_{i}"
        weight_key = f"{course}_weight_{i}"

        # Restore grade
        if grade_key not in st.session_state:
            st.session_state[grade_key] = course_data.get(
                grade_key, 0.0
            )

        # Restore weight
        if weight_key not in st.session_state:
            st.session_state[weight_key] = course_data.get(
                weight_key, 0.0
            )

        col1, col2 = st.columns(2)

        with col1:

            grade = st.number_input(
                f"Grade (%) - Assessment {i + 1}",
                min_value=0.0,
                max_value=100.0,
                step=1.0,
                key=grade_key,
                on_change=save_grade,
                args=(course, i)
            )

        with col2:

            weight = st.number_input(
                f"Weight (%) - Assessment {i + 1}",
                min_value=0.0,
                max_value=100.0,
                step=1.0,
                key=weight_key,
                on_change=save_grade,
                args=(course, i)
            )

        total_weighted_grade += calculate_weighted_grade(
            grade, weight
        )

        total_weight += weight

    st.divider()

    # Results
    st.subheader("Your Results")

    if total_weight > 100:

        st.error(
            "Total assessment weight cannot exceed 100%."
        )

    elif total_weight > 0:

        current_average = calculate_current_average(
            total_weighted_grade,
            total_weight
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Current Average",
                f"{current_average:.2f}%"
            )

        with col2:
            st.metric(
                "Completed Course Weight",
                f"{total_weight:.2f}%"
            )

        st.subheader("Target Grade Calculator")

        target_key = f"{course}_target_grade"

        if target_key not in st.session_state:
            st.session_state[target_key] = course_data.get(
                "target_grade", 85.0
            )

        target_grade = st.number_input(
            "Desired Final Grade (%)",
            min_value=0.0,
            max_value=100.0,
            step=1.0,
            key=target_key,
            on_change=save_target,
            args=(course,)
        )

        if total_weight < 100:

            required_average = calculate_required_grade(
                target_grade,
                total_weighted_grade,
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

            st.info(
                "All course assessments have been completed."
            )

    else:

        st.info(
            "Enter your assessment grades and weights "
            "to see your results."
        )