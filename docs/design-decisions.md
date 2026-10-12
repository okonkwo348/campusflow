# CampusFlow Design Decisions

## 1. Project Structure

- Keep the project as a Python command-line application.
- Separate ticket logic, workflow, storage, and reporting into their own modules.
- Keep `main.py` responsible for interacting with the user and connecting the modules.
- Use the existing project structure rather than introducing unnecessary abstractions.

## 2. Ticket Model

Each ticket is represented as a Python dictionary with these fields:

- `id`
- `title`
- `category`
- `urgency`
- `affected_users`
- `priority`
- `status`
- `assigned_to`

Ticket IDs use the format `T001`, `T002`, and so on. New IDs must not conflict with existing tickets.

## 3. Validation Rules

- Categories: `Network`, `Hardware`, `Software`, `Other`.
- Urgency: `low`, `medium`, `high`.
- Titles must not be blank.
- Affected users must be a positive integer. Booleans are not accepted as integers.
- Invalid input must be rejected without corrupting existing ticket data.
- Normalize user input where appropriate, such as trimming whitespace.

## 4. Priority Calculation

Priority is calculated automatically using urgency and the number of affected users.

| Condition | Priority |
|---|---|
| High urgency and at least 10 affected users | Critical |
| High urgency or at least 10 affected users | High |
| Medium urgency or at least 3 affected users | Medium |
| Otherwise | Low |

The rules are evaluated from highest to lowest priority.

## 5. Ticket Workflow

Allowed transitions:

- `open` → `in_progress`
- `in_progress` → `resolved`
- `resolved` → `open` only through an explicit reopen action.

A ticket must be assigned before it can enter `in_progress`. Invalid transitions must be rejected.

## 6. Queue Behaviour

- Only `open` and `in_progress` tickets appear in the active queue.
- Sort by priority: critical, high, medium, then low.
- Break priority ties by numeric ticket ID in ascending order.
- Building the queue must not change the original ticket list order.

## 7. Data Persistence

- Store tickets in JSON.
- Load saved tickets when the application starts.
- A missing data file represents an empty ticket list.
- Malformed JSON must produce a clear error rather than silently discarding data.
- Validate loaded tickets and reject duplicate IDs.
- Validate data before saving.
- Save after successful mutations and when exiting normally.

## 8. Reports

Reports include:

- Total number of tickets.
- Ticket counts by status.
- Ticket counts by priority.

All expected status and priority keys must be present, even when their counts are zero. Empty ticket lists must be supported.

## 9. Testing

- Use Python's built-in `unittest` framework.
- Keep tests organized by module.
- Test normal behaviour, invalid inputs, and important edge cases.
- Run the complete test suite with:

  `python3 -m unittest discover -s tests -v`

- Unit tests passing is not sufficient by itself; verify the complete CLI workflow and persistence after restarting the application.

## 10. Git Workflow

- Develop features on feature branches rather than directly on `main`.
- Review changes before committing.
- Run tests and check the diff before pushing.
- Push feature branches and use pull requests to review changes before merging into `main`.

## 11. Keep the Design Simple

Prefer straightforward functions and clear module responsibilities. Introduce additional abstractions only when a real requirement justifies them. Revisit decisions when the project demonstrates a need to change them.

## 12. Current Verification Status

The current test suite has passed 84 tests. The complete CLI lifecycle and persistence-after-restart check still need to be performed before declaring the milestone fully verified.
