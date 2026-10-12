

Skip to content
Using Gmail with screen readers
2 of 1,167
storage
Inbox
Emmanuel Okonkwo <okonkwopaul348@gmail.com>
	
Attachments11:38 AM (1 hour ago)
	
	
to me

 3 Attachments
  •  Scanned by Gmail

import json
import os
import tempfile
import unittest

from campusflow.storage import load_tickets, save_tickets
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


class StorageTests(unittest.TestCase):

    def write_tickets(self, folder, tickets):
        """Write ticket data directly to a JSON file for testing."""
        path = os.path.join(folder, "tickets.json")
        with open(path, "w", encoding="utf-8") as file:
            json.dump(tickets, file)
        return path

    def test_save_and_load(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "tickets.json")

            save_tickets([SAMPLE_TICKET], path)

            self.assertEqual(load_tickets(path), [SAMPLE_TICKET])

    def test_missing_file_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "missing.json")

            self.assertEqual(load_tickets(path), [])

    def test_malformed_json_raises_value_error(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "tickets.json")

            with open(path, "w", encoding="utf-8") as file:
                file.write("{invalid json")

            with self.assertRaises(ValueError):
                load_tickets(path)

    def test_non_list_json_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = self.write_tickets(folder, {"ticket": SAMPLE_TICKET})

            with self.assertRaises(ValueError):
                load_tickets(path)

    def test_non_dictionary_ticket_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = self.write_tickets(folder, ["not a ticket"])

            with self.assertRaises(ValueError):
                load_tickets(path)

    def test_missing_ticket_field_is_rejected(self):
        invalid_ticket = SAMPLE_TICKET.copy()
        del invalid_ticket["title"]

        with tempfile.TemporaryDirectory() as folder:
            path = self.write_tickets(folder, [invalid_ticket])

            with self.assertRaises(ValueError):
                load_tickets(path)

    def test_unexpected_ticket_field_is_rejected(self):
        invalid_ticket = {
            **SAMPLE_TICKET,
            "extra_field": "unexpected",
        }

        with tempfile.TemporaryDirectory() as folder:
            path = self.write_tickets(folder, [invalid_ticket])

            with self.assertRaises(ValueError):
                load_tickets(path)

    def test_duplicate_ids_are_rejected(self):
        duplicate_ticket = SAMPLE_TICKET.copy()

        with tempfile.TemporaryDirectory() as folder:
            path = self.write_tickets(
                folder, [SAMPLE_TICKET, duplicate_ticket]
            )

            with self.assertRaises(ValueError):
                load_tickets(path)

    def test_invalid_ticket_id_is_rejected(self):
        invalid_ticket = SAMPLE_TICKET.copy()
        invalid_ticket["id"] = "hello"

        with tempfile.TemporaryDirectory() as folder:
            path = self.write_tickets(folder, [invalid_ticket])

            with self.assertRaises(ValueError):
                load_tickets(path)

    def test_blank_title_is_rejected(self):
        invalid_ticket = SAMPLE_TICKET.copy()
        invalid_ticket["title"] = "   "

        with tempfile.TemporaryDirectory() as folder:
            path = self.write_tickets(folder, [invalid_ticket])

            with self.assertRaises(ValueError):
                load_tickets(path)

    def test_invalid_category_is_rejected(self):
        invalid_ticket = SAMPLE_TICKET.copy()
        invalid_ticket["category"] = "Finance"

        with tempfile.TemporaryDirectory() as folder:
            path = self.write_tickets(folder, [invalid_ticket])

            with self.assertRaises(ValueError):
                load_tickets(path)

    def test_invalid_urgency_is_rejected(self):
        invalid_ticket = SAMPLE_TICKET.copy()
        invalid_ticket["urgency"] = "urgent"

        with tempfile.TemporaryDirectory() as folder:
            path = self.write_tickets(folder, [invalid_ticket])

            with self.assertRaises(ValueError):
                load_tickets(path)

    def test_invalid_affected_users_is_rejected(self):
        invalid_ticket = SAMPLE_TICKET.copy()
        invalid_ticket["affected_users"] = True

        with tempfile.TemporaryDirectory() as folder:
            path = self.write_tickets(folder, [invalid_ticket])

            with self.assertRaises(ValueError):
                load_tickets(path)

    def test_invalid_priority_is_rejected(self):
        invalid_ticket = SAMPLE_TICKET.copy()
        invalid_ticket["priority"] = "low"

        with tempfile.TemporaryDirectory() as folder:
            path = self.write_tickets(folder, [invalid_ticket])

            with self.assertRaises(ValueError):
                load_tickets(path)

    def test_invalid_status_is_rejected(self):
        invalid_ticket = SAMPLE_TICKET.copy()
        invalid_ticket["status"] = "pending"

        with tempfile.TemporaryDirectory() as folder:
            path = self.write_tickets(folder, [invalid_ticket])

            with self.assertRaises(ValueError):
                load_tickets(path)

    def test_invalid_assignee_is_rejected(self):
        invalid_ticket = SAMPLE_TICKET.copy()
        invalid_ticket["assigned_to"] = "   "

        with tempfile.TemporaryDirectory() as folder:
            path = self.write_tickets(folder, [invalid_ticket])

            with self.assertRaises(ValueError):
                load_tickets(path)

    def test_unassigned_in_progress_ticket_is_rejected(self):
        invalid_ticket = SAMPLE_TICKET.copy()
        invalid_ticket["status"] = "in_progress"
        invalid_ticket["assigned_to"] = None

        with tempfile.TemporaryDirectory() as folder:
            path = self.write_tickets(folder, [invalid_ticket])

            with self.assertRaises(ValueError):
                load_tickets(path)

    def test_save_rejects_invalid_tickets(self):
        invalid_ticket = SAMPLE_TICKET.copy()
        invalid_ticket["priority"] = "low"

        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "tickets.json")

            with self.assertRaises(ValueError):
                save_tickets([invalid_ticket], path)

            self.assertFalse(os.path.exists(path))


class ReportTests(unittest.TestCase):

    def test_report_counts_tickets(self):
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
            "title": "Old laptop needs replacement",
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


if __name__ == "__main__":
    unittest.main()

test_storage.py
Displaying test_storage.py.