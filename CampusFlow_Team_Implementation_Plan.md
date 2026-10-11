# CampusFlow — Team Implementation Plan

## 1. Project structure

Both engineers must use the same file structure and shared function contracts.

```text
campusflow/
├── main.py
├── campusflow/
│   ├── __init__.py
│   ├── tickets.py
│   ├── workflow.py
│   ├── storage.py
│   └── reports.py
├── tests/
│   ├── test_tickets.py
│   ├── test_workflow.py
│   └── test_storage.py
├── docs/
│   ├── design-decisions.md
│   └── ai-learning-log.md
├── README.md
└── .gitignore
```

Keep this structure consistent on both branches. Do not create duplicate modules or invent different ticket representations.

## 2. Engineer A — Ticket creation, priority, persistence, and CLI integration

**Suggested branch:** `feat/1-ticket-creation`

### Primary files
- `campusflow/tickets.py`
- `tests/test_tickets.py`
- `campusflow/storage.py`
- `tests/test_storage.py`
- `main.py` (primary author; integrate after contracts are agreed)

### Responsibilities
- Validate ticket input.
- Normalize valid category and urgency values.
- Reject blank titles and invalid `affected_users`.
- Calculate priority using the exact rule order below.
- Generate unique IDs such as `T001`, `T002`, and `T003`.
- Create and return tickets using the agreed shared structure.
- Implement JSON loading and saving.
- Integrate feature functions into the command-line menu after both interfaces are agreed.

### Proposed functions
- `calculate_priority(urgency, affected_users)`
- `create_ticket(tickets, title, category, urgency, affected_users)`
- `load_tickets(path)`
- `save_tickets(tickets, path)`
- `main()`

### Tests
- Priority examples and boundary cases.
- Blank title, invalid category, and invalid urgency.
- Zero, negative, decimal, or text input for `affected_users`.
- Unique IDs, including after existing tickets are loaded.
- JSON save/load round trip.
- Missing JSON file starts with an empty list.
- Malformed JSON produces a clear error and does not silently erase data.

**Important:** `tickets.py` should contain business logic, not `input()` prompts or menu printing. `main.py` collects input and calls functions.

## 3. Engineer B — Assignment, workflow, queue, and reports

**Suggested branch:** `feat/2-ticket-workflow`

### Primary files
- `campusflow/workflow.py`
- `campusflow/reports.py`
- `tests/test_workflow.py`

### Responsibilities
- Assign tickets to non-empty staff names.
- Reject unknown ticket IDs.
- Enforce allowed status transitions.
- Prevent unassigned tickets from entering `in_progress`.
- Require explicit reopening before modifying resolved tickets.
- Build the work queue in priority order, using numeric ticket ID to break ties.
- Generate total ticket, status, and priority reports.

### Proposed functions
- `assign_ticket(tickets, ticket_id, staff_name)`
- `change_status(tickets, ticket_id, new_status)`
- `build_queue(tickets)`
- `generate_report(tickets)`

### Tests
- Valid assignment and blank staff name.
- Unknown ticket ID.
- Valid and invalid status transitions.
- An unassigned ticket cannot enter `in_progress`.
- Queue priority and numeric-ID ordering.
- Reports with tickets and with an empty collection.

**Important:** Engineer B must use the same ticket structure as Engineer A. `workflow.py` and `reports.py` should not create their own ticket collections or prompt for terminal input.

## 4. Shared ticket data structure

Every ticket is a Python dictionary with these fields:

```python
{
    "id": "T001",
    "title": "Campus Wi-Fi is down",
    "category": "Network",
    "urgency": "high",
    "affected_users": 15,
    "priority": "critical",
    "status": "open",
    "assigned_to": None
}
```

### Field rules
- `id`: unique string, formatted as `T001`, `T002`, etc.
- `title`: non-empty string.
- `category`: `Network`, `Hardware`, `Software`, or `Other`.
- `urgency`: `low`, `medium`, or `high`.
- `affected_users`: positive integer.
- `priority`: `low`, `medium`, `high`, or `critical`.
- `status`: `open`, `in_progress`, or `resolved`.
- `assigned_to`: staff name string or `None`.

## 5. Shared function contracts

These are proposed contracts. Both engineers should agree on them before implementation and record the decisions in `docs/design-decisions.md`.

| Function | Expected behaviour |
|---|---|
| `calculate_priority(urgency, affected_users)` | Returns a priority string. |
| `create_ticket(tickets, title, category, urgency, affected_users)` | Adds a valid ticket to the shared list and returns the new ticket. |
| `assign_ticket(tickets, ticket_id, staff_name)` | Updates the matching ticket and returns it. |
| `change_status(tickets, ticket_id, new_status)` | Validates the transition, updates the ticket, and returns it. |
| `build_queue(tickets)` | Returns open, unresolved tickets in required order without changing the original list. |
| `generate_report(tickets)` | Returns total tickets and breakdowns by status and priority. |
| `load_tickets(path)` | Loads tickets from JSON, or returns an empty list when the file is missing. |
| `save_tickets(tickets, path)` | Persists the ticket collection to JSON. |

