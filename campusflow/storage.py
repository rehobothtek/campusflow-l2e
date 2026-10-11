import json
from pathlib import Path


DEFAULT_DATA_FILE = Path("data") / "tickets.json"


def load_tickets(file_path=DEFAULT_DATA_FILE):
    """Load tickets from JSON, or return an empty list on the first run."""
    path = Path(file_path)

    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            tickets = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(f"Could not read ticket data from {path}.") from error

    if not isinstance(tickets, list):
        raise ValueError("Ticket data must be a JSON list.")

    return tickets


def save_tickets(tickets, file_path=DEFAULT_DATA_FILE):
    """Save the current ticket list to JSON."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=2)