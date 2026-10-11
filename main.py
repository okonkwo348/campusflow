
from campusflow.storage import load_tickets, save_tickets
from campusflow.reports import generate_report


def main() -> None:
    """Load tickets, run the CLI menu, and save successful changes."""
    try:
        tickets = load_tickets()
    except (ValueError, OSError) as error:
        print(f"Could not load tickets: {error}")
        return

    while True:
        print("\n=== CampusFlow ===")
        print("1. View all tickets")
        print("2. View ticket report")
        print("3. Save tickets")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            if not tickets:
                print("No tickets found.")
            else:
                for ticket in tickets:
                    print(
                        f'{ticket["id"]}: {ticket["title"]} | '
                        f'Status: {ticket["status"]} | '
                        f'Priority: {ticket["priority"]}'
                    )

        elif choice == "2":
            report = generate_report(tickets)
            print(f'Total tickets: {report["total_tickets"]}')
            print("By status:", report["by_status"])
            print("By priority:", report["by_priority"])

        elif choice == "3":
            try:
                save_tickets(tickets)
                print("Tickets saved successfully.")
            except OSError as error:
                print(f"Could not save tickets: {error}")

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
