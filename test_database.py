import os
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

import database


class TestDatabase(unittest.TestCase):

    def setUp(self):
        # Create a separate temporary database for each test
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(
            self.temp_dir.name,
            "test_grades.db"
        )

        # Redirect database connections to the test database
        self.original_get_connection = database.get_connection

        def test_connection():
            connection = sqlite3.connect(self.db_path)
            connection.execute("PRAGMA foreign_keys = ON")
            return connection

        self.patcher = patch(
            "database.get_connection",
            side_effect=test_connection
        )
        self.patcher.start()

        database.create_tables()

    def tearDown(self):
        # Restore the original database connection
        self.patcher.stop()
        self.temp_dir.cleanup()

    def test_add_course(self):
        course_id = database.add_course("CISC 121")

        self.assertEqual(course_id, 1)

    def test_get_courses(self):
        database.add_course("CISC 171")

        courses = database.get_courses()

        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0][1], "CISC 171")

    def test_update_course(self):
        course_id = database.add_course("CISC 121")

        database.update_course(
            course_id,
            "CISC 121 Updated",
            90
        )

        courses = database.get_courses()

        self.assertEqual(courses[0][1], "CISC 121 Updated")
        self.assertEqual(courses[0][2], 90)

    def test_add_assessment(self):
        course_id = database.add_course("CISC 121")

        database.add_assessment(
            course_id,
            "Assignment 1",
            85,
            20
        )

        assessments = database.get_assessments(course_id)

        self.assertEqual(len(assessments), 1)
        self.assertEqual(assessments[0][2], "Assignment 1")
        self.assertEqual(assessments[0][3], 85)
        self.assertEqual(assessments[0][4], 20)

    def test_update_assessment(self):
        course_id = database.add_course("CISC 121")

        assessment_id = database.add_assessment(
            course_id,
            "Assignment 1",
            85,
            20
        )

        database.update_assessment(
            assessment_id,
            "Assignment 1 Updated",
            90,
            25
        )

        assessments = database.get_assessments(course_id)

        self.assertEqual(
            assessments[0][2],
            "Assignment 1 Updated"
        )
        self.assertEqual(assessments[0][3], 90)
        self.assertEqual(assessments[0][4], 25)

    def test_delete_assessment(self):
        course_id = database.add_course("CISC 121")

        assessment_id = database.add_assessment(
            course_id,
            "Assignment 1",
            85,
            20
        )

        database.delete_assessment(assessment_id)

        assessments = database.get_assessments(course_id)

        self.assertEqual(len(assessments), 0)

    def test_delete_course(self):
        course_id = database.add_course("CISC 121")

        database.delete_course(course_id)

        courses = database.get_courses()

        self.assertEqual(len(courses), 0)


if __name__ == "__main__":
    unittest.main()