import re


VALID_STATUSES = {"open", "in_progress", "resolved"}

PRIORITY_ORDER = {
    "critical": 1,
    "high": 2,
    "medium": 3,
    "low": 4,
}


def assign_ticket(
    tickets: list[dict],
    ticket_id: str,
    staff_name: str,
) -> dict:
    """Assign a ticket to a staff member.

    A resolved ticket cannot be assigned or reassigned until it is
    explicitly reopened. All checks run before the ticket is changed.
    """
    if not isinstance(staff_name, str) or not staff_name.strip():
        raise ValueError("Staff name cannot be empty.")

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            if ticket["status"] == "resolved":
                raise ValueError(
                    f"Ticket {ticket_id} is resolved. "
                    "Reopen it before assigning it."
                )
            ticket["assigned_to"] = staff_name.strip()
            return ticket

    raise LookupError(f"Ticket '{ticket_id}' not found.")


def change_status(
    tickets: list[dict],
    ticket_id: str,
    new_status: str,
) -> dict:
    """Change a ticket's status using the allowed workflow transitions."""
    if not isinstance(new_status, str) or new_status not in VALID_STATUSES:
        raise ValueError("Invalid ticket status.")

    for ticket in tickets:
        if ticket["id"] != ticket_id:
            continue

        current_status = ticket["status"]

        if current_status not in VALID_STATUSES:
            raise ValueError("Ticket has an invalid current status.")

        if current_status == new_status:
            raise ValueError("Ticket already has this status.")

        allowed_transitions = {
            "open": {"in_progress"},
            "in_progress": {"resolved"},
            "resolved": {"open"},
        }

        if new_status not in allowed_transitions[current_status]:
            raise ValueError(
                f"Cannot change ticket status from "
                f"'{current_status}' to '{new_status}'."
            )

        if new_status == "in_progress" and not ticket["assigned_to"]:
            raise ValueError(
                "Ticket must be assigned before work begins."
            )

        ticket["status"] = new_status
        return ticket

    raise LookupError(f"Ticket '{ticket_id}' not found.")


def build_queue(tickets: list[dict]) -> list[dict]:
    """Return the Open Work Queue: only OPEN tickets, most urgent first.

    Sorted by priority (critical, high, medium, low), then numeric ticket
    ID. in_progress and resolved tickets are excluded. Returns a new list;
    the original collection is not modified or reordered.
    """
    for ticket in tickets:
        if ticket["status"] not in VALID_STATUSES:
            raise ValueError(
                f"Invalid ticket status: {ticket['status']}"
            )

        if ticket["priority"] not in PRIORITY_ORDER:
            raise ValueError(
                f"Invalid ticket priority: {ticket['priority']}"
            )

        ticket_id = ticket["id"]

        if not isinstance(ticket_id, str) or not re.fullmatch(
            r"T[0-9]{3,}", ticket_id
        ):
            raise ValueError(f"Invalid ticket ID: {ticket_id!r}")

    queue = [
        ticket
        for ticket in tickets
        if ticket["status"] == "open"
    ]

    return sorted(
        queue,
        key=lambda ticket: (
            PRIORITY_ORDER[ticket["priority"]],
            int(ticket["id"][1:]),
        ),
    )