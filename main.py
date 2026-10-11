from campusflow.storage import load_tickets, save_tickets
from campusflow.tickets import (
    assign_ticket,
    build_ticket_report,
    create_ticket,
    get_work_queue,
    reopen_ticket,
    update_ticket_status,
)


def print_ticket(ticket):
    assigned_to = ticket["assigned_to"] or "Unassigned"

    print(f"\nID: {ticket['id']}")
    print(f"Title: {ticket['title']}")
    print(f"Category: {ticket['category']}")
    print(f"Urgency: {ticket['urgency']}")
    print(f"Affected users: {ticket['affected_users']}")
    print(f"Priority: {ticket['priority']}")
    print(f"Status: {ticket['status']}")
    print(f"Assigned to: {assigned_to}")


def create_new_ticket(tickets):
    title = input("Title: ")
    category = input("Category (Network, Hardware, Software): ")
    urgency = input("Urgency (low, medium, high): ")

    try:
        affected_users = int(input("Number of affected users: "))
        ticket = create_ticket(
            tickets,
            title,
            category,
            urgency,
            affected_users,
        )
        save_tickets(tickets)
        print(f"\nTicket {ticket['id']} created successfully.")
    except ValueError as error:
        print(f"\nCould not create ticket: {error}")


def view_all_tickets(tickets):
    if not tickets:
        print("\nNo tickets found.")
        return

    for ticket in tickets:
        print_ticket(ticket)


def assign_staff_member(tickets):
    ticket_id = input("Ticket ID: ")
    staff_name = input("Staff member name: ")

    try:
        ticket = assign_ticket(tickets, ticket_id, staff_name)
        save_tickets(tickets)
        print(f"\n{ticket['id']} assigned to {ticket['assigned_to']}.")
    except ValueError as error:
        print(f"\nCould not assign ticket: {error}")


def change_ticket_status(tickets):
    ticket_id = input("Ticket ID: ")
    new_status = input("New status (in_progress or resolved): ")

    try:
        ticket = update_ticket_status(tickets, ticket_id, new_status)
        save_tickets(tickets)
        print(f"\n{ticket['id']} is now {ticket['status']}.")
    except ValueError as error:
        print(f"\nCould not update ticket: {error}")


def reopen_resolved_ticket(tickets):
    ticket_id = input("Resolved ticket ID to reopen: ")

    try:
        ticket = reopen_ticket(tickets, ticket_id)
        save_tickets(tickets)
        print(f"\n{ticket['id']} has been reopened.")
    except ValueError as error:
        print(f"\nCould not reopen ticket: {error}")


def show_work_queue(tickets):
    queue = get_work_queue(tickets)

    if not queue:
        print("\nNo open tickets in the work queue.")
        return

    print("\nOpen work queue:")
    for ticket in queue:
        print(f"{ticket['id']} | {ticket['priority']} | {ticket['title']}")


def show_report(tickets):
    report = build_ticket_report(tickets)

    print("\nTicket report")
    print(f"Total tickets: {report['total']}")
    print(f"Assigned: {report['assigned']}")
    print(f"Unassigned: {report['unassigned']}")

    print("\nBy status:")
    for status, count in report["by_status"].items():
        print(f"- {status}: {count}")

    print("\nBy priority:")
    for priority, count in report["by_priority"].items():
        print(f"- {priority}: {count}")


def main():
    try:
        tickets = load_tickets()
    except ValueError as error:
        print(f"Cannot start CampusFlow: {error}")
        return

    while True:
        print("\n--- CampusFlow Helpdesk ---")
        print("1. Create ticket")
        print("2. View all tickets")
        print("3. Assign staff member")
        print("4. Update ticket status")
        print("5. Reopen resolved ticket")
        print("6. View work queue")
        print("7. View report")
        print("8. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_new_ticket(tickets)
        elif choice == "2":
            view_all_tickets(tickets)
        elif choice == "3":
            assign_staff_member(tickets)
        elif choice == "4":
            change_ticket_status(tickets)
        elif choice == "5":
            reopen_resolved_ticket(tickets)
        elif choice == "6":
            show_work_queue(tickets)
        elif choice == "7":
            show_report(tickets)
        elif choice == "8":
            print("Goodbye.")
            break
        else:
            print("\nPlease enter a number from 1 to 8.")


if __name__ == "__main__":
    main()