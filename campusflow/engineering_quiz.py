
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


def run_quiz():
    score = 0

    print("\nENGINEERING UNDERSTANDING CHECK")

    for number, question in enumerate(QUESTIONS, start=1):
        print(f"\n{number}. {question['question']}")

        for letter, option in question["options"].items():
            print(f"  {letter}. {option}")

        while True:
            answer = input("Your answer (A/B/C/D): ").strip().upper()

            if answer in ("A", "B", "C", "D"):
                break

            print("Invalid choice. Enter A, B, C, or D.")

        if answer == question["answer"]:
            print("Correct!")
            score += 1
        else:
            print(f"Incorrect. Correct answer: {question['answer']}")

    print(f"\nFinal score: {score}/{len(QUESTIONS)}")

    for number in range(1, 3):
        input(
            f"Explain one answer in your own words "
            f"({number}/2): "
        )

    return score
