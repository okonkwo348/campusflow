# 🎓 CampusFlow

### A Simple Campus Helpdesk and Ticket Management System

**CampusFlow** is a Python command-line application designed to help manage campus IT support requests. It allows users to create and track support tickets, assign responsibility, manage ticket progress, prioritize urgent issues, and generate reports.

The project demonstrates practical software engineering principles, including input validation, modular design, JSON data persistence, automated testing, and collaborative Git workflows.

---

## 👥 Our Team

| No. | Team Member | Role / Contribution |
|---|---|---|
| 1 | **[OKONKWO EMMANUEL CHISOM]** | [Project lead / Ticket creation] |
| 2 | **[MUHAMMED MARYAM]** | [Workflow and status management] |
| 3 | **[CHRISTAIN PATRICK]** | [Data persistence and storage] |


**Team / Group Name:** [Enter team name]

**Course / Institution:** [Enter course or institution]

**Project Repository:** [Insert GitHub repository URL]

*Update the table to reflect your actual team members and their contributions.*

---

## 🎯 Project Objectives

CampusFlow aims to:

- Simplify the recording and tracking of campus IT support requests.
- Prioritize tickets according to urgency and the number of affected users.
- Ensure tickets follow a controlled assignment and resolution workflow.
- Preserve ticket records between application sessions.
- Provide useful summaries of ticket statuses and priorities.
- Encourage clean code, automated testing, and collaborative development.

## ✨ Features

### 1. Ticket creation
Create support tickets with a title, category, urgency, and number of affected users.

### 2. Automatic priority calculation
Tickets receive a priority based on urgency and the number of affected users.

| Priority | Rule |
|---|---|
| Critical | High urgency and at least 10 affected users |
| High | High urgency or at least 10 affected users, unless critical |
| Medium | Medium urgency or at least 3 affected users, unless a higher priority applies |
| Low | Low urgency and fewer than 3 affected users |

### 3. Ticket assignment
Assign tickets to a responsible support person or team before work begins.

### 4. Status management
Track ticket progress through the supported workflow:

`Open → In Progress → Resolved`

The workflow prevents tickets from being resolved directly from the open state and requires assignment before work begins.

### 5. Prioritized work queue
View active tickets in priority order, with ticket ID used to break ties.

### 6. Reports
Generate summaries of the total number of tickets, their statuses, and their priority levels.

### 7. JSON persistence
Save tickets to a JSON file and reload them when the application starts, preserving records between sessions.

### 8. Automated tests
Use Python's built-in `unittest` framework to verify business rules, workflow transitions, validation, reporting, and persistence.

---

## 🛠️ Technology Stack

- **Language:** Python 3
- **Data storage:** JSON
- **Automated testing:** `unittest`
- **Version control:** Git
- **Collaboration and code review:** GitHub

CampusFlow uses Python's standard library and does not require a web framework, external database, AI SDK, or API key.

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
│   └── reports.py
├── tests/
│   ├── test_tickets.py
│   ├── test_workflow.py
│   ├── test_storage.py
│   └── test_reports.py
└── docs/
    ├── ai-learning-log.md
    └── design-decisions.md
```

**Module responsibilities**

- `main.py` — command-line interface and application loop.
- `tickets.py` — ticket creation, validation, priority calculation, and ticket lookup.
- `workflow.py` — assignment, status transitions, and queue construction.
- `storage.py` — loading and saving ticket data in JSON format.
- `reports.py` — ticket summaries and reporting.
- `tests/` — automated tests for application behaviour.
- `docs/` — design decisions and the team's AI learning records.

The JSON data file is created or used at runtime and should not be committed if it contains local application data.

---

## 🚀 Getting Started

### Prerequisites

Install Python 3. Confirm that Python is available:

```bash
python3 --version
```

Git is recommended if you want to clone the repository and contribute.

### 1. Clone the repository

Replace the placeholder with your actual GitHub repository URL.

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Run the application

From the project root directory:

```bash
python3 main.py
```

Follow the menu prompts to create tickets, assign them, update their statuses, view the queue, generate reports, save data, or exit.

### 3. Run the automated tests

From the project root directory:

```bash
python3 -m unittest discover -s tests -v
```

Review the output and confirm that all tests pass before submitting changes.

---

## 🧪 Testing and Quality Assurance

The team uses automated tests to check expected behaviour and guard against regressions.

Important scenarios include:

- Creating tickets with valid information.
- Rejecting blank titles and invalid affected-user counts.
- Calculating the correct priority at boundary values.
- Preventing unassigned tickets from entering the in-progress state.
- Enforcing valid status transitions.
- Ordering tickets correctly in the work queue.
- Producing correct reports for populated and empty ticket collections.
- Saving and reloading tickets without losing records or duplicating IDs.
- Handling missing or malformed JSON data appropriately.

Run the test suite after implementing a feature or reviewing a teammate's changes.

---

## 🤝 Team Workflow

We use Git and GitHub to coordinate development and review changes.

1. Agree on the feature and its acceptance criteria.
2. Create a feature branch from the latest `main`.
3. Implement the change and add relevant tests.
4. Run the test suite and inspect the changes.
5. Push the branch and open a pull request.
6. Ask a teammate to review the implementation.
7. Merge only after the required review and checks are complete.

**Team principles**

- Keep `main` stable.
- Do not commit directly to `main`.
- Make small, focused commits.
- Review code and tests, not just commit messages.
- Never commit passwords, tokens, or private configuration.
- Document important decisions and genuine learning experiences.

---

## 📚 Learning and Documentation

CampusFlow is also a collaborative learning project. Team members should understand the code they contribute, test their assumptions, and be able to explain their technical decisions.

Project documentation:

- `docs/design-decisions.md` — agreed architecture, behaviour, and function contracts.
- `docs/ai-learning-log.md` — individual AI-assisted learning, experiments, verification, and lessons learned.

AI assistance should support understanding and experimentation, not replace independent reasoning, implementation, or verification.

---

## 🔮 Future Improvements

Possible extensions, depending on project scope and team capacity:

- Search and filter tickets.
- Add ticket descriptions, timestamps, and resolution notes.
- Track assignment history.
- Export reports to CSV.
- Add a graphical or web-based interface.
- Introduce user authentication and role-based permissions.

These are potential future enhancements, not claims about existing functionality.

---

## 📌 Project Status

CampusFlow has implemented its core ticket-management modules and automated tests. The reported test suite has passed, but the complete interactive workflow and persistence across application restarts should also be verified before declaring the project fully complete.

---

## 📄 License

No license has been selected yet. Add a license if the team intends to publish or distribute the project, after agreeing on the appropriate terms.

---

**Built collaboratively by the CampusFlow team.**

*Organize requests. Prioritize what matters. Keep campus support moving.*
