
import unittest

from campusflow.workflow import assign_ticket, change_status, build_queue


class TestWorkflow(unittest.TestCase):

    def setUp(self):
        self.tickets = [
            {
                "id": "T001",
                "title": "Wi-Fi is down",
                "category": "Network",
                "urgency": "high",
                "affected_users": 15,
                "priority": "critical",
                "status": "open",
                "assigned_to": None,
            }
        ]

    # -------------------------
    # Assignment tests
    # -------------------------

    def test_assign_ticket_successfully(self):
        ticket = assign_ticket(self.tickets, "T001", "Mary")

        self.assertEqual(ticket["assigned_to"], "Mary")

    def test_assign_ticket_trims_staff_name(self):
        ticket = assign_ticket(self.tickets, "T001", "  Mary  ")

        self.assertEqual(ticket["assigned_to"], "Mary")

    def test_blank_staff_name_is_rejected(self):
        original_ticket = self.tickets[0].copy()

        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", "   ")

        self.assertEqual(self.tickets[0], original_ticket)

    def test_unknown_ticket_assignment_is_rejected(self):
        with self.assertRaises(LookupError):
            assign_ticket(self.tickets, "T999", "Mary")

    # -------------------------
    # Status transition tests
    # -------------------------

    def test_assigned_ticket_can_enter_progress(self):
        self.tickets[0]["assigned_to"] = "Mary"

        ticket = change_status(self.tickets, "T001", "in_progress")

        self.assertEqual(ticket["status"], "in_progress")

    def test_unassigned_ticket_cannot_enter_progress(self):
        original_ticket = self.tickets[0].copy()

        with self.assertRaises(ValueError):
            change_status(self.tickets, "T001", "in_progress")

        self.assertEqual(self.tickets[0], original_ticket)

    def test_open_ticket_cannot_be_resolved_directly(self):
        original_ticket = self.tickets[0].copy()

        with self.assertRaises(ValueError):
            change_status(self.tickets, "T001", "resolved")

        self.assertEqual(self.tickets[0], original_ticket)

    def test_in_progress_ticket_can_be_resolved(self):
        self.tickets[0]["assigned_to"] = "Alice"
        self.tickets[0]["status"] = "in_progress"

        ticket = change_status(self.tickets, "T001", "resolved")

        self.assertEqual(ticket["status"], "resolved")

    def test_resolved_ticket_must_be_reopened_first(self):
        self.tickets[0]["status"] = "resolved"

        with self.assertRaises(ValueError):
            change_status(self.tickets, "T001", "in_progress")

        ticket = change_status(self.tickets, "T001", "open")

        self.assertEqual(ticket["status"], "open")

    def test_in_progress_ticket_cannot_return_directly_to_open(self):
        self.tickets[0]["assigned_to"] = "Alice"
        self.tickets[0]["status"] = "in_progress"
        original_ticket = self.tickets[0].copy()

        with self.assertRaises(ValueError):
            change_status(self.tickets, "T001", "open")

        self.assertEqual(self.tickets[0], original_ticket)

    def test_same_status_transition_is_rejected(self):
        original_ticket = self.tickets[0].copy()

        with self.assertRaises(ValueError):
            change_status(self.tickets, "T001", "open")

        self.assertEqual(self.tickets[0], original_ticket)

    def test_invalid_new_status_is_rejected(self):
        original_ticket = self.tickets[0].copy()

        with self.assertRaises(ValueError):
            change_status(self.tickets, "T001", "pending")

        self.assertEqual(self.tickets[0], original_ticket)

    def test_unknown_ticket_status_change_is_rejected(self):
        with self.assertRaises(LookupError):
            change_status(self.tickets, "T999", "open")

    # -------------------------
    # Work queue tests
    # -------------------------

    def test_build_queue_orders_by_priority(self):
        self.tickets.extend([
            {
                "id": "T003",
                "title": "Slow internet",
                "category": "Network",
                "urgency": "medium",
                "affected_users": 5,
                "priority": "medium",
                "status": "open",
                "assigned_to": None,
            },
            {
                "id": "T002",
                "title": "Server down",
                "category": "Network",
                "urgency": "high",
                "affected_users": 20,
                "priority": "critical",
                "status": "open",
                "assigned_to": None,
            },
        ])

        queue = build_queue(self.tickets)

        self.assertEqual(
            [ticket["id"] for ticket in queue],
            ["T001", "T002", "T003"],
        )

    def test_build_queue_breaks_priority_ties_by_numeric_id(self):
        # Keep the ticket data consistent with the priority rules.
        self.tickets[0]["affected_users"] = 2
        self.tickets[0]["priority"] = "high"

        self.tickets.extend([
            {
                "id": "T004",
                "title": "Printer issue",
                "category": "Hardware",
                "urgency": "high",
                "affected_users": 2,
                "priority": "high",
                "status": "open",
                "assigned_to": None,
            },
            {
                "id": "T002",
                "title": "Email issue",
                "category": "Network",
                "urgency": "high",
                "affected_users": 2,
                "priority": "high",
                "status": "open",
                "assigned_to": None,
            },
        ])

        queue = build_queue(self.tickets)

        self.assertEqual(
            [ticket["id"] for ticket in queue],
            ["T001", "T002", "T004"],
        )

    def test_queue_sorts_ticket_ids_numerically(self):
        self.tickets[0]["id"] = "T010"
        self.tickets[0]["affected_users"] = 2
        self.tickets[0]["priority"] = "high"

        self.tickets.append({
            "id": "T002",
            "title": "Printer issue",
            "category": "Hardware",
            "urgency": "high",
            "affected_users": 2,
            "priority": "high",
            "status": "open",
            "assigned_to": None,
        })

        queue = build_queue(self.tickets)

        self.assertEqual(
            [ticket["id"] for ticket in queue],
            ["T002", "T010"],
        )

    def test_build_queue_excludes_resolved_tickets(self):
        self.tickets[0]["status"] = "resolved"

        queue = build_queue(self.tickets)

        self.assertEqual(queue, [])

    def test_build_queue_excludes_resolved_but_keeps_active_tickets(self):
        self.tickets[0]["status"] = "resolved"

        self.tickets.append({
            "id": "T002",
            "title": "Software issue",
            "category": "Software",
            "urgency": "low",
            "affected_users": 1,
            "priority": "low",
            "status": "open",
            "assigned_to": None,
        })

        queue = build_queue(self.tickets)

        self.assertEqual(
            [ticket["id"] for ticket in queue],
            ["T002"],
        )

    def test_build_queue_does_not_modify_original_list_order(self):
        self.tickets.extend([
            {
                "id": "T003",
                "title": "Slow internet",
                "category": "Network",
                "urgency": "low",
                "affected_users": 1,
                "priority": "low",
                "status": "open",
                "assigned_to": None,
            },
            {
                "id": "T002",
                "title": "Server down",
                "category": "Network",
                "urgency": "high",
                "affected_users": 2,
                "priority": "high",
                "status": "open",
                "assigned_to": None,
            },
        ])

        original_ids = [ticket["id"] for ticket in self.tickets]

        build_queue(self.tickets)

        self.assertEqual(
            [ticket["id"] for ticket in self.tickets],
            original_ids,
        )

    def test_build_queue_empty_list(self):
        self.assertEqual(build_queue([]), [])

    def test_build_queue_rejects_invalid_priority(self):
        self.tickets[0]["priority"] = "urgent"

        with self.assertRaises(ValueError):
            build_queue(self.tickets)

    def test_build_queue_rejects_invalid_status(self):
        self.tickets[0]["status"] = "pending"

        with self.assertRaises(ValueError):
            build_queue(self.tickets)

    def test_build_queue_rejects_invalid_ticket_id(self):
        self.tickets[0]["id"] = "invalid"

        with self.assertRaises(ValueError):
            build_queue(self.tickets)


if __name__ == "__main__":
    unittest.main()
