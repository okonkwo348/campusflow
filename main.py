from campusflow.tickets import create_ticket
from campusflow.workflow import assign_ticket, change_status, build_queue
from campusflow.storage import load_tickets, save_tickets
from campusflow.reports import generate_report


def display_tickets(tickets: list[dict]) -> None:
    """Display ticket summaries."""
    if not tickets:
        print("No tickets found.")
        return

    for ticket in tickets:
        print(
            f'{ticket["id"]}: {ticket["title"]} | '
            f'Category: {ticket["category"]} | '
            f'Priority: {ticket["priority"]} | '
            f'Status: {ticket["status"]} | '
            f'Assigned to: {ticket["assigned_to"] or "Unassigned"}'
        )


def save_changes(tickets: list[dict]) -> bool:
    """Save tickets and report whether saving succeeded."""
    try:
        save_tickets(tickets)
        print("Tickets saved successfully.")
        return True
    except (OSError, ValueError) as error:
        print(f"Could not save tickets: {error}")
        return False


def main() -> None:
    """Load tickets and run the CampusFlow CLI."""
    try:
        tickets = load_tickets()
    except (ValueError, OSError) as error:
        print(f"Could not load tickets: {error}")
        return

    print(f"Loaded {len(tickets)} ticket(s).")

    while True:
        print("\n=== CampusFlow ===")
        print("1. View all tickets")
        print("2. View ticket report")
        print("3. Create ticket")
        print("4. Assign ticket")
        print("5. Change ticket status")
        print("6. View work queue")
        print("7. Save tickets")
        print("8. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            display_tickets(tickets)

        elif choice == "2":
            report = generate_report(tickets)

            print(f'Total tickets: {report["total_tickets"]}')
            print("By status:", report["by_status"])
            print("By priority:", report["by_priority"])

        elif choice == "3":
            try:
                title = input("Ticket title: ")
                category = input(
                    "Category (Network, Hardware, Software, Other): "
                )
                urgency = input("Urgency (low, medium, high): ")

                affected_users_text = input("Number of affected users: ")
                affected_users = int(affected_users_text)

                ticket = create_ticket(
                    tickets,
                    title,
                    category,
                    urgency,
                    affected_users,
                )

                print(
                    f'Created {ticket["id"]}: {ticket["title"]} '
                    f'(Priority: {ticket["priority"]})'
                )
                save_changes(tickets)

            except ValueError as error:
                print(f"Could not create ticket: {error}")

        elif choice == "4":
            ticket_id = input("Ticket ID: ").strip()
            staff_name = input("Staff name: ").strip()

            try:
                ticket = assign_ticket(tickets, ticket_id, staff_name)
                print(f'Ticket {ticket["id"]} assigned to {ticket["assigned_to"]}.')
                save_changes(tickets)

            except (ValueError, LookupError) as error:
                print(f"Could not assign ticket: {error}")

        elif choice == "5":
            ticket_id = input("Ticket ID: ").strip()

            print("Available status actions:")
            print("1. Start work (in_progress)")
            print("2. Resolve ticket (resolved)")
            print("3. Reopen ticket (open)")

            status_choice = input("Choose an action: ").strip()

            status_options = {
                "1": "in_progress",
                "2": "resolved",
                "3": "open",
            }

            new_status = status_options.get(status_choice)

            if new_status is None:
                print("Invalid status action.")
                continue

            try:
                ticket = change_status(tickets, ticket_id, new_status)
                print(
                    f'Ticket {ticket["id"]} status changed '
                    f'to {ticket["status"]}.'
                )
                save_changes(tickets)

            except (ValueError, LookupError) as error:
                print(f"Could not change ticket status: {error}")

        elif choice == "6":
            queue = build_queue(tickets)
            display_tickets(queue)

        elif choice == "7":
            save_changes(tickets)

        elif choice == "8":
            if save_changes(tickets):
                print("Goodbye!")
                break

            print("Exit cancelled so you can retry saving.")

        else:
            print("Invalid option. Please choose 1-8.")


if __name__ == "__main__":
    main()
