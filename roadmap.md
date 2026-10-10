
# PROJECT STRUCTURE

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
│   └── test_storage.py
└── docs/
    ├── ai-learning-log.md
    └── design-decisions.md


# ticket.py

**For a ticket**

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

***function***:
	->id: function that automatically create ticket ID number to 	 		avoid 	user's error
	-> "title: request for a title and insist it can't be blank
	-> category: function that tells the user to select among the 			issues(Network, Hardware, Software, Other)
	-> urgency: function that ask the user how severe the issue is 
		(low, medium, high) 
	-> affected_users: Error Handling to accept  positive integer 			(not zero, a negative number, a decimal, or text)
	-> priority: function that calculate for priority.
		RULE 1   high urgency AND 10 or more affected users  →  			critical
		RULE 2   high urgency OR 10 or more affected users    →  			high
		RULE 3   medium urgency OR 3 or more affected users   →  			medium
		RULE 4   all remaining valid tickets                  →  			low

	-> status: function t hat tells the user to select open or			close
	-> assigned_to: receive name

 
# FEATURE ONE: CREATE TICKET

• Ticket IDs are unique and automatically generated (T001, T002, T003, …).
• Allowed categories: Network, Hardware, Software, Other.
• Allowed urgency levels: low, medium, high.
• Title must not be blank. affected_users must be a positive integer (not zero, a negative number, a decimal, or text).
• Accept and normalize valid case variations consistently
  display useful errors for invalid input

 Calculate priority exactly as specified
Your function must check the following rules IN THIS ORDER and apply the first match:
RULE 1   high urgency AND 10 or more affected users  →  critical
RULE 2   high urgency OR 10 or more affected users    →  high
RULE 3   medium urgency OR 3 or more affected users   →  medium
RULE 4   all remaining valid tickets 


# FEATURE TWO: PERSISTENCE  - storage.py

*functions that*:
-> save list of dictionaries into a json file
-> load this list of dictionaries from a json file

*Error Handling*:
-> Missing file should allow a fresh start;
-> malformed JSON should produce a clear error rather than silently erase data. 
-> IDs must remain unique after reload.

we must find a way to make sure a dict after loading is save in a file and when creating a ticket the function check the last dict's ID in the list 


                 →  low


#  FEATURE THREE REPORTS
-> Show total tickets and breakdowns by status and priority; handle zero tickets correctly.

# # FEATURE FOUR: LIST / VIEW
A function:
-> that list all tickets and select one for mor detail

# FEATURE FIVE: WORKFLOW: 
Support open → in_progress → resolved. Do not move an unassigned ticket into in_progress. A resolved ticket may only be modified after an explicit reopen that sets it to open.

# FEATURE SIX: WORK QUEUE: 
Show open, unresolved tickets in critical → high → medium → low order; break priority ties using the earlier numeric ticket ID.


# FEATURE SEVEN: ASSIGN: 
Assign a ticket to a non-empty staff member name; reject unknown ticket IDs.


# MAIN

seven features as the CLI menu
*Error Handling*:
Invalid inputs and transitions are rejected WITHOUT corrupting stored tickets.
Tickets survive a restart using JSON
At least eight meaningful automated tests pass on the integrated main branch