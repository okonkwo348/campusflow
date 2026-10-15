from campusflow.tickets import (
    create_ticket,
    validate_title,
    validate_category,
    validate_urgency,
)
from campusflow.workflow import assign_ticket, change_status, build_queue
from campusflow.storage import load_tickets, save_tickets
from campusflow.search import search_tickets
from campusflow.reports import generate_report
from campusflow.engineering_quiz import run_quiz
from campusflow.tickets import add_note, get_ticket_notes


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


def search_menu(tickets):
    query = input("Title search (leave blank for all titles): ")

    category = input(
        "Category (Network/Hardware/Software/Other, blank for any): "
    ).strip()

    status = input(
        "Status (open/in_progress/resolved, blank for any): "
    ).strip()

    priority = input(
        "Priority (critical/high/medium/low, blank for any): "
    ).strip()

    try:
        results = search_tickets(
            tickets,
            query=query,
            category=category or None,
            status=status or None,
            priority=priority or None,
        )
    except ValueError as error:
        print(f"Search error: {error}")
        return

    if not results:
        print("No matching tickets found.")
        return

    for ticket in results:
        print(
            f"{ticket['id']} | {ticket['title']} | "
            f"{ticket['category']} | {ticket['priority']} | "
            f"{ticket['status']} | Assigned: "
            f"{ticket['assigned_to'] or 'Unassigned'}"
        )


def report_menu(tickets):
    report = generate_report(tickets)

    print("\n--- TICKET ANALYTICS ---")
    print(f"Total tickets: {report['total_tickets']}")

    print("\nBy status:")
    for status, count in report["by_status"].items():
        print(f"  {status}: {count}")

    print("\nBy priority:")
    for priority, count in report["by_priority"].items():
        print(f"  {priority}: {count}")

    print("\nBy category:")
    for category, count in report["by_category"].items():
        print(f"  {category}: {count}")

    print(f"\nUnresolved: {report['unresolved']}")
    print(f"Resolved: {report['resolved']}")
    print(
        "Resolution percentage: "
        f"{report['resolution_percentage']:.1f}%"
    )


def add_note_menu(tickets):
    ticket_id = input("Ticket ID: ").strip()
    author = input("Author: ").strip()
    message = input("Note: ").strip()

    try:
        note = add_note(tickets, ticket_id, author, message)
    except (ValueError, LookupError) as error:
        print(f"Could not add note: {error}")
        return

    print(f"Note {note['note_id']} added successfully.")


def view_notes_menu(tickets):
    ticket_id = input("Ticket ID: ").strip()

    try:
        notes = get_ticket_notes(tickets, ticket_id)
    except LookupError as error:
        print(f"Could not find ticket: {error}")
        return

    if not notes:
        print("This ticket has no notes.")
        return

    for note in notes:
        print(
            f"{note['note_id']} | {note['author']}: "
            f"{note['message']}"
        )


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
        print("F1. CREATE tickets")
        print("F2. LIST / VIEW report")
        print("F3. ASSIGN ticket to staff")
        print("F4. WORKFLOW ticket")
        print("F5.  WORK QUEUE of ticket")
        print("F6.  REPORTS of ticket")
        print("F7.  PERSISTENCE-Save tickets")
        print("F8. SEARCH")
        print("F9. ADD_NOTE")
        print("F10. VIEW_NOTES")
        print("F11 QUIZ")
        print("F12. Exit")

        choice = input("Choose an option (F1-F12): ").strip().upper()

        if choice in ("F1", "1"):
            # Validate each field at the point where it is entered so the
            # user sees the error immediately and can retry that field.
            while True:
                try:
                    title = validate_title(input("Ticket title: "))
                    break
                except ValueError as error:
                    print(f"Invalid title: {error}")

            while True:
                try:
                    category = validate_category(input(
                        "Category (Network, Hardware, Software, Other): "
                    ))
                    break
                except ValueError as error:
                    print(f"Invalid category: {error}")

            while True:
                try:
                    urgency = validate_urgency(
                        input("Urgency (low, medium, high): ")
                    )
                    break
                except ValueError as error:
                    print(f"Invalid urgency: {error}")

            while True:
                affected_users_text = input(
                    "Number of affected users (positive whole number): "
                ).strip()

                try:
                    affected_users = int(affected_users_text)
                except ValueError:
                    print(
                        "Invalid input. Enter a positive whole number, "
                        "such as 1 or 5."
                    )
                    continue

                if affected_users <= 0:
                    print(
                        "Invalid input. The number of affected users "
                        "must be greater than zero."
                    )
                    continue

                break

            try:
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

        elif choice in ("F2", "2"):
            display_tickets(tickets)

        elif choice in ("F3", "3"):
            ticket_id = input("Ticket ID: ").strip()
            staff_name = input("Staff name: ").strip()
            try:
                ticket = assign_ticket(tickets, ticket_id, staff_name)
                print(
                    f'Ticket {ticket["id"]} assigned to '
                    f'{ticket["assigned_to"]}.'
                )
                save_changes(tickets)
            except (ValueError, LookupError) as error:
                print(f"Could not assign ticket: {error}")

        elif choice in ("F4", "4"):
            ticket_id = input("Ticket ID: ").strip()
            print("Available workflow actions:")
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
                print("Invalid workflow action.")
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

        elif choice in ("F5", "5"):
            display_tickets(build_queue(tickets))

        elif choice in ("F6", "6"):
            report_menu(tickets)

        elif choice in ("F7", "7"):
            save_changes(tickets)

        elif choice in ("F8", "8"):
            search_menu(tickets)

        elif choice in ("F9", "9"):
            add_note_menu(tickets)
            save_changes(tickets)

        elif choice in ("F10", "10"):
            view_notes_menu(tickets)

        elif choice in ("F11", "11"):
            run_quiz()

        elif choice in ("F12", "12", "EXIT", "Q"):
            if save_changes(tickets):
                print("Goodbye!")
                break
            print("Exit cancelled so you can retry saving.")

        else:
            print("Invalid option. Please choose F1-F12.")


if __name__ == "__main__":
    main()
