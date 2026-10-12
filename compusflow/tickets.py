VALID_CATEGORIES = {"Network", "Hardware", "Software", "Other"}
VALID_URGENCIES = {"low", "medium", "high"}


def validate_title(title: str) -> str:
    """Return a trimmed, non-empty title."""
    if not isinstance(title, str):
        raise ValueError("Title must be a string.")

    title = title.strip()

    if not title:
        raise ValueError("Title must not be blank. Enter a problem.")
 
    return title


def validate_category(category: str) -> str:
    """Validate and normalize a ticket category."""
    if not isinstance(category, str):
        raise ValueError("Category must be a string.")

    category = category.strip().lower()

    categories = {value.lower(): value for value in VALID_CATEGORIES}

    if category not in categories:
        raise ValueError(
            "Invalid category. Choose Network, Hardware, Software, or Other."
        )

    return categories[category]


def validate_urgency(urgency: str) -> str:
    """Validate and normalize urgency."""
    if not isinstance(urgency, str):
        raise ValueError("Urgency must be a string.")

    urgency = urgency.strip().lower()

    if urgency not in VALID_URGENCIES:
        raise ValueError("Invalid urgency. Choose low, medium, or high.")

    return urgency


def validate_affected_users(count: int) -> int:
    """Require a positive integer, excluding booleans."""
    if isinstance(count, bool) or not isinstance(count, int):
        raise ValueError("Affected users must be a whole number.")

    if count <= 0:
        raise ValueError("Affected users must be greater than zero.")

    return count
