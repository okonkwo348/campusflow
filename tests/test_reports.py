

Skip to content
Using Gmail with screen readers
1 of 1,167
main and report
Inbox
Emmanuel Okonkwo <okonkwopaul348@gmail.com>
	
Attachments11:50 AM (51 minutes ago)
	
	
to me

 4 Attachments
  •  Scanned by Gmail

import unittest

from campusflow.reports import generate_report


SAMPLE_TICKET = {
    "id": "T001",
    "title": "Campus Wi-Fi is down",
    "category": "Network",
    "urgency": "high",
    "affected_users": 15,
    "priority": "critical",
    "status": "open",
    "assigned_to": None,
}


class ReportTests(unittest.TestCase):

    def test_report_counts_single_ticket(self):
        report = generate_report([SAMPLE_TICKET])

        self.assertEqual(report["total_tickets"], 1)
        self.assertEqual(report["by_status"]["open"], 1)
        self.assertEqual(report["by_priority"]["critical"], 1)

    def test_empty_report_has_all_zero_counts(self):
        report = generate_report([])

        self.assertEqual(report["total_tickets"], 0)

        self.assertEqual(
            report["by_status"],
            {
                "open": 0,
                "in_progress": 0,
                "resolved": 0,
            },
        )

        self.assertEqual(
            report["by_priority"],
            {
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
            },
        )

    def test_report_counts_mixed_tickets(self):
        second_ticket = {
            **SAMPLE_TICKET,
            "id": "T002",
            "title": "Laptop issue",
            "category": "Hardware",
            "urgency": "low",
            "affected_users": 1,
            "priority": "low",
            "status": "resolved",
            "assigned_to": "Alex",
        }

        third_ticket = {
            **SAMPLE_TICKET,
            "id": "T003",
            "title": "Software installation issue",
            "category": "Software",
            "urgency": "medium",
            "affected_users": 4,
            "priority": "medium",
            "status": "in_progress",
            "assigned_to": "Jordan",
        }

        report = generate_report(
            [SAMPLE_TICKET, second_ticket, third_ticket]
        )

        self.assertEqual(report["total_tickets"], 3)

        self.assertEqual(
            report["by_status"],
            {
                "open": 1,
                "in_progress": 1,
                "resolved": 1,
            },
        )

        self.assertEqual(
            report["by_priority"],
            {
                "critical": 1,
                "high": 0,
                "medium": 1,
                "low": 1,
            },
        )

    def test_invalid_status_raises_value_error(self):
        invalid_ticket = {
            **SAMPLE_TICKET,
            "status": "pending",
        }

        with self.assertRaises(ValueError):
            generate_report([invalid_ticket])

    def test_invalid_priority_raises_value_error(self):
        invalid_ticket = {
            **SAMPLE_TICKET,
            "priority": "urgent",
        }

        with self.assertRaises(ValueError):
            generate_report([invalid_ticket])

    def test_non_dictionary_ticket_raises_value_error(self):
        with self.assertRaises(ValueError):
            generate_report(["not a ticket"])

    def test_non_list_input_raises_value_error(self):
        with self.assertRaises(ValueError):
            generate_report(None)


if __name__ == "__main__":
    unittest.main()

test_report.py
Displaying main.py.