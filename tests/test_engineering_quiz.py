
import unittest
from unittest.mock import patch

from campusflow.engineering_quiz import run_quiz


class TestEngineeringQuiz(unittest.TestCase):
    @patch("builtins.input", side_effect=[
        "X", "B",       # Q1: invalid, then correct
        "C",            # Q2
        "B",            # Q3
        "C",            # Q4
        "A",            # Q5
        "A",            # Q6
        "First explanation",
        "Second explanation",
    ])
    def test_invalid_answer_retries_and_score_is_correct(self, mocked_input):
        score = run_quiz()

        self.assertEqual(score, 6)
        self.assertEqual(mocked_input.call_count, 9)

    @patch("builtins.input", side_effect=[
        "A", "A", "A", "A", "A", "B",
        "Explanation one",
        "Explanation two",
    ])
    def test_incorrect_answers_reduce_score(self, mocked_input):
        score = run_quiz()
        self.assertEqual(score, 0)


if __name__ == "__main__":
    unittest.main()
