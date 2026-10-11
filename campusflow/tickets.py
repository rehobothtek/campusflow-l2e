ALLOWED_CATEGORIES = {
    "network": "Network",
    "hardware": "Hardware",
    "software": "Software",
    "other": "Other",
}

ALLOWED_URGENCIES = {"low", "medium", "high"}

def calculate_priority(urgency, affected_users):
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

    if normalised_urgency == "high" and affected_users >= 10:
        return "critical"

    if normalised_urgency == "high" or affected_users >= 10:
        return "high"

    if normalised_urgency == "medium" or affected_users >= 3:
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