### Error-handling agreement
1. Raise `ValueError` for invalid input, such as a blank title or staff name.
2. Raise `LookupError` when a requested ticket ID does not exist.
3. Validate before modifying a ticket.
4. Functions must not print menu messages or request terminal input.
5. `main.py` catches expected errors and displays helpful messages.
6. A failed save must not be reported as a successful operation. The integration layer must restore the previous in-memory state if saving fails.

These exception types are a proposed team convention, not an immutable requirement. Agree on them before coding.

## 6. Critical business rules

### Priority calculation — check rules in this order
1. High urgency **AND** at least 10 affected users → `critical`
2. High urgency **OR** at least 10 affected users → `high`
3. Medium urgency **OR** at least 3 affected users → `medium`
4. All remaining valid tickets → `low`

Apply the first matching rule.

### Status workflow
- `open` → `in_progress` → `resolved`.
- An unassigned ticket cannot enter `in_progress`.
- A resolved ticket requires an explicit reopen to `open` before further modification.
- A blank staff name is invalid; a failed reassignment must leave the existing assignee unchanged.

### Work queue
- Include open, unresolved tickets.
- Sort by `critical`, `high`, `medium`, `low`.
- Break priority ties using the numeric ticket ID, not alphabetical string ordering.
- Building the queue should not reorder or mutate the original ticket collection.


# Enginner C  Persistence, Reporting, and CLI

Files owned
- campusflow/storage.py

- campusflow/reports.py

- main.py

- tests/test_storage.py

- tests/test_reports.py



Required function signatures
In campusflow/storage.py:
def load_tickets(path: str = "tickets.json") -> list[dict]:
    ...

def save_tickets(
    tickets: list[dict],
    path: str = "tickets.json",
) -> None:
    ```

In `campusflow/reports.py`:

```python
def generate_report(tickets: list[dict]) -> dict:
    ...


In main.py:

def main() -> None:
    ...

    
### Persistence
- Load JSON at program startup.
- Save successful changes.
- A missing file means a fresh start with an empty list.
- Malformed JSON must produce a clear error, not silently erase data.
- IDs must remain unique after reloading.
- If saving fails, do not claim the change was saved. Restore in-memory state if the save fails. Consider writing to a temporary file and replacing the original only after the write succeeds, to reduce the risk of corrupting the existing JSON file.

## 7. Ownership and collaboration rules

| File | Primary owner | Notes |
|---|---|---|
| `tickets.py` | Engineer A | Creation, validation, priority, IDs |
| `test_tickets.py` | Engineer A | Creation and priority tests |
| `storage.py` | Engineer A | JSON persistence |
| `test_storage.py` | Engineer A | Persistence and reload tests |
| `main.py` | Engineer A | CLI and integration after contracts are agreed |
| `workflow.py` | Engineer B | Assignment and status transitions |
| `reports.py` | Engineer C | Queue and reports |
| `test_workflow.py` | Engineer B | Assignment and workflow tests |
| `docs/design-decisions.md` | Both | Record agreed data structure, contracts, exceptions, persistence policy |
| `docs/ai-learning-log.md` | Each engineer | Each person records their own genuine learning and verification |

Both engineers must contribute application code and tests. Each engineer must open a pull request, review the partner's pull request, and receive approval before merging. Avoid editing the same file independently on separate branches.

## 8. Git workflow

Create branches from the latest `main`; do not work directly on `main`.

Engineer A:

```bash
git switch main
git pull origin main
git switch -c feat/1-ticket-creation
```

Engineer B:

```bash
git switch main
git pull origin main
git switch -c feat/2-ticket-workflow
```


Engineer B:

```bash

git switch main
git pull origin main
git switch -c   feat/storage-reports-cli  .
```

For each change:
1. Implement one small requirement.
2. Run relevant tests.
3. Inspect `git status` and `git diff`.
4. Commit focused changes with a meaningful message.
5. Push the branch.
6. Open a pull request with the issue reference and actual test results.
7. Have the partner review the code and tests before approval and merge.

If the other PR merges first, update your branch from the latest `main`, resolve any conflicts carefully, and rerun the full test suite.

## 9. Suggested implementation order

1. Agree on ticket fields, function signatures, exception handling, and save-failure behaviour.
2. Record decisions in `docs/design-decisions.md`.
3. Both engineers implement their own business logic and tests in parallel.
4. Engineer A implements JSON persistence and the initial CLI integration.
5. Integrate both branches through reviewed pull requests.
6. Run the full test suite on `main` and manually demonstrate the full CLI workflow.

## 10. Final checklist

- [ ] All seven features are available from the CLI.
- [ ] Priority rules and order are correct.
- [ ] Invalid input and invalid status transitions are rejected without corrupting tickets.
- [ ] Tickets survive a restart through JSON persistence.
- [ ] IDs remain unique after reload.
- [ ] At least eight meaningful automated tests pass on integrated `main`.
- [ ] Both engineers authored a feature PR and reviewed the partner's PR.
- [ ] Both engineers have genuine AI learning-log entries and can explain their own code.
- [ ] README includes setup, run, test, workflow, persistence, and known limitations.

**Sprint advice:** Keep the design simple. Agree on the contracts, build small functions, test them, and integrate early. Do not spend the six-hour sprint over-designing the architecture.
