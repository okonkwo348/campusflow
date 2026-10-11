
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

    def test_duplicate_ids_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "tickets.json")
            with open(path, "w", encoding="utf-8") as file:
                json.dump([SAMPLE_TICKET, SAMPLE_TICKET], file)
            with self.assertRaises(ValueError):
                load_tickets(path)


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
            {"open": 0, "in_progress": 0, "resolved": 0},
        )
        self.assertEqual(
            report["by_priority"],
            {"critical": 0, "high": 0, "medium": 0, "low": 0},
        )


if __name__ == "__main__":
    unittest.main()
