
VALID_CATEGORIES = {"Network", "Hardware", "Software", "Other"}
VALID_STATUSES = {"open", "in_progress", "resolved"}
VALID_PRIORITIES = {"critical", "high", "medium", "low"}


def search_tickets(
    tickets,
    query="",
    category=None,
    status=None,
    priority=None,
):
    if category is not None and category not in VALID_CATEGORIES:
        raise ValueError("Invalid category.")

    if status is not None and status not in VALID_STATUSES:
        raise ValueError("Invalid status.")

    if priority is not None and priority not in VALID_PRIORITIES:
        raise ValueError("Invalid priority.")

    query = query.strip().casefold()
    results = []

    for ticket in tickets:
        if query and query not in ticket["title"].casefold():
            continue

        if category is not None and ticket["category"] != category:
            continue

        if status is not None and ticket["status"] != status:
            continue

        if priority is not None and ticket["priority"] != priority:
            continue

        results.append(ticket)

    return results
