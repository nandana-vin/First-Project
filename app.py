import streamlit as st

from calculations import (
    calculate_weighted_grade,
    calculate_current_average,
    calculate_required_grade
)

st.set_page_config(
    page_title="Student Grade Tracker",
    page_icon="🎓",
    layout="centered"
)

st.title("Student Grade Tracker")

st.write("Track your grades and calculate what you need to reach your goals.")

course = st.text_input("Enter your course name", "CISC 171")

num_assignments = st.number_input(
    "Number of graded assessments",
    min_value=1,
    max_value=20,
    value=3,
    step=1
)

total_weighted_grade = 0
total_weight = 0

st.subheader("Your Assessments")

for i in range(num_assignments):

    st.write(f"Assessment {i + 1}")

    grade = st.number_input(
        f"Grade (%) - Assessment {i + 1}",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        key=f"grade_{i}"
    )

    weight = st.number_input(
        f"Weight (%) - Assessment {i + 1}",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        key=f"weight_{i}"
    )

    weighted_grade = calculate_weighted_grade(grade, weight)

    total_weighted_grade += weighted_grade
    total_weight += weight

st.divider()

st.subheader("Your Results")

if total_weight > 100:
    st.error("Total assessment weight cannot exceed 100%.")

elif total_weight > 0:

    current_average = calculate_current_average(
        total_weighted_grade,
        total_weight
    )

    st.metric("Current Average", f"{current_average:.2f}%")

    st.metric("Completed Course Weight", f"{total_weight:.2f}%")

    st.subheader("Target Grade Calculator")

    target_grade = st.number_input(
        "Desired Final Grade (%)",
        min_value=0.0,
        max_value=100.0,
        value=85.0
    )

    if total_weight < 100:

        required_average = calculate_required_grade(
            target_grade,
            total_weighted_grade,
            total_weight
        )

        st.metric(
            "Required Average on Remaining Assessments",
            f"{required_average:.2f}%"
        )

        if required_average > 100:
            st.error("Your target is not achievable.")

        elif required_average <= 0:
            st.success("You have already earned enough points to reach your target!")

        else:
            st.success("Your target is mathematically achievable!")

    else:
        st.info("All course assessments have been completed.")

else:
    st.info("Enter your assessment grades and weights to see your results.")