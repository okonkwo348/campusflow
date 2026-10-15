import unittest

from campusflow.tickets import (
    validate_title,
    validate_category,
    validate_urgency,
    validate_affected_users,
    calculate_priority,
    generate_ticket_id,
    find_ticket,
    create_ticket,
    validate_ticket,
)


class TestValidateTitle(unittest.TestCase):

    def test_valid_title(self):
        self.assertEqual(validate_title("Wi-Fi is down"), "Wi-Fi is down")

    def test_title_is_trimmed(self):
        self.assertEqual(validate_title("  Wi-Fi is down  "), "Wi-Fi is down")

    def test_blank_title_raises_error(self):
        for title in ("", "   "):
            with self.subTest(title=title):
                with self.assertRaises(ValueError):
                    validate_title(title)

    def test_non_string_title_raises_error(self):
        with self.assertRaises(ValueError):
            validate_title(123)


class TestValidateCategory(unittest.TestCase):

    def test_valid_categories(self):
        categories = ["Network", "Hardware", "Software", "Other"]

        for category in categories:
            with self.subTest(category=category):
                self.assertEqual(validate_category(category), category)

    def test_category_is_normalized(self):
        self.assertEqual(validate_category(" network "), "Network")
        self.assertEqual(validate_category("HARDWARE"), "Hardware")

    def test_invalid_category_raises_error(self):
        with self.assertRaises(ValueError):
            validate_category("Printer")

    def test_non_string_category_raises_error(self):
        with self.assertRaises(ValueError):
            validate_category(123)


class TestValidateUrgency(unittest.TestCase):

    def test_valid_urgencies(self):
        for urgency in ("low", "medium", "high"):
            with self.subTest(urgency=urgency):
                self.assertEqual(validate_urgency(urgency), urgency)

    def test_urgency_is_normalized(self):
        self.assertEqual(validate_urgency(" HIGH "), "high")
        self.assertEqual(validate_urgency("MEDIUM"), "medium")

    def test_invalid_urgency_raises_error(self):
        with self.assertRaises(ValueError):
            validate_urgency("urgent")

    def test_non_string_urgency_raises_error(self):
        with self.assertRaises(ValueError):
            validate_urgency(123)


class TestValidateAffectedUsers(unittest.TestCase):

    def test_positive_integer_is_accepted(self):
        self.assertEqual(validate_affected_users(5), 5)

    def test_zero_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_affected_users(0)

    def test_negative_integer_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_affected_users(-3)

    def test_non_integer_is_rejected(self):
        for count in ("five", 3.5, True, False, None):
            with self.subTest(count=count):
                with self.assertRaises(ValueError):
                    validate_affected_users(count)


class TestCalculatePriority(unittest.TestCase):

    def test_critical_priority(self):
        self.assertEqual(calculate_priority("high", 10), "critical")
        self.assertEqual(calculate_priority("high", 15), "critical")

    def test_high_priority(self):
        self.assertEqual(calculate_priority("high", 2), "high")
        self.assertEqual(calculate_priority("low", 10), "high")

    def test_medium_priority(self):
        self.assertEqual(calculate_priority("medium", 1), "medium")
        self.assertEqual(calculate_priority("low", 3), "medium")

    def test_low_priority(self):
        self.assertEqual(calculate_priority("low", 1), "low")
        self.assertEqual(calculate_priority("low", 2), "low")

    def test_invalid_urgency_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_priority("urgent", 5)

    def test_invalid_user_count_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_priority("high", 0)


class TestGenerateTicketId(unittest.TestCase):

    def test_empty_list_starts_at_t001(self):
        self.assertEqual(generate_ticket_id([]), "T001")

    def test_next_sequential_id(self):
        tickets = [{"id": "T001"}, {"id": "T002"}]
        self.assertEqual(generate_ticket_id(tickets), "T003")

    def test_unsorted_ids_use_highest_number(self):
        tickets = [
            {"id": "T001"},
            {"id": "T010"},
            {"id": "T003"},
        ]
        self.assertEqual(generate_ticket_id(tickets), "T011")

    def test_ids_beyond_three_digits(self):
        tickets = [{"id": "T999"}]
        self.assertEqual(generate_ticket_id(tickets), "T1000")


class TestFindTicket(unittest.TestCase):

    def setUp(self):
        self.ticket = {"id": "T001", "title": "Wi-Fi is down"}
        self.tickets = [self.ticket]

    def test_existing_ticket_is_returned(self):
        result = find_ticket(self.tickets, "T001")
        self.assertIs(result, self.ticket)

    def test_unknown_ticket_raises_lookup_error(self):
        with self.assertRaises(LookupError):
            find_ticket(self.tickets, "T999")


class TestCreateTicket(unittest.TestCase):

    def setUp(self):
        self.tickets = []

    def test_create_ticket_with_correct_fields(self):
        ticket = create_ticket(
            self.tickets, "Wi-Fi is down", "Network", "high", 15
        )

        self.assertEqual(ticket, {
            "id": "T001",
            "title": "Wi-Fi is down",
            "category": "Network",
            "urgency": "high",
            "affected_users": 15,
            "priority": "critical",
            "status": "open",
            "assigned_to": None,
            "notes": [],
        })

    def test_ticket_is_appended_exactly_once(self):
        ticket = create_ticket(
            self.tickets, "Broken laptop", "Hardware", "medium", 2
        )

        self.assertEqual(len(self.tickets), 1)
        self.assertIs(self.tickets[0], ticket)

    def test_ticket_fields_are_normalized(self):
        ticket = create_ticket(
            self.tickets, "  Wi-Fi down  ", " network ", " HIGH ", 15
        )

        self.assertEqual(ticket["title"], "Wi-Fi down")
        self.assertEqual(ticket["category"], "Network")
        self.assertEqual(ticket["urgency"], "high")

    def test_invalid_input_does_not_modify_list(self):
        with self.assertRaises(ValueError):
            create_ticket(
                self.tickets, "Wi-Fi down", "Printer", "high", 15
            )

        self.assertEqual(self.tickets, [])

    def test_each_new_ticket_gets_unique_id(self):
        create_ticket(self.tickets, "Wi-Fi down", "Network", "high", 15)
        second = create_ticket(
            self.tickets, "Broken laptop", "Hardware", "low", 1
        )

        self.assertEqual(second["id"], "T002")
        self.assertEqual(len(self.tickets), 2)


class TestValidateTicket(unittest.TestCase):

    def setUp(self):
        self.ticket = {
            "id": "T001", "title": "Wi-Fi is down", "category": "Network",
            "urgency": "high", "affected_users": 15, "priority": "critical",
            "status": "open", "assigned_to": None, "notes": [],
        }

    def test_valid_ticket_passes(self):
        self.assertIsNone(validate_ticket(self.ticket))

    def test_created_ticket_passes_validation(self):
        tickets = []
        ticket = create_ticket(tickets, "Broken laptop", "hardware", "low", 1)
        validate_ticket(ticket)

    def test_invalid_values_are_rejected(self):
        bad_values = [
            ("category", "Banana"),
            ("affected_users", True),
            ("affected_users", 2.5),
            ("priority", "low"),
            ("title", "   "),
            ("status", "pending"),
        ]
        for field, value in bad_values:
            with self.subTest(field=field, value=value):
                bad = dict(self.ticket)
                bad[field] = value
                with self.assertRaises(ValueError):
                    validate_ticket(bad)

    def test_unassigned_in_progress_ticket_is_rejected(self):
        self.ticket["status"] = "in_progress"
        with self.assertRaises(ValueError):
            validate_ticket(self.ticket)


if __name__ == "__main__":
    unittest.main()