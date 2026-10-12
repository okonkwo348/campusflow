

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

VALID_STATUSES = {"open", "in_progress", "resolved"}
VALID_PRIORITIES = {"critical", "high", "medium", "low"}


def generate_report(tickets: list[dict]) -> dict:
    """Return total tickets and counts by status and priority."""
    if not isinstance(tickets, list):
        raise ValueError("Tickets must be provided as a list.")

    report = {
        "total_tickets": len(tickets),
        "by_status": {
            "open": 0,
            "in_progress": 0,
            "resolved": 0,
        },
        "by_priority": {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
        },
    }

    for ticket in tickets:
        if not isinstance(ticket, dict):
            raise ValueError("Every ticket must be a dictionary.")

        status = ticket.get("status")
        priority = ticket.get("priority")

        if status not in VALID_STATUSES:
            raise ValueError(f"Invalid ticket status: {status!r}")

        if priority not in VALID_PRIORITIES:
            raise ValueError(f"Invalid ticket priority: {priority!r}")

        report["by_status"][status] += 1
        report["by_priority"][priority] += 1

    return report

report.py
Displaying test_storage.py.