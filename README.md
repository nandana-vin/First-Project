# Student Grade Tracker

A Python-based academic grade management application that helps university students track their course performance, calculate weighted averages, and determine the grades required to achieve their academic goals.

Built using Python, Streamlit, SQLite, and Pandas.

## Project Overview

Student Grade Tracker is an interactive web application designed to simplify academic grade management.

Students can organize multiple courses, record assessment grades, calculate their current standing, and determine the average required on remaining assessments to achieve a desired final grade.

The application uses SQLite for persistent data storage, allowing users to retrieve saved course information after restarting the application.

## Features

### Academic Dashboard
- View all courses in one dashboard.
- Compare current averages across courses.
- Track completed assessment weights.
- Visualize academic performance using charts.

### Course Management
- Add new courses.
- Edit course names and target grades.
- Delete courses.
- Manage assessments for individual courses.

### Grade Calculator
- Calculate weighted assessment contributions.
- Calculate current course averages.
- Track completed course weight.
- Calculate the average required on remaining assessments.
- Identify whether a target grade is mathematically achievable.

### Database Integration
- Store courses and assessments using SQLite.
- Retrieve previously saved grades.
- Update and delete assessment records.
- Preserve data across application restarts within the same persistent environment.

### Input Validation
- Validate grade percentages.
- Prevent assessment weights from exceeding 100% through the application interface.
- Handle duplicate course names.
- Display feedback for invalid inputs.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Interactive web interface |
| SQLite | Database management |
| Pandas | Data processing and dashboard tables |
| unittest | Automated testing |
| Git | Version control |
| GitHub | Source code hosting |

## Project Structure

```text
student-grade-tracker/
│
├── app.py
├── calculations.py
├── database.py
├── grade_calculator.py
├── test_calculations.py
├── test_database.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/nandana-vin/First-Project.git
```

### 2. Navigate to the project directory

```bash
cd First-Project
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Initialize the database

```bash
python database.py
```

### 5. Launch the application

```bash
python -m streamlit run app.py
```

Streamlit will display a local URL that you can open in your browser.

## Example Grade Calculation

Suppose a student has completed two assessments:

| Assessment | Grade | Weight |
|---|---:|---:|
| Assignment 1 | 90% | 20% |
| Midterm | 80% | 30% |

**Weighted grade contributions:**

Assignment 1:

90 × 0.20 = 18

Midterm:

80 × 0.30 = 24

Total weighted contribution:

18 + 24 = 42

Completed course weight:

20% + 30% = 50%

Current average:

42 ÷ 0.50 = **84%**

If the student wants a final grade of 85%, the required average on the remaining 50% is:

(85 − 42) ÷ 0.50 = **86%**

The application automatically performs these calculations.

## Automated Testing

The project includes automated unit tests for calculation functions and SQLite database operations.

### Run all tests

```bash
python -m unittest discover -v
```

The test suite includes:

**Calculation tests**
- Weighted grade calculation
- Current average calculation
- Required grade calculation
- Zero-weight handling
- No remaining assessment weight

**Database tests**
- Adding courses
- Retrieving courses
- Updating courses
- Deleting courses
- Adding assessments
- Updating assessments
- Deleting assessments

The project currently includes 12 automated unit tests.

## Screenshots

Screenshots of the academic dashboard and course tracker will be added.

## Future Improvements

- User authentication and individual student accounts.
- Cloud database integration.
- Grade history and progress tracking.
- GPA calculation.
- CSV import and export.
- Mobile-friendly interface improvements.
- Public application deployment.

## Author

Nandana Vinodkumar

Computer Science Student  
Queen's University

GitHub: [nandana-vin](https://github.com/nandana-vin)

## Project Status

Core application implemented with course management, grade calculations, SQLite persistence, dashboard visualizations, and automated unit tests.

Further improvements and deployment are planned.