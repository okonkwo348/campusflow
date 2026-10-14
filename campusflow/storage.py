import json
import re

from campusflow.tickets import calculate_priority


REQUIRED_KEYS = {
    "id",
    "title",
    "category",
    "urgency",
    "affected_users",
    "priority",
    "status",
    "assigned_to",
}

VALID_CATEGORIES = {"Network", "Hardware", "Software", "Other"}
VALID_URGENCIES = {"low", "medium", "high"}
VALID_PRIORITIES = {"critical", "high", "medium", "low"}
VALID_STATUSES = {"open", "in_progress", "resolved"}

NOTE_KEYS = {"note_id", "author", "message"}
MIN_NOTE_LENGTH = 5
MAX_NOTE_LENGTH = 300


def validate_notes(ticket_id: str, notes) -> None:
    """Check one ticket's notes: shape, IDs, author and message rules."""
    if not isinstance(notes, list):
        raise ValueError(f"Ticket {ticket_id}: notes must be a list.")

    seen_note_ids = set()

    for note in notes:
        if not isinstance(note, dict) or set(note.keys()) != NOTE_KEYS:
            raise ValueError(
                f"Ticket {ticket_id}: each note needs exactly "
                "note_id, author and message."
            )

        note_id = note["note_id"]
        if not isinstance(note_id, str) or not re.fullmatch(
            r"N[0-9]{3,}", note_id
        ):
            raise ValueError(
                f"Ticket {ticket_id}: note IDs must look like N001."
            )

        if note_id in seen_note_ids:
            raise ValueError(
                f"Ticket {ticket_id}: duplicate note ID {note_id}."
            )
        seen_note_ids.add(note_id)

        author = note["author"]
        if not isinstance(author, str) or not author.strip():
            raise ValueError(
                f"Ticket {ticket_id}, note {note_id}: author cannot be blank."
            )

        message = note["message"]
        if not isinstance(message, str) or not (
            MIN_NOTE_LENGTH <= len(message.strip()) <= MAX_NOTE_LENGTH
        ):
            raise ValueError(
                f"Ticket {ticket_id}, note {note_id}: message must be "
                f"{MIN_NOTE_LENGTH}-{MAX_NOTE_LENGTH} characters."
            )


def validate_tickets(tickets: list[dict]) -> None:
    """Validate ticket records and their business-rule consistency."""
    if not isinstance(tickets, list):
        raise ValueError("The saved data must be a list of tickets.")

    seen_ids = set()

    for ticket in tickets:
        if not isinstance(ticket, dict):
            raise ValueError("Every ticket must be a dictionary.")

        if set(ticket.keys()) != REQUIRED_KEYS | {"notes"}:
            raise ValueError("A ticket has missing or unexpected fields.")

        ticket_id = ticket["id"]

        if not isinstance(ticket_id, str) or not re.fullmatch(
            r"T[0-9]{3,}", ticket_id
        ):
            raise ValueError(
                "Ticket IDs must use the format T001, T002, and so on."
            )

        if ticket_id in seen_ids:
            raise ValueError(f"Duplicate ticket ID found: {ticket_id}")

        seen_ids.add(ticket_id)

        title = ticket["title"]
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Ticket titles cannot be blank.")

        if ticket["category"] not in VALID_CATEGORIES:
            raise ValueError("Invalid ticket category.")

        urgency = ticket["urgency"]
        if urgency not in VALID_URGENCIES:
            raise ValueError("Invalid ticket urgency.")

        affected_users = ticket["affected_users"]
        if (
            isinstance(affected_users, bool)
            or not isinstance(affected_users, int)
            or affected_users <= 0
        ):
            raise ValueError("affected_users must be a positive integer.")

        priority = ticket["priority"]
        if priority not in VALID_PRIORITIES:
            raise ValueError("Invalid ticket priority.")

        expected_priority = calculate_priority(urgency, affected_users)
        if priority != expected_priority:
            raise ValueError(
                f"Ticket {ticket_id} has priority '{priority}', "
                f"but its urgency and affected users require "
                f"'{expected_priority}'."
            )

        status = ticket["status"]
        if status not in VALID_STATUSES:
            raise ValueError("Invalid ticket status.")

        staff = ticket["assigned_to"]
        if staff is not None and (
            not isinstance(staff, str) or not staff.strip()
        ):
            raise ValueError("assigned_to must be a staff name or None.")

        if status == "in_progress" and staff is None:
            raise ValueError(
                f"Ticket {ticket_id} cannot be in progress without an assignee."
            )

        validate_notes(ticket_id, ticket["notes"])


def load_tickets(path: str = "tickets.json") -> list[dict]:
    """Load saved tickets, validating their structure and values."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            tickets = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON in {path}: {error}"
        ) from error

    # Migration: files saved before notes existed have no "notes" key.
    # Give those tickets an empty notes list before validating.
    if isinstance(tickets, list):
        for ticket in tickets:
            if isinstance(ticket, dict) and "notes" not in ticket:
                ticket["notes"] = []

    validate_tickets(tickets)
    return tickets


def save_tickets(
    tickets: list[dict], path: str = "tickets.json"
) -> None:
    """Validate and save tickets to a JSON file."""
    validate_tickets(tickets)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=4)
        file.write("\n")