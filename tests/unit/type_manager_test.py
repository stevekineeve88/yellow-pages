import unittest
from unittest.mock import patch, MagicMock
from modules.tag.data.tag_type_data import TagTypeData
from modules.tag.exceptions.tag_type_error import TagTypeError
from modules.tag.managers.tag_type_manager import TagTypeManager
from modules.util.managers.postgres_conn_manager import PostgresConnManager
from modules.util.objects.result import Result


class TypeManagerTest(unittest.TestCase):
    @classmethod
    @patch("modules.util.managers.postgres_conn_manager.PostgresConnManager")
    def setUpClass(cls, postgres_conn_manager) -> None:
        cls.postgres_conn_manager: PostgresConnManager = postgres_conn_manager
        cls.type_manager: TagTypeManager = TagTypeManager(
            tag_type_data=TagTypeData(
                postgres_conn_manager=cls.postgres_conn_manager
            )
        )

    def test_get_all_returns_all_types(self):
        type_1 = {
            "id": 1,
            "const": "RESTAURANT",
            "description": "Description 1"
        }
        type_2 = {
            "id": 2,
            "const": "BAR",
            "description": "Description 2"
        }

        self.postgres_conn_manager.select = MagicMock(return_value=Result(
            True,
            "",
            [type_1, type_2]
        ))

        statuses = self.type_manager.get_all()
        self.assertEqual(type_1["id"], statuses.RESTAURANT.get_id())
        self.assertEqual(type_1["const"], statuses.RESTAURANT.get_const())
        self.assertEqual(type_1["description"], statuses.RESTAURANT.get_description())

        self.assertEqual(type_2["id"], statuses.BAR.get_id())
        self.assertEqual(type_2["const"], statuses.BAR.get_const())
        self.assertEqual(type_2["description"], statuses.BAR.get_description())

    def test_get_all_fails_on_type_error(self):
        self.postgres_conn_manager.select = MagicMock(return_value=Result(False))
        with self.assertRaises(TagTypeError):
            self.type_manager.get_all()
            self.fail("Did not fail")
        self.postgres_conn_manager.select.assert_called_once()
