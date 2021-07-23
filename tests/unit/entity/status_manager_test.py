import unittest
from unittest.mock import patch, MagicMock
from modules.entity.data.status_data import StatusData
from modules.entity.exceptions.entity_status_error import EntityStatusError
from modules.entity.managers.status_manager import StatusManager
from modules.util.managers.postgres_conn_manager import PostgresConnManager
from modules.util.objects.result import Result


class StatusManagerTest(unittest.TestCase):
    @classmethod
    @patch("modules.util.managers.postgres_conn_manager.PostgresConnManager")
    def setUpClass(cls, postgres_conn_manager) -> None:
        cls.postgres_conn_manager: PostgresConnManager = postgres_conn_manager
        cls.status_manager: StatusManager = StatusManager(
            status_data=StatusData(
                postgres_conn_manager=cls.postgres_conn_manager
            )
        )

    def test_get_all_returns_all_statuses(self):
        status_1 = {
            "id": 1,
            "const": "STATUS1",
            "description": "Description 1"
        }
        status_2 = {
            "id": 2,
            "const": "STATUS2",
            "description": "Description 2"
        }

        self.postgres_conn_manager.select = MagicMock(return_value=Result(
            True,
            "",
            [status_1, status_2]
        ))

        statuses = self.status_manager.get_all()
        self.assertEqual(status_1["id"], statuses.STATUS1.get_id())
        self.assertEqual(status_1["const"], statuses.STATUS1.get_const())
        self.assertEqual(status_1["description"], statuses.STATUS1.get_description())

        self.assertEqual(status_2["id"], statuses.STATUS2.get_id())
        self.assertEqual(status_2["const"], statuses.STATUS2.get_const())
        self.assertEqual(status_2["description"], statuses.STATUS2.get_description())

    def test_get_all_fails_on_status_error(self):
        self.postgres_conn_manager.select = MagicMock(return_value=Result(False))
        with self.assertRaises(EntityStatusError):
            self.status_manager.get_all()
            self.fail("Did not fail")
        self.postgres_conn_manager.select.assert_called_once()
