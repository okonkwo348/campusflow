# CampusFlow — Shared Function Signatures and Fixed Ticket Contract

This document is the shared interface contract for all three team members. Agree on it before implementation. Do not change field names or function signatures independently; propose changes to the whole team first.

## 1. Canonical ticket structure

Every ticket is a Python dictionary with exactly these keys:

```python
{
    "id": "T001",
    "title": "Campus Wi-Fi is down",
    "category": "Network",
    "urgency": "high",
    "affected_users": 15,
    "priority": "critical",
    "status": "open",
    "assigned_to": None,
}
```

| Key | Type | Rule |
|---|---|---|
| `id` | `str` | Unique ID in `T001`, `T002`, ... format |
| `title` | `str` | Must not be blank |
| `category` | `str` | `Network`, `Hardware`, `Software`, or `Other` |
| `urgency` | `str` | `low`, `medium`, or `high` |
| `affected_users` | `int` | Positive integer; reject booleans |
| `priority` | `str` | `critical`, `high`, `medium`, or `low` |
| `status` | `str` | `open`, `in_progress`, or `resolved` |
| `assigned_to` | `str | None` | Nonblank staff name or `None` |

Normalize valid case variations to the canonical spelling before storing them. Keep the ticket fields and their types consistent in memory and in JSON.

## 2. Priority rules

Apply in this exact order:

1. `urgency == "high"` AND `affected_users >= 10` → `"critical"`
2. `urgency == "high"` OR `affected_users >= 10` → `"high"`
3. `urgency == "medium"` OR `affected_users >= 3` → `"medium"`
4. Otherwise → `"low"`

Priority is calculated during ticket creation and stored on the ticket. The queue sorts by this stored value; it does not recalculate priority.

## 3. Shared function signatures

Use these names, arguments, and return expectations across the team.

### `campusflow/tickets.py` — Person 1

```python
def calculate_priority(urgency: str, affected_users: int) -> str:
    """Return critical, high, medium, or low; do not create or mutate a ticket."""

def create_ticket(
    tickets: list[dict],
    title: str,
    category: str,
    urgency: str,
    affected_users: int,
) -> dict:
    """Validate input, create the next unique ID, append the new ticket to tickets, and return it."""

def find_ticket(tickets: list[dict], ticket_id: str) -> dict:
    """Return the matching ticket; raise LookupError if no ticket matches."""
```

`create_ticket` owns the append to the shared list. The caller should not append the returned ticket a second time.

### `campusflow/workflow.py` — Person 2

```python
def assign_ticket(
    tickets: list[dict],
    ticket_id: str,
    staff_name: str,
) -> dict:
    """Assign a ticket and return the updated ticket."""

def change_status(
    tickets: list[dict],
    ticket_id: str,
    new_status: str,
) -> dict:
    """Apply a permitted status transition and return the updated ticket."""

def build_queue(tickets: list[dict]) -> list[dict]:
    """Return a NEW filtered/sorted list; never reorder or mutate tickets."""
```

Workflow contract:
- Permitted transitions: `open` → `in_progress`, `in_progress` → `resolved`, and explicit reopen `resolved` → `open`.
- An unassigned ticket cannot move to `in_progress`.
- Invalid transitions must leave the ticket unchanged.
- A blank staff name must be rejected before changing `assigned_to`.
- Unknown IDs raise `LookupError`.
- `build_queue` includes `open` and `in_progress` tickets and excludes `resolved`.
- Queue order: `critical`, `high`, `medium`, `low`; within equal priority, sort by the numeric part of the ID ascending. Example: `T002` before `T010`.
- Do not recalculate priority in `build_queue`.

### `campusflow/storage.py` — Person 3

```python
def load_tickets(path: str = "tickets.json") -> list[dict]:
    """Load and validate the saved ticket list; return [] if the file is missing."""

def save_tickets(tickets: list[dict], path: str = "tickets.json") -> None:
    """Persist the current ticket list as JSON; return None on success."""
```

Storage contract:
- Missing file returns an empty list.
- Malformed JSON raises a clear error; never silently replace it with an empty file.
- File read/write errors must be surfaced to the CLI.
- IDs must remain unique after reload.
- Saving successfully means the data was written. If saving fails, the CLI must not claim it was saved. Team must agree whether a failed save rolls back the in-memory change; recommended for this sprint: restore the prior ticket state.

### `campusflow/reports.py` — Person 3

```python
def generate_report(tickets: list[dict]) -> dict:
    """Return totals and status/priority counts; do not print."""
```

Use this exact report result shape:

```python
{
    "total_tickets": 4,
    "by_status": {
        "open": 2,
        "in_progress": 1,
        "resolved": 1,
    },
    "by_priority": {
        "critical": 1,
        "high": 1,
        "medium": 1,
        "low": 1,
    },
}
```

All keys must be present even when their count is zero. An empty list returns `total_tickets: 0` and zero for every status and priority.

### `main.py` — Person 3

```python
def main() -> None:
    """Load tickets, run the CLI menu loop, call module functions, and save successful changes."""
```

`main.py` owns input/output and user-facing messages. Business functions must not call `input()` or print CLI messages. Catch expected exceptions at the CLI boundary and keep the menu running after recoverable input errors.

## 4. Error contract

Use consistent errors:

- `ValueError`: invalid field, blank title/staff name, invalid status, or forbidden transition.
- `LookupError`: unknown ticket ID.
- `OSError`: file read/write failure.
- `ValueError` with a clear message (or a documented custom storage exception) for malformed JSON.

Always validate before mutating a ticket. Failed operations must not leave partial changes.

## 5. Shared collection and module ownership

- `main.py` loads one `tickets` list and passes that same list to functions.
- Person 1 owns creation, validation, priority calculation, and ticket lookup.
- Person 2 owns assignment, status transitions, and queue generation.
- Person 3 owns JSON persistence, reports, and CLI orchestration.
- Do not maintain separate ticket lists in individual modules.
- Do not duplicate priority calculation, queue sorting, or workflow rules in `main.py`.

## 6. Minimum integration tests

- Each priority rule returns the expected value.
- Ticket validation rejects invalid values and creation assigns unique IDs.
- `find_ticket` returns a match and raises `LookupError` for an unknown ID.
- Blank assignment and invalid transitions leave existing ticket data unchanged.
- Unassigned tickets cannot enter `in_progress`.
- Queue filters resolved tickets, sorts by priority then numeric ID, and leaves original list order unchanged.
- JSON save/load round trip works; missing file returns `[]`; malformed JSON is not silently erased.
- Reports return all expected keys for normal and empty lists.
- CLI handles invalid user input without crashing.

Run the suite:

```bash
python -m unittest discover -s tests -v
```

## 7. Change-control rule

If a teammate needs to change a signature, ticket field, allowed value, or return shape, discuss it with the other two teammates and update this contract first. Do not make unilateral interface changes.
