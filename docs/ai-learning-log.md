# Final Individual Reflection — CampusFlow

### 1. Which feature did you personally implement, and how do you know it works?

I personally implemented the ticket workflow functionality in `campusflow/workflow.py`. This included assigning tickets to staff members, managing ticket status transitions, and building a work queue that sorts tickets by priority and numeric ticket ID while excluding resolved tickets.

I also wrote automated tests in `tests/test_workflow.py` to verify the functionality, including valid and invalid operations. I ran the test suite using `python3 -m unittest discover -s tests -v`, and all 15 tests passed.

### 2. What did AI teach you that you did not understand at the start?

AI helped me understand how to break a programming task into smaller steps and translate requirements into working Python functions. I learned how to validate inputs, raise appropriate exceptions, enforce permitted status transitions, and use `sorted()` with a custom sorting key to organize tickets by priority and numeric ID.

I also learned that passing tests is important, but tests must cover the actual project requirements to give confidence that the implementation is correct.

### 3. Give one example where you verified, changed, or rejected an AI suggestion.

One example was testing the ticket queue's sorting behavior. I already had tests that checked priority ordering, but I added another test to verify that ticket `T002` appears before `T010` when their priorities are equal. This helped me verify that the queue sorts by the numeric part of the ticket ID rather than treating the IDs as ordinary text.

I ran the automated tests again and confirmed that all 15 tests passed.

### 4. What did you learn from reviewing your partner's PR?

Reviewing my partner's pull request helped me understand the importance of integrating different parts of a shared project consistently. I learned to check whether code follows the agreed interface contract, uses the expected function names and return values, and works with the other modules.

It also showed me that code review is not just about finding errors; it is about making sure individual contributions work together as one application.

### 5. What would you improve next if the team had another hour?

If the team had another hour, I would focus on integration testing the complete application. I would verify that ticket creation, assignment, status changes, queue generation, reporting, and saving and loading tickets work together correctly. I would also test more edge cases, such as invalid input and unexpected file errors, to improve the application's reliability.
