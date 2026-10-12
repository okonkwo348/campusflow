def assign_ticket(tickets, ticket_id, staff_name):
    if not isinstance(staff_name, str) or not staff_name.strip():
        raise ValueError("Staff name can not be empty")


    for ticket in tickets:
        if ticket["id"] == ticket_id:
            ticket["assigned_to"] = staff_name.strip()
            return ticket
    raise LookupError(f"Ticket {ticket_id} not found") 


def change_status(tickets, ticket_id, new_status):
    allowed_statuses = {"open", "in_progress", "resolved"}

    if new_status not in allowed_statuses:
        raise ValueError("Invalid ticket status")

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            current_status = ticket["status"]

            if current_status == new_status:
                raise ValueError("Ticket already has this status")

            if current_status == "open" and new_status == "in_progress":
                if not ticket["assigned_to"]:
                    raise ValueError("Ticket must be assigned before work begins")

            elif current_status == "open" and new_status == "resolved":
                raise ValueError("An open ticket cannot be resolved directly")

            elif current_status == "in_progress" and new_status == "open":
                raise ValueError("Reopening is only allowed from resolved status")

            elif current_status == "resolved" and new_status != "open":
                raise ValueError("Reopen the ticket before changing its status")

            elif current_status not in allowed_statuses:
                raise ValueError("Ticket has an invalid current status")

            ticket["status"] = new_status
            return ticket

    raise LookupError(f"Ticket {ticket_id} not found")   


def build_queue(tickets):
    priority_order = {
        "critical": 1,
        "high": 2,
        "medium": 3,
        "low": 4,
    }

    for ticket in tickets:
        if ticket["priority"] not in priority_order:
            raise ValueError(
                f"Invalid priority: {ticket['priority']}"
            )

    queue = [
        ticket for ticket in tickets
        if ticket["status"] != "resolved"
    ]

    queue = sorted(
        queue,
        key=lambda ticket: (
            priority_order[ticket["priority"]],
            int(ticket["id"][1:])
        )
    )

    return queue