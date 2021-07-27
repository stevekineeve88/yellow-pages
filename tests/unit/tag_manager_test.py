import unittest
from unittest.mock import patch, MagicMock
from modules.tag.data.tag_data import TagData
from modules.tag.exceptions.tag_add_error import TagAddError
from modules.tag.exceptions.tag_delete_error import TagDeleteError
from modules.tag.exceptions.tag_search_error import TagSearchError
from modules.tag.managers.tag_manager import TagManager
from modules.tag.managers.tag_type_manager import TagTypeManager
from modules.tag.objects.tag import Tag
from modules.tag.objects.tag_type import TagType
from modules.util.managers.postgres_conn_manager import PostgresConnManager
from modules.util.objects.data_list import DataList
from modules.util.objects.result import Result


class TagManagerTest(unittest.TestCase):
    @classmethod
    @patch("modules.util.managers.postgres_conn_manager.PostgresConnManager")
    @patch("modules.tag.managers.tag_type_manager.TagTypeManager")
    def setUpClass(cls, postgres_conn_manager, type_manager) -> None:
        cls.postgres_conn_manager: PostgresConnManager = postgres_conn_manager
        cls.type_manager: TagTypeManager = type_manager

        cls.type_restaurant = TagType(1, "RESTAURANT", "Restaurant")
        cls.type_manager.get_all = MagicMock(return_value=DataList(
            "TYPES",
            [cls.type_restaurant],
            "id",
            "const"
        ))
        cls.tag_manager: TagManager = TagManager(
            tag_data=TagData(
                postgres_conn_manager=cls.postgres_conn_manager
            ),
            tag_type_manager=cls.type_manager
        )

    def test_add_adds_tag_successfully(self):
        tag_id = 1
        entity_id = 2
        type_id = self.type_restaurant.get_id()

        result = Result(True)
        result.set_insert_id(tag_id)
        self.postgres_conn_manager.insert = MagicMock(return_value=result)
        tag = self.tag_manager.add(entity_id, type_id)
        self.postgres_conn_manager.insert.assert_called_once()
        self.assertEqual(tag_id, tag.get_id())
        self.assertEqual(entity_id, tag.get_entity_id())
        self.assertEqual(type_id, tag.get_type().get_id())

    def test_add_fails_on_add_error(self):
        self.postgres_conn_manager.insert = MagicMock(return_value=Result(False))
        with self.assertRaises(TagAddError):
            self.tag_manager.add(1, 1)
            self.fail("Did not fail")
        self.postgres_conn_manager.insert.assert_called_once()

    def test_get_gets_tag(self):
        tag_data = {
            "id": 1,
            "entity_id": 2,
            "type_id": self.type_restaurant.get_id()
        }
        self.postgres_conn_manager.select = MagicMock(return_value=Result(True, "", [tag_data]))
        tag = self.tag_manager.get(tag_data["id"])
        self.postgres_conn_manager.select.assert_called_once()
        self.assertEqual(tag_data["id"], tag.get_id())
        self.assertEqual(tag_data["entity_id"], tag.get_entity_id())
        self.assertEqual(tag_data["type_id"], tag.get_type().get_id())

    def test_get_fails_on_search_error(self):
        self.postgres_conn_manager.select = MagicMock(return_value=Result(False))
        with self.assertRaises(TagSearchError):
            self.tag_manager.get(1)
            self.fail("Did not fail")
        self.postgres_conn_manager.select.assert_called_once()

    def test_get_by_entity_id_gets_tags(self):
        entity_id = 1
        tag_data = [
            {
                "id": 1,
                "entity_id": entity_id,
                "type_id": self.type_restaurant.get_id()
            },
            {
                "id": 2,
                "entity_id": entity_id,
                "type_id": self.type_restaurant.get_id()
            }
        ]
        self.postgres_conn_manager.select = MagicMock(return_value=Result(True, "", tag_data))
        tag_objs = self.tag_manager.get_by_entity_id(entity_id)
        self.assertEqual(len(tag_data), len(tag_objs))
        for i in range(0, len(tag_data)):
            tag_datum = tag_data[i]
            tag_obj: Tag = tag_objs[i]
            self.assertEqual(tag_datum["id"], tag_obj.get_id())
            self.assertEqual(entity_id, tag_obj.get_entity_id())
            self.assertEqual(tag_datum["type_id"], tag_obj.get_type().get_id())

    def test_get_by_entity_id_fails_on_search_error(self):
        self.postgres_conn_manager.select = MagicMock(return_value=Result(False))
        with self.assertRaises(TagSearchError):
            self.tag_manager.get_by_entity_id(1)
            self.fail("Did not fail")
        self.postgres_conn_manager.select.assert_called_once()

    def test_delete_deletes_tag(self):
        self.postgres_conn_manager.query = MagicMock(return_value=Result(True))
        try:
            self.tag_manager.delete(1)
            self.postgres_conn_manager.query.assert_called_once()
        except Exception as e:
            self.fail(str(e))

    def test_delete_fails_on_delete_error(self):
        self.postgres_conn_manager.query = MagicMock(return_value=Result(False))
        with self.assertRaises(TagDeleteError):
            self.tag_manager.delete(1)
            self.fail("Did not fail")
        self.postgres_conn_manager.query.assert_called_once()
