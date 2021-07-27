from modules.entity.managers.entity_manager import EntityManager
from modules.entity.objects.entity import Entity
from modules.tag.exceptions.tag_add_error import TagAddError
from modules.tag.exceptions.tag_search_error import TagSearchError
from modules.tag.managers.tag_manager import TagManager
from modules.tag.managers.tag_type_manager import TagTypeManager
from modules.tag.objects.tag import Tag
from modules.util.managers.postgres_conn_manager import PostgresConnManager
from modules.util.objects.data_list import DataList
from tests.integration.setup.integration_setup import IntegrationSetup


class TagManagerTest(IntegrationSetup):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.entity_manager: EntityManager = EntityManager()
        cls.tag_manager: TagManager = TagManager()
        cls.tag_type_manager: TagTypeManager = TagTypeManager()
        cls.types: DataList = cls.tag_type_manager.get_all()

    def test_add_adds_successfully(self):
        entity = self.entity_manager.create(
            name="Some name",
            address="Empire State Building, New York City, NY"
        )
        tag_created = self.tag_manager.add(entity.get_id(), self.types.RESTAURANT.get_id())
        tag_fetched = self.tag_manager.get(tag_created.get_id())
        self.assertEqual(tag_fetched.get_id(), tag_created.get_id())
        self.assertEqual(tag_fetched.get_entity_id(), tag_created.get_entity_id())
        self.assertEqual(tag_fetched.get_type().get_id(), tag_created.get_type().get_id())

    def test_add_fails_on_unknown_entity(self):
        with self.assertRaises(TagAddError):
            self.tag_manager.add(1, self.types.RESTAURANT.get_id())
            self.fail("Did not fail")

    def test_add_fails_on_unknown_type(self):
        entity = self.entity_manager.create(
            name="Some name",
            address="Empire State Building, New York City, NY"
        )
        with self.assertRaises(TagAddError):
            self.tag_manager.add(entity.get_id(), 44444)
            self.fail("Did not fail")

    def test_get_by_entity_id_gets_tags(self):
        entity_1 = self.entity_manager.create(
            name="Some name",
            address="Empire State Building, New York City, NY"
        )
        entity_2 = self.entity_manager.create(
            name="Some name 2",
            address="Empire State Building, New York City, NY"
        )
        tag_1 = self.tag_manager.add(entity_1.get_id(), self.types.RESTAURANT.get_id())
        tag_2 = self.tag_manager.add(entity_1.get_id(), self.types.BAR.get_id())
        tag_3 = self.tag_manager.add(entity_2.get_id(), self.types.RESTAURANT.get_id())

        self.__check_by_entity_id(entity_1, {
            tag_1.get_id(): tag_1,
            tag_2.get_id(): tag_2
        })

        self.__check_by_entity_id(entity_2, {
            tag_3.get_id(): tag_3
        })

    def test_delete_deletes_successfully(self):
        entity = self.entity_manager.create(
            name="Some name",
            address="Empire State Building, New York City, NY"
        )
        tag_created = self.tag_manager.add(entity.get_id(), self.types.RESTAURANT.get_id())
        tag_fetched = self.tag_manager.get(tag_created.get_id())

        self.tag_manager.delete(tag_fetched.get_id())
        with self.assertRaises(TagSearchError):
            self.tag_manager.get(tag_fetched.get_id())
            self.fail("Did not fail")

    def __check_by_entity_id(self, entity: Entity, expected: dict):
        """ Check search by entity ID successful
        Args:
            entity (Entity):
            expected (dict):        Represented as the following: {<TAG_ID>: <TAG_OBJ>...}
        """
        tags = self.tag_manager.get_by_entity_id(entity.get_id())
        self.assertEqual(len(expected), len(tags))
        tag: Tag
        for tag in tags:
            expected_tag = expected[tag.get_id()]
            self.assertEqual(expected_tag.get_id(), tag.get_id())

    def tearDown(self) -> None:
        postgres_conn_manager: PostgresConnManager = PostgresConnManager()
        postgres_conn_manager.query(f"""
            TRUNCATE entity.entities CASCADE;
            TRUNCATE contact.contacts CASCADE;
            TRUNCATE tag.tags CASCADE;
        """)
