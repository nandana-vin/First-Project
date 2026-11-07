from calculations import (
    calculate_weighted_grade,
    calculate_current_average,
    calculate_required_grade
)

print("Welcome to the Student Grade Calculator!")

course = input("Enter your course name: ")

# Ask for the number of assessments
while True:
    try:
        num_assignments = int(input("How many graded assessments do you have? "))

        if num_assignments >= 0:
            break
        else:
            print("Error: Number of assessments cannot be negative.")

    except ValueError:
        print("Error: Please enter a valid whole number.")

total_weighted_grade = 0
total_weight = 0

# Enter assessment grades and weights
for i in range(num_assignments):
    print("\nAssessment", i + 1)

    # Validate grade
    while True:
        try:
            grade = float(input("Enter grade (%): "))

            if 0 <= grade <= 100:
                break
            else:
                print("Error: Grade must be between 0 and 100.")

        except ValueError:
            print("Error: Please enter a valid number.")

    # Validate weight
    while True:
        try:
            weight = float(input("Enter weight (%): "))

            if 0 < weight <= 100 - total_weight:
                break
            else:
                print("Error: Weight must be positive and total course weight cannot exceed 100%.")

        except ValueError:
            print("Error: Please enter a valid number.")

    # Calculate weighted grade
    weighted_grade = calculate_weighted_grade(grade, weight)

    total_weighted_grade += weighted_grade
    total_weight += weight


# Calculate current course average
if total_weight > 0:
    current_average = calculate_current_average(
        total_weighted_grade,
        total_weight
    )

    print("\nCourse:", course)
    print("Current average:", round(current_average, 2), "%")
    print("Completed course weight:", total_weight, "%")

else:
    print("No graded assessments entered.")


# Target grade calculator
print("\n--- Target Grade Calculator ---")

if 0 < total_weight < 100:

    while True:
        try:
            target_grade = float(input("Enter your desired final grade (%): "))

            if 0 <= target_grade <= 100:
                break
            else:
                print("Error: Target grade must be between 0 and 100.")

        except ValueError:
            print("Error: Please enter a valid number.")

    remaining_weight = 100 - total_weight

    required_average = calculate_required_grade(
        target_grade,
        total_weighted_grade,
        total_weight
    )

    print("\nYour target final grade:", target_grade, "%")
    print("Remaining course weight:", remaining_weight, "%")

    if required_average is not None:
        print(
            "Required average on remaining assessments:",
            round(required_average, 2),
            "%"
        )

        if required_average > 100:
            print("Your target is not achievable with the remaining assessments.")

        elif required_average <= 0:
            print("You have already earned enough points to reach your target!")

        else:
            print("Your target is mathematically achievable.")

    else:
        print("Unable to calculate the required grade.")

elif total_weight == 100:
    print("All course assessments have been completed.")

else:
    print("Target calculation unavailable. Check your assessment weights.")