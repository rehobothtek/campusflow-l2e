import unittest

from campusflow.tickets import calculate_priority


class CalculatePriorityTests(unittest.TestCase):
    def test_high_urgency_and_twelve_users_is_critical(self):
        result = calculate_priority("high", 12)
        self.assertEqual(result, "critical")

    def test_high_urgency_and_two_users_is_high(self):
        result = calculate_priority("high", 2)
        self.assertEqual(result, "high")

    def test_low_urgency_and_four_users_is_medium(self):
        result = calculate_priority("low", 4)
        self.assertEqual(result, "medium")

    def test_low_urgency_and_one_user_is_low(self):
        result = calculate_priority("low", 1)
        self.assertEqual(result, "low")


if __name__ == "__main__":
    unittest.main()