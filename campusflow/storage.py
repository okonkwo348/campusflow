
import json


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


def load_tickets(path: str = "tickets.json") -> list[dict]:
    """Load and validate the saved ticket list."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            tickets = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON in {path}: {error}"
        ) from error

    if not isinstance(tickets, list):
        raise ValueError("The saved data must be a list of tickets.")

    seen_ids = set()

    for ticket in tickets:
        if not isinstance(ticket, dict):
            raise ValueError("Every ticket must be a dictionary.")

        if set(ticket.keys()) != REQUIRED_KEYS:
            raise ValueError("A ticket has missing or unexpected fields.")

        if not isinstance(ticket["id"], str) or not ticket["id"]:
            raise ValueError("Every ticket must have a valid ID.")

        if ticket["id"] in seen_ids:
            raise ValueError("Duplicate ticket IDs found.")

        seen_ids.add(ticket["id"])

        if not isinstance(ticket["title"], str) or not ticket["title"].strip():
            raise ValueError("Ticket titles cannot be blank.")

        if ticket["category"] not in {"Network", "Hardware", "Software", "Other"}:
            raise ValueError("Invalid ticket category.")

        if ticket["urgency"] not in {"low", "medium", "high"}:
            raise ValueError("Invalid ticket urgency.")

        if (
            not isinstance(ticket["affected_users"], int)
            or isinstance(ticket["affected_users"], bool)
            or ticket["affected_users"] <= 0
        ):
            raise ValueError("affected_users must be a positive integer.")

        if ticket["priority"] not in {"critical", "high", "medium", "low"}:
            raise ValueError("Invalid ticket priority.")

        if ticket["status"] not in {"open", "in_progress", "resolved"}:
            raise ValueError("Invalid ticket status.")

        staff = ticket["assigned_to"]
        if staff is not None and (
            not isinstance(staff, str) or not staff.strip()
        ):
            raise ValueError("assigned_to must be a staff name or None.")

    return tickets


def save_tickets(tickets: list[dict], path: str = "tickets.json") -> None:
    """Save tickets to a JSON file."""
    with open(path, "w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=4)
