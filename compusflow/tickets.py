VALID_CATEGORIES = {"Network", "Hardware", "Software", "Other"}
VALID_URGENCIES = {"low", "medium", "high"}


def validate_title(title: str) -> str:
    """Return a trimmed, non-empty title."""
    if not isinstance(title, str):
        raise ValueError("Title must be a string.")

    title = title.strip()

    if not title:
        raise ValueError("Title must not be blank. Enter a problem.")
 
    return title


def validate_category(category: str) -> str:
    """Validate and normalize a ticket category."""
    if not isinstance(category, str):
        raise ValueError("Category must be a string.")

    category = category.strip().lower()

    categories = {value.lower(): value for value in VALID_CATEGORIES}

    if category not in categories:
        raise ValueError(
            "Invalid category. Choose Network, Hardware, Software, or Other."
        )

    return categories[category]


def validate_urgency(urgency: str) -> str:
    """Validate and normalize urgency."""
    if not isinstance(urgency, str):
        raise ValueError("Urgency must be a string.")

    urgency = urgency.strip().lower()

    if urgency not in VALID_URGENCIES:
        raise ValueError("Invalid urgency. Choose low, medium, or high.")

    return urgency


def validate_affected_users(count: int) -> int:
    """Require a positive integer, excluding booleans."""
    if isinstance(count, bool) or not isinstance(count, int):
        raise ValueError("Affected users must be a whole number.")

    if count <= 0:
        raise ValueError("Affected users must be greater than zero.")

    return count



def calculate_priority(urgency: str, affected_users: int) -> str:
    """Return priority based on validated urgency and user count."""
    urgency = validate_urgency(urgency)
    affected_users = validate_affected_users(affected_users)

    if urgency == "high" and affected_users >= 10:
        return "critical"

    if urgency == "high" or affected_users >= 10:
        return "high"

    if urgency == "medium" or affected_users >= 3:
        return "medium"

    return "low"



def generate_ticket_id(tickets: list[dict]) -> str:
    """Generate the next ID using the highest existing numeric ID."""
    highest_id = 0

    for ticket in tickets:
        ticket_id = ticket.get("id", "")

        if (
            isinstance(ticket_id, str)
            and ticket_id.startswith("T")
            and ticket_id[1:].isdigit()
        ):
            highest_id = max(highest_id, int(ticket_id[1:]))

    return f"T{highest_id + 1:03d}"


def find_ticket(tickets: list[dict], ticket_id: str) -> dict:
    """Return a ticket by ID or raise LookupError."""
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket

    raise LookupError(f"Ticket '{ticket_id}' not found.")

