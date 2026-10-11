def generate_report(tickets: list[dict]) -> dict:
    """Return totals and counts by status and priority."""
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
        report["by_status"][ticket["status"]] += 1
        report["by_priority"][ticket["priority"]] += 1

    return report