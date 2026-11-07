import streamlit as st

from calculations import (
    calculate_weighted_grade,
    calculate_current_average,
    calculate_required_grade
)

# Page configuration
st.set_page_config(
    page_title="Student Grade Tracker",
    page_icon="🎓",
    layout="centered"
)

st.title("Student Grade Tracker")
st.write("Track your grades and calculate what you need to reach your goals.")


# Initialize course storage
if "courses" not in st.session_state:
    st.session_state.courses = {
        "CISC 121": {},
        "CISC 171": {},
        "MATH 121": {}
    }


# Save assessment grades and weights
def save_grade(course_name, assessment_number):
    grade_key = f"{course_name}_grade_{assessment_number}"
    weight_key = f"{course_name}_weight_{assessment_number}"

    course_data = st.session_state.courses[course_name]

    if grade_key in st.session_state:
        course_data[grade_key] = st.session_state[grade_key]

    if weight_key in st.session_state:
        course_data[weight_key] = st.session_state[weight_key]


# Save number of assessments
def save_assessment_count(course_name):
    count_key = f"{course_name}_num_assignments"

    st.session_state.courses[course_name]["num_assignments"] = (
        st.session_state[count_key]
    )


# Course selector
st.sidebar.title("My Courses")

course = st.sidebar.selectbox(
    "Select a course",
    ["CISC 121", "CISC 171", "MATH 121"]
)

course_data = st.session_state.courses[course]


# Restore assessment count
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


# Initialize totals
total_weighted_grade = 0
total_weight = 0

st.subheader("Your Assessments")


# Assessment inputs
for i in range(num_assignments):

    st.write(f"Assessment {i + 1}")

    grade_key = f"{course}_grade_{i}"
    weight_key = f"{course}_weight_{i}"

    # Restore saved grade
    if grade_key not in st.session_state:
        st.session_state[grade_key] = course_data.get(
            grade_key, 0.0
        )

    # Restore saved weight
    if weight_key not in st.session_state:
        st.session_state[weight_key] = course_data.get(
            weight_key, 0.0
        )

    grade = st.number_input(
        f"Grade (%) - Assessment {i + 1}",
        min_value=0.0,
        max_value=100.0,
        step=1.0,
        key=grade_key,
        on_change=save_grade,
        args=(course, i)
    )

    weight = st.number_input(
        f"Weight (%) - Assessment {i + 1}",
        min_value=0.0,
        max_value=100.0,
        step=1.0,
        key=weight_key,
        on_change=save_grade,
        args=(course, i)
    )

    # Calculate weighted grade
    weighted_grade = calculate_weighted_grade(
        grade,
        weight
    )

    total_weighted_grade += weighted_grade
    total_weight += weight


# Results section
st.divider()

st.subheader("Your Results")

if total_weight > 100:
    st.error(
        "Total assessment weight cannot exceed 100%. "
        "Please check your assessment weights."
    )

elif total_weight > 0:

    current_average = calculate_current_average(
        total_weighted_grade,
        total_weight
    )

    st.metric(
        "Current Average",
        f"{current_average:.2f}%"
    )

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

    # Save target grade
    def save_target():
        st.session_state.courses[course]["target_grade"] = (
            st.session_state[target_key]
        )

    target_grade = st.number_input(
        "Desired Final Grade (%)",
        min_value=0.0,
        max_value=100.0,
        step=1.0,
        key=target_key,
        on_change=save_target
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
                    "Your target is not achievable with "
                    "the remaining assessments."
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
            st.warning(
                "Unable to calculate the required grade."
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