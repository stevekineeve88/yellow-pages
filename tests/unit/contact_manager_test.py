import unittest
from unittest.mock import patch, MagicMock
from modules.contact.data.contact_data import ContactData
from modules.contact.exceptions.contact_add_error import ContactAddError
from modules.contact.exceptions.contact_delete_error import ContactDeleteError
from modules.contact.exceptions.contact_parser_error import ContactParserError
from modules.contact.exceptions.contact_search_error import ContactSearchError
from modules.contact.exceptions.contact_update_error import ContactUpdateError
from modules.contact.managers.contact_manager import ContactManager
from modules.contact.managers.contact_type_manager import ContactTypeManager
from modules.contact.objects.contact import Contact
from modules.contact.objects.contact_type import ContactType
from modules.util.managers.postgres_conn_manager import PostgresConnManager
from modules.util.objects.data_list import DataList
from modules.util.objects.result import Result


class ContactManagerTest(unittest.TestCase):
    @classmethod
    @patch("modules.util.managers.postgres_conn_manager.PostgresConnManager")
    @patch("modules.contact.managers.contact_type_manager.ContactTypeManager")
    def setUpClass(cls, postgres_conn_manager, contact_type_manager) -> None:
        cls.postgres_conn_manager: PostgresConnManager = postgres_conn_manager
        cls.contact_type_manager: ContactTypeManager = contact_type_manager

        cls.type_phone = ContactType(1, "PHONE", "Phone")
        cls.type_email = ContactType(2, "EMAIL", "Email")
        cls.type_website = ContactType(3, "WEBSITE", "Website")
        cls.contact_type_manager.get_all = MagicMock(return_value=DataList(
            "TYPES",
            [cls.type_phone, cls.type_email, cls.type_website],
            "id",
            "const"
        ))

        cls.contact_manager: ContactManager = ContactManager(
            contact_data=ContactData(
                postgres_conn_manager=cls.postgres_conn_manager
            ),
            contact_type_manager=cls.contact_type_manager
        )

    def test_add_phone_returns_contact(self):
        self.__check_add(self.type_phone.get_id(), "+14445556666")

    def test_add_email_returns_contact(self):
        self.__check_add(self.type_email.get_id(), "email@website.com")

    def test_add_website_returns_contact(self):
        self.__check_add(self.type_website.get_id(), "http://google.com")

    def test_add_phone_fails_on_phone_parse_error(self):
        self.__check_error_add(self.type_phone.get_id(), "+13333334445555")

    def test_add_email_fails_on_email_parse_error(self):
        self.__check_error_add(self.type_email.get_id(), "@website.com")

    def test_add_website_fails_on_website_parse_error(self):
        self.__check_error_add(self.type_website.get_id(), "example.com")

    def test_add_fails_on_add_error(self):
        self.postgres_conn_manager.insert = MagicMock(return_value=Result(False))
        self.postgres_conn_manager.select = MagicMock(return_value=Result(True))
        with self.assertRaises(ContactAddError):
            self.contact_manager.add(
                1,
                type_id=self.type_phone.get_id(),
                info="+19998884444"
            )
            self.fail("Did not fail")
        self.postgres_conn_manager.insert.assert_called_once()
        self.postgres_conn_manager.select.assert_not_called()

    def test_get_fails_on_search_error(self):
        self.postgres_conn_manager.select = MagicMock(return_value=Result(False))
        with self.assertRaises(ContactSearchError):
            self.contact_manager.get(1)
            self.fail("Did not fail")

    def test_update_updates_contact(self):
        contact = Contact(
            id=1,
            entity_id=123,
            type=self.type_phone,
            info="+19998887777",
            description="Some Description"
        )
        self.postgres_conn_manager.query = MagicMock(return_value=Result(True))
        try:
            self.contact_manager.update(contact)
            self.postgres_conn_manager.query.assert_called_once()
        except Exception as e:
            self.fail(str(e))

    def test_update_fails_on_parse_error(self):
        contact = Contact(
            id=1,
            entity_id=123,
            type=self.type_email,
            info="+19998887777",
            description="Some Description"
        )
        self.postgres_conn_manager.query = MagicMock(return_value=Result(True))
        with self.assertRaises(ContactParserError):
            self.contact_manager.update(contact)
            self.fail("Did not fail")
        self.postgres_conn_manager.query.assert_not_called()

    def test_update_fails_on_update_error(self):
        contact = Contact(
            id=1,
            entity_id=123,
            type=self.type_phone,
            info="+19998887777",
            description="Some Description"
        )
        self.postgres_conn_manager.query = MagicMock(return_value=Result(False))
        with self.assertRaises(ContactUpdateError):
            self.contact_manager.update(contact)
            self.fail("Did not fail")

    def test_delete_deletes_contact(self):
        self.postgres_conn_manager.query = MagicMock(return_value=Result(True))
        try:
            self.contact_manager.delete(1)
        except Exception as e:
            self.fail(str(e))

    def test_delete_fails_on_delete_error(self):
        self.postgres_conn_manager.query = MagicMock(return_value=Result(False))
        with self.assertRaises(ContactDeleteError):
            self.contact_manager.delete(1)
            self.fail("Did not fail")
        self.postgres_conn_manager.query.assert_called_once()

    def test_get_by_entity_id_gets_contacts(self):
        entity_id = 2
        contacts = [
            {
                "id": 1,
                "entity_id": entity_id,
                "type_id": self.type_email.get_id(),
                "info": "example@website.com",
                "description": "Some description"
            },
            {
                "id": 2,
                "entity_id": entity_id,
                "type_id": self.type_phone.get_id(),
                "info": "+19998887777",
                "description": "Some description"
            }
        ]
        self.postgres_conn_manager.select = MagicMock(return_value=Result(True, "", contacts))
        contact_objs = self.contact_manager.get_by_entity_id(entity_id)
        self.assertEqual(len(contacts), len(contact_objs))
        for i in range(0, len(contacts)):
            contact_dict_item = contacts[i]
            contact_obj_item: Contact = contact_objs[i]
            self.assertEqual(contact_dict_item["id"], contact_obj_item.get_id())
            self.assertTrue(entity_id == contact_obj_item.get_entity_id() and entity_id == contact_dict_item["entity_id"])
            self.assertEqual(contact_dict_item["type_id"], contact_obj_item.get_type().get_id())
            self.assertEqual(contact_dict_item["info"], contact_obj_item.get_info())
            self.assertEqual(contact_dict_item["description"], contact_obj_item.get_description())

    def test_get_by_entity_id_fails_on_search_error(self):
        self.postgres_conn_manager.select = MagicMock(return_value=Result(False))
        with self.assertRaises(ContactSearchError):
            self.contact_manager.get_by_entity_id(2)
            self.fail("Did not fail")
        self.postgres_conn_manager.select.assert_called_once()

    def __check_add(self, type_id, info: str):
        """ Check add successful
        Args:
            type_id (ID):
            info (str):
        """
        contact_id = 1
        entity_id = 123
        description = "Owner"

        result = Result(True)
        result.set_insert_id(contact_id)
        self.postgres_conn_manager.insert = MagicMock(return_value=result)
        self.postgres_conn_manager.select = MagicMock(return_value=Result(
            True,
            "",
            [{
                "id": contact_id,
                "entity_id": entity_id,
                "type_id": type_id,
                "info": info,
                "description": description
            }]
        ))
        contact = self.contact_manager.add(
            entity_id,
            type_id=type_id,
            info=info,
            description=description
        )

        self.postgres_conn_manager.insert.assert_called_once()
        self.postgres_conn_manager.select.assert_called_once()
        self.assertEqual(contact_id, contact.get_id())
        self.assertEqual(entity_id, contact.get_entity_id())
        self.assertEqual(type_id, contact.get_type().get_id())
        self.assertEqual(info, contact.get_info())
        self.assertEqual(description, contact.get_description())

    def __check_error_add(self, type_id, info: str):
        """ Check error on add
        Args:
            type_id (ID):
            info (str):
        """
        self.postgres_conn_manager.insert = MagicMock(return_value=Result(True))
        self.postgres_conn_manager.select = MagicMock(return_value=Result(True))
        with self.assertRaises(ContactParserError):
            self.contact_manager.add(
                123,
                type_id=type_id,
                info=info,
                description="Some description"
            )
            self.fail("Did not fail")
        self.postgres_conn_manager.insert.assert_not_called()
        self.postgres_conn_manager.select.assert_not_called()
