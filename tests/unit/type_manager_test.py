import unittest
from unittest.mock import patch, MagicMock
from modules.entity.data.type_data import TypeData
from modules.entity.managers.type_manager import TypeManager
from modules.util.managers.postgres_conn_manager import PostgresConnManager
from modules.util.objects.result import Result


class TypeManagerTest(unittest.TestCase):
    @classmethod
    @patch("modules.util.managers.postgres_conn_manager.PostgresConnManager")
    def setUpClass(cls, postgres_conn_manager) -> None:
        cls.postgres_conn_manager: PostgresConnManager = postgres_conn_manager
        cls.type_manager: TypeManager = TypeManager(
            type_data=TypeData(
                postgres_conn_manager=cls.postgres_conn_manager
            )
        )

    def test_get_all_returns_all_types(self):
        type_1 = {
            "id": 1,
            "const": "TYPE1",
            "description": "Description 1"
        }
        type_2 = {
            "id": 2,
            "const": "TYPE2",
            "description": "Description 2"
        }

        self.postgres_conn_manager.select = MagicMock(return_value=Result(
            True,
            "",
            [type_1, type_2]
        ))

        types = self.type_manager.get_all()
        self.assertEqual(type_1["id"], types.TYPE1.get_id())
        self.assertEqual(type_1["const"], types.TYPE1.get_const())
        self.assertEqual(type_1["description"], types.TYPE1.get_description())

        self.assertEqual(type_2["id"], types.TYPE2.get_id())
        self.assertEqual(type_2["const"], types.TYPE2.get_const())
        self.assertEqual(type_2["description"], types.TYPE2.get_description())
