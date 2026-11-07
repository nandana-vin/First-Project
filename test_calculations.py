import unittest

from calculations import (
    calculate_weighted_grade,
    calculate_current_average,
    calculate_required_grade
)


class TestGradeCalculations(unittest.TestCase):

    def test_weighted_grade(self):
        result = calculate_weighted_grade(85, 20)
        self.assertEqual(result, 17)

    def test_current_average(self):
        result = calculate_current_average(41.5, 50)
        self.assertEqual(result, 83)

    def test_required_grade(self):
        result = calculate_required_grade(85, 41.5, 50)
        self.assertEqual(result, 87)

    def test_zero_weight(self):
        result = calculate_current_average(0, 0)
        self.assertEqual(result, 0)

    def test_no_remaining_weight(self):
        result = calculate_required_grade(85, 83, 100)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()