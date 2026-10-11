import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from campusflow.storage import load_tickets, save_tickets


class StorageTests(unittest.TestCase):
    def test_missing_file_loads_as_empty_list(self):
        with TemporaryDirectory() as temporary_folder:
            file_path = Path(temporary_folder) / "tickets.json"

            self.assertEqual(load_tickets(file_path), [])

    def test_saved_tickets_can_be_loaded_again(self):
        tickets = [
            {
                "id": "T001",
                "title": "Campus Wi-Fi is down",
                "category": "Network",
                "urgency": "high",
                "affected_users": 12,
                "priority": "critical",
                "status": "open",
                "assigned_to": None,
            }
        ]

        with TemporaryDirectory() as temporary_folder:
            file_path = Path(temporary_folder) / "data" / "tickets.json"

            save_tickets(tickets, file_path)

            self.assertTrue(file_path.exists())
            self.assertEqual(load_tickets(file_path), tickets)

    def test_invalid_json_is_rejected(self):
        with TemporaryDirectory() as temporary_folder:
            file_path = Path(temporary_folder) / "tickets.json"
            file_path.write_text("{not valid json", encoding="utf-8")

            with self.assertRaises(ValueError):
                load_tickets(file_path)


if __name__ == "__main__":
    unittest.main()