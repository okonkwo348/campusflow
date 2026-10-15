
import unittest

from campusflow.search import search_tickets


class TestSearchTickets(unittest.TestCase):
    def setUp(self):
        self.tickets = [
            {
                "id": "T001",
                "title": "Campus Wi-Fi failure",
                "category": "Network",
                "priority": "critical",
                "status": "open",
            },
            {
                "id": "T002",
                "title": "Laptop screen broken",
                "category": "Hardware",
                "priority": "medium",
                "status": "in_progress",
            },
            {
                "id": "T003",
                "title": "Wi-Fi login problem",
                "category": "Network",
                "priority": "high",
                "status": "resolved",
            },
        ]

    def test_title_search_is_case_insensitive(self):
        result = search_tickets(self.tickets, query="WI-FI")
        self.assertEqual(
            [ticket["id"] for ticket in result],
            ["T001", "T003"],
        )

    def test_all_filters_use_and_logic(self):
        result = search_tickets(
            self.tickets,
            query="Wi-Fi",
            category="Network",
            status="open",
            priority="critical",
        )
        self.assertEqual(
            [ticket["id"] for ticket in result],
            ["T001"],
        )

    def test_empty_filters_return_all_tickets(self):
        result = search_tickets(self.tickets)
        self.assertEqual(len(result), 3)
        self.assertIsNot(result, self.tickets)

    def test_no_match_returns_empty_list(self):
        result = search_tickets(self.tickets, query="printer")
        self.assertEqual(result, [])

    def test_invalid_category_is_rejected(self):
        with self.assertRaises(ValueError):
            search_tickets(self.tickets, category="Printers")

    def test_search_does_not_mutate_tickets(self):
        original = [ticket.copy() for ticket in self.tickets]
        search_tickets(self.tickets, query="Wi-Fi")
        self.assertEqual(self.tickets, original)


if __name__ == "__main__":
    unittest.main()
