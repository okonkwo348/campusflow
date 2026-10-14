
STATUSES = ("open", "in_progress", "resolved")
PRIORITIES = ("critical", "high", "medium", "low")
CATEGORIES = ("Network", "Hardware", "Software", "Other")


def generate_report(tickets):
    report = {
        "total_tickets": len(tickets),
        "by_status": {status: 0 for status in STATUSES},
        "by_priority": {priority: 0 for priority in PRIORITIES},
        "by_category": {category: 0 for category in CATEGORIES},
        "unresolved": 0,
        "resolved": 0,
        "resolution_percentage": 0.0,
    }

    for ticket in tickets:
        report["by_status"][ticket["status"]] += 1
        report["by_priority"][ticket["priority"]] += 1
        report["by_category"][ticket["category"]] += 1

        if ticket["status"] == "resolved":
            report["resolved"] += 1
        else:
            report["unresolved"] += 1

    if report["total_tickets"] > 0:
        report["resolution_percentage"] = (
            report["resolved"] / report["total_tickets"]
        ) * 100

    return report
