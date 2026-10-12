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


def validate_tickets(tickets: list[dict]) -> None:
    """Validate ticket records and their business-rule consistency."""
    if not isinstance(tickets, list):
        raise ValueError("The saved data must be a list of tickets.")

    seen_ids = set()

    for ticket in tickets:
        if not isinstance(ticket, dict):
            raise ValueError("Every ticket must be a dictionary.")

        if set(ticket.keys()) != REQUIRED_KEYS:
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
