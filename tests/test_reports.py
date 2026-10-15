
import unittest

from campusflow.reports import generate_report


class TestGenerateReport(unittest.TestCase):
    def test_empty_report_contains_all_keys(self):
        report = generate_report([])

        self.assertEqual(report["total_tickets"], 0)
        self.assertEqual(report["unresolved"], 0)
        self.assertEqual(report["resolved"], 0)
        self.assertEqual(report["resolution_percentage"], 0.0)

        self.assertEqual(
            set(report["by_status"]),
            {"open", "in_progress", "resolved"},
        )
        self.assertEqual(
            set(report["by_priority"]),
            {"critical", "high", "medium", "low"},
        )
        self.assertEqual(
            set(report["by_category"]),
            {"Network", "Hardware", "Software", "Other"},
        )

    def test_counts_and_resolution_percentage(self):
        tickets = [
            {
                "status": "resolved",
                "priority": "critical",
                "category": "Network",
            },
            {
                "status": "open",
                "priority": "high",
                "category": "Hardware",
            },
            {
                "status": "in_progress",
                "priority": "medium",
                "category": "Software",
            },
            {
                "status": "resolved",
                "priority": "low",
                "category": "Other",
            },
        ]

        report = generate_report(tickets)

        self.assertEqual(report["total_tickets"], 4)
        self.assertEqual(report["resolved"], 2)
        self.assertEqual(report["unresolved"], 2)
        self.assertEqual(report["resolution_percentage"], 50.0)
        self.assertEqual(report["by_status"]["open"], 1)
        self.assertEqual(report["by_status"]["in_progress"], 1)
        self.assertEqual(report["by_status"]["resolved"], 2)


if __name__ == "__main__":
    unittest.main()
