
QUESTIONS = [
    {
        "question": "An unassigned open ticket is moved to in_progress. What should happen?",
        "options": {
            "A": "The transition succeeds",
            "B": "The transition is rejected",
            "C": "The ticket is deleted",
            "D": "The ticket becomes resolved",
        },
        "answer": "B",
    },
    {
        "question": "What is the resolution percentage when there are no tickets?",
        "options": {
            "A": "100.0",
            "B": "None",
            "C": "0.0",
            "D": "The report crashes",
        },
        "answer": "C",
    },
    {
        "question": "How should category and status filters work together?",
        "options": {
            "A": "Either filter can match",
            "B": "Both filters must match",
            "C": "Only the category matters",
            "D": "Filters are ignored",
        },
        "answer": "B",
    },
    {
        "question": "Can a resolved ticket receive a note before reopening?",
        "options": {
            "A": "Yes, always",
            "B": "Only if it is critical",
            "C": "No",
            "D": "Only if it has no assignee",
        },
        "answer": "C",
    },
    {
        "question": "What should loading JSON with duplicate ticket IDs do?",
        "options": {
            "A": "Reject the entire load",
            "B": "Silently delete one ticket",
            "C": "Merge the tickets",
            "D": "Change their priorities",
        },
        "answer": "A",
    },
    {
        "question": "Validation code changes but no negative tests are added. What is the best response?",
        "options": {
            "A": "Review and test invalid cases",
            "B": "Merge immediately",
            "C": "Delete the existing tests",
            "D": "Skip code review",
        },
        "answer": "A",
    },
]
# Replace the existing run_quiz() function in campusflow/engineering_quiz.py
# with this function. Keep the existing QUESTIONS list unchanged.
def run_quiz():
    score = 0
    completed = 0
    quit_early = False

    print("\\nENGINEERING UNDERSTANDING CHECK")
    print("Enter Q at any question to quit and return to the menu.")

    try:
        for number, question in enumerate(QUESTIONS, start=1):
            print(f"\\n{number}. {question['question']}")

            for letter, option in question["options"].items():
                print(f"  {letter}. {option}")

            while True:
                answer = input("Your answer (A/B/C/D or Q to quit): ").strip().upper()

                if answer == "Q":
                    quit_early = True
                    break

                if answer in ("A", "B", "C", "D"):
                    break

                print("Invalid choice. Enter A, B, C, D, or Q to quit.")

            if quit_early:
                break

            completed += 1
            if answer == question["answer"]:
                print("Correct!")
                score += 1
            else:
                print(f"Incorrect. Correct answer: {question['answer']}")

    except (KeyboardInterrupt, EOFError):
        # Treat Ctrl+C / closed input as a normal early exit.
        print("\\nQuiz interrupted. Returning to the menu.")
        quit_early = True

    if quit_early:
        print(f"\\nQuiz ended early. Score so far: {score}/{completed}.")
        return score

    print(f"\\nFinal score: {score}/{len(QUESTIONS)}")

    for number in range(1, 3):
        try:
            input(
                f"Explain one answer in your own words ({number}/2): "
            )
        except (KeyboardInterrupt, EOFError):
            print("\\nExplanation skipped.")
            break

    return score
