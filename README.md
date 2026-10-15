# 🎓 CampusFlow Next

### A Reliable Campus Helpdesk and Ticket Management System

**CampusFlow** is a Python command-line application for managing campus IT support requests. Staff can create and track tickets, assign responsibility, move tickets through a controlled workflow, add follow-up notes, search and filter tickets, and generate reports.

**CampusFlow Next** is the quality-and-reliability upgrade of the original project. It adds stronger validation, structured follow-up notes, multi-filter search, richer reports, safe JSON loading, an Engineering Understanding Check quiz, and a larger automated test suite, while preserving every original feature.

---

## 👥 Our Team

| Role | Team Member | Responsibility |
|---|---|---|
| **Engineer A** | **AYANDE WUESE JOY** | Ticket safety and storage: validation, assignment and status protection, open-only work queue, follow-up notes (data rules), safe JSON load/save and ID continuity |
| **Engineer B** | **OKONKWO EMMANUEL CHISOM** | Search, reports and CLI: title search with combined filters, enhanced reports, menu and input handling, note menus, Engineering Understanding Check quiz |

Both engineers agreed the function contracts, wrote code and tests, reviewed each other's pull requests, and documented their AI-assisted learning.

The original CampusFlow version also included contributions from **Muhammed Maryam** and **Christain Patrick**.

**Project Repository:** https://github.com/okonkwo348/campusflow

---

## 🎯 Project Objectives

- Record and track campus IT support requests.
- Prioritise tickets by urgency and the number of affected users.
- Enforce a controlled assignment and resolution workflow.
- Reject invalid actions without changing or losing data.
- Preserve tickets and notes between sessions.
- Help staff find tickets quickly and report clearly to the Head of Campus.

---

## ✨ Features

### 1. Ticket creation (F1)
Create tickets with a title, category, urgency and number of affected users. Input is validated before anything is saved:

- Category must be **Network, Hardware, Software or Other** (case variations such as `network` are normalised).
- Urgency must be **low, medium or high**.
- Title cannot be blank.
- Affected users must be a positive whole number. Zero, negatives, decimals, text and booleans are rejected.

Ticket IDs are generated automatically (`T001`, `T002`, …) and stay unique after a restart.

### 2. Automatic priority calculation
The first matching rule wins:

| Priority | Rule |
|---|---|
| Critical | High urgency **and** at least 10 affected users |
| High | High urgency **or** at least 10 affected users |
| Medium | Medium urgency **or** at least 3 affected users |
| Low | All other valid tickets |

### 3. List and view tickets (F2)
Show all tickets with their ID, title, category, priority, status and assigned staff.

### 4. Assignment (F3)
Assign a ticket to a non-empty staff name. Assigning does **not** change the ticket's status. A **resolved** ticket cannot be assigned or reassigned until it is reopened.

### 5. Status workflow (F4)

`open → in_progress → resolved`, and `resolved → open` (explicit reopen)

- An unassigned ticket cannot move to `in_progress`.
- A ticket cannot skip from `open` straight to `resolved`.
- Invalid transitions are rejected and the ticket is left unchanged.

### 6. Open Work Queue (F5)
Shows **only open tickets**, ordered critical → high → medium → low, with the lower numeric ticket ID first when priorities tie (T002 before T010). `in_progress` and `resolved` tickets are not included.

### 7. Reports (F6)
- Total tickets
- Counts by status, priority and category
- Unresolved count (open + in_progress) and resolved count
- Resolution percentage (resolved ÷ total × 100). An empty dataset reports **0%** without errors.

Reports count each ticket by its **current** status, so a reopened ticket is no longer counted as resolved.

