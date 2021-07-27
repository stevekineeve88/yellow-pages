import unittest
from unittest.mock import patch, MagicMock
from modules.contact.data.contact_type_data import ContactTypeData
from modules.contact.exceptions.contact_type_error import ContactTypeError
from modules.contact.managers.contact_type_manager import ContactTypeManager
from modules.util.managers.postgres_conn_manager import PostgresConnManager
from modules.util.objects.result import Result


class ContactTypeManagerTest(unittest.TestCase):
    @classmethod
    @patch("modules.util.managers.postgres_conn_manager.PostgresConnManager")
    def setUpClass(cls, postgres_conn_manager) -> None:
        cls.postgres_conn_manager: PostgresConnManager = postgres_conn_manager
        cls.contact_type_manager: ContactTypeManager = ContactTypeManager(
            contact_type_data=ContactTypeData(
                postgres_conn_manager=cls.postgres_conn_manager
            )
        )

    def test_get_all_returns_all_types(self):
        type_1 = {
            "id": 1,
            "const": "PHONE",
            "description": "Phone Type"
        }
        type_2 = {
            "id": 2,
            "const": "EMAIL",
            "description": "Email Type"
        }
        self.postgres_conn_manager.select = MagicMock(return_value=Result(True, "", [
            type_1,
            type_2
        ]))
        types = self.contact_type_manager.get_all()
        self.assertEqual(type_1["id"], types.PHONE.get_id())
        self.assertEqual(type_1["const"], types.PHONE.get_const())
        self.assertEqual(type_1["description"], types.PHONE.get_description())

        self.assertEqual(type_2["id"], types.EMAIL.get_id())
        self.assertEqual(type_2["const"], types.EMAIL.get_const())
        self.assertEqual(type_2["description"], types.EMAIL.get_description())

    def test_get_all_fails_on_type_error(self):
        self.postgres_conn_manager.select = MagicMock(return_value=Result(False))
        with self.assertRaises(ContactTypeError):
            self.contact_type_manager.get_all()
            self.fail("Did not fail")
        self.postgres_conn_manager.select.assert_called_once()
