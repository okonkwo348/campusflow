
import json
import os


def load_tickets(path: str = "tickets.json") -> list[dict]:
    """Load tickets from a JSON file."""
    if not os.path.exists(path):
        return []

    try:
        with open(path, "r", encoding="utf-8") as file:
            tickets = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON in {path}: {error}") from error

    if not isinstance(tickets, list):
        raise ValueError(f"{path} must contain a JSON list of tickets.")

    return tickets
