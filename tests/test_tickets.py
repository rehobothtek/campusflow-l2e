import unittest

from campusflow.tickets import calculate_priority, create_ticket


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

    def test_invalid_urgency_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_priority("urgent", 1)

    def test_invalid_affected_users_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_priority("low", "three")


class CreateTicketTests(unittest.TestCase):
    def setUp(self):
        self.tickets = []

    def test_valid_ticket_is_created_with_normalized_values(self):
        ticket = create_ticket(
            self.tickets,
            " Campus Wi-Fi is down ",
            "network",
            "HIGH",
            12,
        )

        self.assertEqual(ticket["id"], "T001")
        self.assertEqual(ticket["title"], "Campus Wi-Fi is down")
        self.assertEqual(ticket["category"], "Network")
        self.assertEqual(ticket["urgency"], "high")
        self.assertEqual(ticket["affected_users"], 12)
        self.assertEqual(ticket["priority"], "critical")
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])
        self.assertEqual(self.tickets, [ticket])

    def test_blank_title_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket(self.tickets, "   ", "Network", "low", 1)

    def test_zero_affected_users_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket(self.tickets, "Broken laptop", "Hardware", "low", 0)

    def test_decimal_affected_users_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket(self.tickets, "Broken laptop", "Hardware", "low", 1.5)

    def test_invalid_category_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket(self.tickets, "Broken laptop", "Facilities", "low", 1)

    def test_invalid_urgency_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket(self.tickets, "Broken laptop", "Hardware", "urgent", 1)

    def test_next_id_uses_highest_existing_ticket_id(self):
        self.tickets = [{"id": "T001"}, {"id": "T009"}]

        ticket = create_ticket(
            self.tickets,
            "Printer is unavailable",
            "Hardware",
            "low",
            1,
        )

        self.assertEqual(ticket["id"], "T010")

    def test_malformed_existing_id_is_ignored(self):
        self.tickets = [{"id": 42}]

        ticket = create_ticket(
            self.tickets,
            "Printer is unavailable",
            "Hardware",
            "low",
            1,
        )

        self.assertEqual(ticket["id"], "T001")


if __name__ == "__main__":
    unittest.main()