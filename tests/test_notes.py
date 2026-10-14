import json
import os
import tempfile
import unittest

from campusflow.tickets import create_ticket, add_note, get_ticket_notes
from campusflow.workflow import assign_ticket, change_status
from campusflow.storage import load_tickets, save_tickets


class TestNotes(unittest.TestCase):

    def setUp(self):
        self.tickets = []
        create_ticket(self.tickets, "Wi-Fi is down", "Network", "high", 15)

    def test_new_ticket_starts_with_empty_notes(self):
        self.assertEqual(self.tickets[0]["notes"], [])

    def test_valid_notes_get_sequential_ids(self):
        first = add_note(self.tickets, "T001", "Mentor A",
                         "Wi-Fi router reboot attempted")
        second = add_note(self.tickets, "T001", "Mentor B",
                          "Investigating switch ports")

        self.assertEqual(first["note_id"], "N001")
        self.assertEqual(second["note_id"], "N002")

    def test_note_author_and_message_are_trimmed(self):
        note = add_note(self.tickets, "T001", "  Mentor A  ",
                        "  Router rebooted  ")

        self.assertEqual(note["author"], "Mentor A")
        self.assertEqual(note["message"], "Router rebooted")

    def test_rejected_note_does_not_use_an_id(self):
        before = [dict(n) for n in self.tickets[0]["notes"]]

        for author, message in [("", "Valid message"),
                                ("Mentor A", "hi"),
                                ("Mentor A", "x" * 301)]:
            with self.assertRaises(ValueError):
                add_note(self.tickets, "T001", author, message)

        self.assertEqual(self.tickets[0]["notes"], before)

        note = add_note(self.tickets, "T001", "Mentor A", "Now a valid note")
        self.assertEqual(note["note_id"], "N001")

    def test_resolved_ticket_rejects_note_until_reopened(self):
        add_note(self.tickets, "T001", "Mentor A", "Router reboot attempted")
        assign_ticket(self.tickets, "T001", "Ada")
        change_status(self.tickets, "T001", "in_progress")
        change_status(self.tickets, "T001", "resolved")

        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "Mentor B", "Still broken here")
        self.assertEqual(len(self.tickets[0]["notes"]), 1)

        change_status(self.tickets, "T001", "open")
        note = add_note(self.tickets, "T001", "Mentor B", "Still broken here")

        self.assertEqual(note["note_id"], "N002")
        self.assertEqual(len(self.tickets[0]["notes"]), 2)

    def test_unknown_ticket_note_is_rejected(self):
        with self.assertRaises(LookupError):
            add_note(self.tickets, "T999", "Mentor A", "Valid message")

    def test_get_ticket_notes_returns_ordered_copies(self):
        add_note(self.tickets, "T001", "Mentor A", "First note text")
        add_note(self.tickets, "T001", "Mentor B", "Second note text")

        notes = get_ticket_notes(self.tickets, "T001")
        notes[0]["message"] = "changed by caller"

        self.assertEqual([n["note_id"] for n in notes], ["N001", "N002"])
        self.assertEqual(self.tickets[0]["notes"][0]["message"],
                         "First note text")


class TestNoteStorage(unittest.TestCase):

    def test_notes_and_next_note_id_survive_save_and_load(self):
        tickets = []
        create_ticket(tickets, "Wi-Fi is down", "Network", "high", 15)
        add_note(tickets, "T001", "Mentor A", "Router reboot attempted")

        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "tickets.json")
            save_tickets(tickets, path)
            reloaded = load_tickets(path)

        self.assertEqual(reloaded, tickets)
        note = add_note(reloaded, "T001", "Mentor B", "Checking switch ports")
        self.assertEqual(note["note_id"], "N002")

    def test_old_file_without_notes_loads_with_empty_notes(self):
        old_ticket = {
            "id": "T001", "title": "Wi-Fi is down", "category": "Network",
            "urgency": "high", "affected_users": 15, "priority": "critical",
            "status": "open", "assigned_to": None,
        }
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "tickets.json")
            with open(path, "w", encoding="utf-8") as file:
                json.dump([old_ticket], file)

            self.assertEqual(load_tickets(path)[0]["notes"], [])

    def test_duplicate_note_ids_reject_the_load(self):
        bad_ticket = {
            "id": "T001", "title": "Wi-Fi is down", "category": "Network",
            "urgency": "high", "affected_users": 15, "priority": "critical",
            "status": "open", "assigned_to": None,
            "notes": [
                {"note_id": "N001", "author": "A", "message": "First note"},
                {"note_id": "N001", "author": "B", "message": "Second note"},
            ],
        }
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "tickets.json")
            with open(path, "w", encoding="utf-8") as file:
                json.dump([bad_ticket], file)

            with self.assertRaises(ValueError):
                load_tickets(path)

    def test_new_ticket_after_reload_gets_next_id(self):
        tickets = []
        create_ticket(tickets, "Wi-Fi is down", "Network", "high", 15)
        create_ticket(tickets, "Broken laptop", "Hardware", "low", 1)

        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "tickets.json")
            save_tickets(tickets, path)
            reloaded = load_tickets(path)

        new_ticket = create_ticket(reloaded, "Printer jam", "Hardware", "low", 1)
        self.assertEqual(new_ticket["id"], "T003")

if __name__ == "__main__":
    unittest.main()