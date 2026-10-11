import unittest

from campusflow.tickets import (
    assign_ticket,
    build_ticket_report,
    calculate_priority,
    create_ticket,
    get_work_queue,
    reopen_ticket,
    update_ticket_status,
)

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


class AssignTicketTests(unittest.TestCase):
    def setUp(self):
        self.tickets = []
        self.ticket = create_ticket(
            self.tickets,
            "Wi-Fi unavailable in library",
            "Network",
            "high",
            12,
        )

    def test_assign_ticket_stores_cleaned_staff_name(self):
        updated_ticket = assign_ticket(self.tickets, "T001", " Ada Lovelace ")

        self.assertIs(updated_ticket, self.ticket)
        self.assertEqual(updated_ticket["assigned_to"], "Ada Lovelace")
        self.assertEqual(updated_ticket["status"], "open")

    def test_blank_staff_name_is_rejected(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", "   ")

    def test_unknown_ticket_id_is_rejected(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T999", "Ada Lovelace")


class StatusWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tickets = []
        self.ticket = create_ticket(
            self.tickets,
            "Projector will not turn on",
            "Hardware",
            "medium",
            5,
        )

    def start_work(self):
        assign_ticket(self.tickets, "T001", "Ada Lovelace")
        return update_ticket_status(self.tickets, "T001", "in_progress")

    def test_open_ticket_requires_assignment_before_work_can_start(self):
        with self.assertRaises(ValueError):
            update_ticket_status(self.tickets, "T001", "in_progress")

    def test_assigned_open_ticket_can_move_to_in_progress(self):
        updated_ticket = self.start_work()

        self.assertIs(updated_ticket, self.ticket)
        self.assertEqual(updated_ticket["status"], "in_progress")

    def test_in_progress_ticket_can_move_to_resolved(self):
        self.start_work()

        updated_ticket = update_ticket_status(self.tickets, "T001", "resolved")

        self.assertEqual(updated_ticket["status"], "resolved")

    def test_resolved_ticket_can_be_explicitly_reopened_to_open(self):
        self.start_work()
        update_ticket_status(self.tickets, "T001", "resolved")

        updated_ticket = reopen_ticket(self.tickets, "T001")

        self.assertEqual(updated_ticket["status"], "open")

    def test_resolved_ticket_cannot_move_directly_to_in_progress(self):
        self.start_work()
        update_ticket_status(self.tickets, "T001", "resolved")

        with self.assertRaises(ValueError):
            update_ticket_status(self.tickets, "T001", "in_progress")

    def test_open_ticket_cannot_skip_to_resolved(self):
        with self.assertRaises(ValueError):
            update_ticket_status(self.tickets, "T001", "resolved")

    def test_only_resolved_ticket_can_be_reopened(self):
        with self.assertRaises(ValueError):
            reopen_ticket(self.tickets, "T001")


    def test_invalid_status_is_rejected(self):
        with self.assertRaises(ValueError):
            update_ticket_status(self.tickets, "T001", "paused")


class WorkQueueTests(unittest.TestCase):
    def setUp(self):
        self.tickets = []

        self.low_ticket = create_ticket(
            self.tickets,
            "Replace mouse batteries",
            "Hardware",
            "low",
            1,
        )
        self.in_progress_ticket = create_ticket(
            self.tickets,
            "Lecture hall Wi-Fi is unstable",
            "Network",
            "high",
            2,
        )
        self.critical_ticket = create_ticket(
            self.tickets,
            "Campus network outage",
            "Network",
            "high",
            50,
        )
        self.resolved_ticket = create_ticket(
            self.tickets,
            "Install approved software",
            "Software",
            "medium",
            2,
        )

        assign_ticket(self.tickets, "T002", "Ada Lovelace")
        update_ticket_status(self.tickets, "T002", "in_progress")
        assign_ticket(self.tickets, "T004", "Ada Lovelace")
        update_ticket_status(self.tickets, "T004", "in_progress")
        update_ticket_status(self.tickets, "T004", "resolved")

    def test_work_queue_lists_only_open_tickets_by_priority(self):
        queue = get_work_queue(self.tickets)

        self.assertEqual(
            [ticket["id"] for ticket in queue],
            ["T003", "T001"],
        )

    def test_work_queue_uses_numeric_ticket_id_as_tie_breaker(self):
        tickets = [
            {"id": "T010", "priority": "high", "status": "open"},
            {"id": "T002", "priority": "high", "status": "open"},
        ]

        queue = get_work_queue(tickets)

        self.assertEqual([ticket["id"] for ticket in queue], ["T002", "T010"])

class TicketReportTests(unittest.TestCase):
    def setUp(self):
        self.tickets = []

        create_ticket(
            self.tickets,
            "Replace mouse batteries",
            "Hardware",
            "low",
            1,
        )
        high_ticket = create_ticket(
            self.tickets,
            "Lecture hall Wi-Fi is unstable",
            "Network",
            "high",
            2,
        )
        create_ticket(
            self.tickets,
            "Campus network outage",
            "Network",
            "high",
            50,
        )
        resolved_ticket = create_ticket(
            self.tickets,
            "Install approved software",
            "Software",
            "medium",
            2,
        )

        assign_ticket(self.tickets, high_ticket["id"], "Ada Lovelace")
        assign_ticket(self.tickets, resolved_ticket["id"], "Grace Hopper")
        update_ticket_status(
            self.tickets,
            resolved_ticket["id"],
            "in_progress",
        )
        update_ticket_status(
            self.tickets,
            resolved_ticket["id"],
            "resolved",
        )

    def test_report_summarises_tickets(self):
        report = build_ticket_report(self.tickets)

        self.assertEqual(report["total"], 4)
        self.assertEqual(
            report["by_status"],
            {
                "open": 3,
                "in_progress": 0,
                "resolved": 1,
            },
        )
        self.assertEqual(
            report["by_priority"],
            {
                "critical": 1,
                "high": 1,
                "medium": 1,
                "low": 1,
            },
        )
        self.assertEqual(report["assigned"], 2)
        self.assertEqual(report["unassigned"], 2)

if __name__ == "__main__":
    unittest.main()
