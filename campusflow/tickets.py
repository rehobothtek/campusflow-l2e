ALLOWED_CATEGORIES = {
    "network": "Network",
    "hardware": "Hardware",
    "software": "Software",
    "other": "Other",
}

ALLOWED_URGENCIES = {"low", "medium", "high"}


def calculate_priority(urgency, affected_users):
    if urgency == "high" and affected_users >= 10:
        return "critical"

    if urgency == "high" or affected_users >= 10:
        return "high"

    if urgency == "medium" or affected_users >= 3:
        return "medium"

    return "low"


def next_ticket_id(tickets):
    existing_numbers = []

    for ticket in tickets:
        ticket_id = ticket.get("id", "")

        if (
            isinstance(ticket_id, str)
            and ticket_id.startswith("T")
            and ticket_id[1:].isdigit()
        ):
            existing_numbers.append(int(ticket_id[1:]))

    next_number = max(existing_numbers, default=0) + 1
    return f"T{next_number:03d}"


def create_ticket(tickets, title, category, urgency, affected_users):
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Title must not be blank.")

    if not isinstance(category, str):
        raise ValueError("Category must be Network, Hardware, Software, or Other.")

    normalised_category = category.strip().lower()

    if normalised_category not in ALLOWED_CATEGORIES:
        raise ValueError("Category must be Network, Hardware, Software, or Other.")

    if not isinstance(urgency, str):
        raise ValueError("Urgency must be low, medium, or high.")

    normalised_urgency = urgency.strip().lower()

    if normalised_urgency not in ALLOWED_URGENCIES:
        raise ValueError("Urgency must be low, medium, or high.")

    if (
        isinstance(affected_users, bool)
        or not isinstance(affected_users, int)
        or affected_users <= 0
    ):
        raise ValueError("Affected users must be a positive integer.")

    ticket = {
        "id": next_ticket_id(tickets),
        "title": title.strip(),
        "category": ALLOWED_CATEGORIES[normalised_category],
        "urgency": normalised_urgency,
        "affected_users": affected_users,
        "priority": calculate_priority(normalised_urgency, affected_users),
        "status": "open",
        "assigned_to": None,
    }

    tickets.append(ticket)
    return ticket


def find_ticket(tickets, ticket_id):
    if not isinstance(ticket_id, str) or not ticket_id.strip():
        raise ValueError("Ticket ID must not be blank.")

    normalised_ticket_id = ticket_id.strip().upper()

    for ticket in tickets:
        if ticket.get("id") == normalised_ticket_id:
            return ticket

    raise ValueError(f"Ticket {normalised_ticket_id} was not found.")


def assign_ticket(tickets, ticket_id, staff_name):
    if not isinstance(staff_name, str) or not staff_name.strip():
        raise ValueError("Staff name must not be blank.")

    ticket = find_ticket(tickets, ticket_id)
    ticket["assigned_to"] = staff_name.strip()
    return ticket

ALLOWED_STATUS_TRANSITIONS = {
    "open": {"in_progress"},
    "in_progress": {"resolved"},
    "resolved": set(),
}


def update_ticket_status(tickets, ticket_id, new_status):
    if not isinstance(new_status, str) or not new_status.strip():
        raise ValueError("Status must not be blank.")

    normalised_status = new_status.strip().lower()

    if normalised_status not in ALLOWED_STATUS_TRANSITIONS:
        raise ValueError("Status must be open, in_progress, or resolved.")

    ticket = find_ticket(tickets, ticket_id)
    current_status = ticket["status"]

    if normalised_status == "in_progress" and not ticket.get("assigned_to"):
        raise ValueError("A ticket must be assigned before work can start.")

    if normalised_status not in ALLOWED_STATUS_TRANSITIONS[current_status]:
        raise ValueError(
            f"Cannot change ticket status from {current_status} to {normalised_status}."
        )

    ticket["status"] = normalised_status
    return ticket


def reopen_ticket(tickets, ticket_id):
    ticket = find_ticket(tickets, ticket_id)

    if ticket["status"] != "resolved":
        raise ValueError("Only resolved tickets can be reopened.")

    ticket["status"] = "open"
    return ticket


PRIORITY_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
}

def get_work_queue(tickets):
    open_tickets = [
        ticket
        for ticket in tickets
        if ticket.get("status") == "open"
    ]

    return sorted(
        open_tickets,
        key=lambda ticket: (
            PRIORITY_ORDER.get(ticket.get("priority"), len(PRIORITY_ORDER)),
            int(str(ticket.get("id", ""))[1:])
            if str(ticket.get("id", "")).startswith("T")
            and str(ticket.get("id", ""))[1:].isdigit()
            else float("inf"),
        ),
    )

def build_ticket_report(tickets):
    by_status = {
        "open": 0,
        "in_progress": 0,
        "resolved": 0,
    }
    by_priority = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
    }
    assigned = 0

    for ticket in tickets:
        status = ticket.get("status")
        priority = ticket.get("priority")

        if status in by_status:
            by_status[status] += 1

        if priority in by_priority:
            by_priority[priority] += 1

        if ticket.get("assigned_to"):
            assigned += 1

    return {
        "total": len(tickets),
        "by_status": by_status,
        "by_priority": by_priority,
        "assigned": assigned,
        "unassigned": len(tickets) - assigned,
    }