### 8. JSON persistence (F7)
Tickets, including notes, are saved to `tickets.json` and reloaded at startup. See [Data storage](#-data-storage).

### 9. Search and filter (F8)
Read-only search by title (case-insensitive substring), with optional filters for category, status and priority. **All supplied filters must match (AND)**; empty filters mean "do not filter by this field". Search never changes ticket records.

### 10. Follow-up notes (F9, F10)
- Add a note with an author and a message; view all notes for a ticket in ID order.
- Notes can be added only to **open** or **in_progress** tickets. A resolved ticket must be reopened first.
- Author cannot be blank; the message must be **5–300 characters** after trimming.
- Note IDs are per ticket (`N001`, `N002`, …). A rejected note does not use up an ID.
- Notes are kept through resolve and reopen, and survive save and reload.

### 11. Engineering Understanding Check (F11)
A six-question multiple-choice quiz about the application's own rules. Answers must be A, B, C or D (invalid input is asked again), the score is shown out of 6, and the user explains at least two answers.

---

## 💾 Data Storage

- **File:** `tickets.json` in the project root.
- **Format:** a JSON list of ticket objects:

```json
[
    {
        "id": "T001",
        "title": "Campus Wi-Fi is down",
        "category": "Network",
        "urgency": "high",
        "affected_users": 15,
        "priority": "critical",
        "status": "open",
        "assigned_to": null,
        "notes": [
            {"note_id": "N001", "author": "Support staff", "message": "Investigating the router."}
        ]
    }
]
```

- **Missing file:** the app starts with no tickets.
- **Safe loading:** the whole file is checked before it is used. The load is rejected with a clear error, and current data is left untouched, if the file has malformed JSON, missing or extra fields, invalid category/urgency/status/priority, a priority that does not match the rules, duplicate ticket IDs, an `in_progress` ticket with no assignee, invalid notes, or duplicate note IDs within a ticket.
- **Older files:** files saved before notes existed have no `notes` field; these tickets load with an empty notes list.
- **Start fresh:** delete or rename `tickets.json`.
- `tickets.json` is runtime data and is excluded from Git via `.gitignore`.

---

## 🛠️ Technology Stack

- **Language:** Python 3 (standard library only)
- **Data storage:** JSON
- **Automated testing:** `unittest`
- **Version control and review:** Git and GitHub

No web framework, external database, AI SDK or API key is required.

---

## 📁 Project Structure

```text
campusflow/
├── README.md
├── .gitignore
├── main.py
├── campusflow/
│   ├── __init__.py
│   ├── tickets.py
│   ├── workflow.py
│   ├── storage.py
│   ├── search.py
│   ├── reports.py
│   └── engineering_quiz.py
├── tests/
│   ├── test_tickets.py
│   ├── test_workflow.py
│   ├── test_notes.py
│   ├── test_storage.py
│   ├── test_search.py
│   ├── test_reports.py
│   └── test_engineering_quiz.py
└── docs/
    ├── ai-learning-log.md
    └── design-decisions.md
```

**Module responsibilities**

| Module | Responsibility | Owner |
|---|---|---|
| `tickets.py` | Ticket validation, priority, ID generation, lookup, `validate_ticket`, `add_note`, `get_ticket_notes` | Engineer A |
| `workflow.py` | Assignment, status transitions, Open Work Queue | Engineer A |
| `storage.py` | Safe JSON load/save, full-file validation, notes migration | Engineer A |
| `search.py` | Title search and combined filters | Engineer B |
| `reports.py` | Report counts and resolution percentage | Engineer B |
| `engineering_quiz.py` | Understanding Check question bank and scoring | Engineer B |
| `main.py` | Menu, input, output and friendly error messages | Engineer B |

Business functions never call `input()` or `print()`. They return values or raise errors (`ValueError` for invalid input or forbidden actions, `LookupError` for unknown ticket IDs), and `main.py` displays friendly messages.

---

## 🚀 Getting Started

### Prerequisites

```bash
python3 --version
```

### 1. Clone the repository

```bash
git clone https://github.com/okonkwo348/campusflow.git
cd campusflow
```

### 2. Run the application

```bash
python3 main.py
```

Choose an option from the menu by entering, for example, `F1` or `1`:

| Option | Action |
|---|---|
| F1 | Create a ticket |
| F2 | List / view tickets |
| F3 | Assign a ticket to staff |
| F4 | Change ticket status (start, resolve, reopen) |
| F5 | View the Open Work Queue |
| F6 | View reports |
| F7 | Save tickets |
| F8 | Search tickets |
| F9 | Add a follow-up note |
| F10 | View ticket notes |
| F11 | Engineering Understanding Check quiz |
| F12 | Exit |

### 3. Run the automated tests

```bash
python3 -m unittest discover -s tests -v
```

---

## 🧪 Testing

The suite uses `unittest` and runs from a fresh clone with the command above. It covers:

- Priority rules and their boundaries.
- Rejection of invalid categories, urgency, blank titles and invalid affected users (0, negative, decimal, boolean).
- Unassigned `open → in_progress` rejected with the ticket unchanged.
- Resolved-ticket reassignment rejected with the ticket unchanged.
- The full lifecycle, including reopen.
- Open Work Queue ordering, numeric tie-breaks, and exclusion of `in_progress` and `resolved` tickets.
- Notes: correct IDs, rejected notes not using an ID, resolved tickets rejecting notes until reopened.
- Save/load preserving notes and the next ticket and note IDs.
- Corrupt JSON, duplicate ticket IDs and duplicate note IDs rejected.
- Case-insensitive title search and AND-combined filters.
- Empty reports returning 0% and correct counts after resolve/reopen.
- Quiz input validation and scoring.

---

## 🤝 Team Workflow

1. Open a GitHub Issue with clear acceptance criteria.
2. Create a feature branch from the latest `main` (`<type>/<issue>-<description>`).
3. Implement the change with tests, in small focused commits.
4. Run the full test suite before every commit.
5. Open a pull request with test evidence and `Closes #<issue>`.
6. The other engineer reviews the code, runs the tests and leaves specific comments.
7. Merge only after approval; then update other branches from `main` and rerun the tests.

**Principles:** no direct commits to `main`, no self-approval, no secrets in commits, and honest documentation of decisions and learning.

---

## 📚 Documentation

- `docs/design-decisions.md` — agreed rules, function contracts and the reasons behind them.
- `docs/ai-learning-log.md` — each engineer's AI-assisted learning cycles, experiments and verification.

AI was used to learn, investigate failures and review designs. Every suggestion was checked with tests before being kept.

---

## ⚠️ Known Limitations

- Ticket IDs are matched exactly inside the business functions (`T001`, not `t001`); the menu should normalise input.
- Notes can be added and viewed, but not edited or deleted.
- Search uses simple substring matching; there is no fuzzy spelling correction.
- Data is stored in a single local JSON file; there is no multi-user access.

## 🔮 Future Improvements

- Timestamps for tickets and notes.
- Editing and deleting notes.
- Assignment history.
- Exporting reports to CSV.

---

*Organise requests. Prioritise what matters. Keep campus support moving.*