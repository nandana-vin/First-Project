import sqlite3

DATABASE_NAME = "grades.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_tables():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                target_grade REAL NOT NULL DEFAULT 85
                    CHECK(target_grade >= 0 AND target_grade <= 100)
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                grade REAL NOT NULL CHECK(grade >= 0 AND grade <= 100),
                weight REAL NOT NULL CHECK(weight > 0 AND weight <= 100),
                FOREIGN KEY (course_id)
                    REFERENCES courses(id) ON DELETE CASCADE
            )
        """)


def add_course(name, target_grade=85):
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO courses (name, target_grade) VALUES (?, ?)",
            (name, target_grade)
        )
        return cursor.lastrowid


def get_courses():
    with get_connection() as connection:
        return connection.execute(
            "SELECT id, name, target_grade FROM courses ORDER BY name"
        ).fetchall()


def update_course(course_id, name, target_grade):
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE courses
            SET name = ?, target_grade = ?
            WHERE id = ?
            """,
            (name, target_grade, course_id)
        )


def delete_course(course_id):
    with get_connection() as connection:
        connection.execute(
            "DELETE FROM courses WHERE id = ?",
            (course_id,)
        )


def add_assessment(course_id, name, grade, weight):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO assessments (course_id, name, grade, weight)
            VALUES (?, ?, ?, ?)
            """,
            (course_id, name, grade, weight)
        )
        return cursor.lastrowid


def get_assessments(course_id):
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT id, course_id, name, grade, weight
            FROM assessments
            WHERE course_id = ?
            ORDER BY id
            """,
            (course_id,)
        ).fetchall()


def update_assessment(assessment_id, name, grade, weight):
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE assessments
            SET name = ?, grade = ?, weight = ?
            WHERE id = ?
            """,
            (name, grade, weight, assessment_id)
        )


def delete_assessment(assessment_id):
    with get_connection() as connection:
        connection.execute(
            "DELETE FROM assessments WHERE id = ?",
            (assessment_id,)
        )


if __name__ == "__main__":
    create_tables()
    print("Database created successfully!")