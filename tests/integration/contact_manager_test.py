from modules.contact.exceptions.contact_search_error import ContactSearchError
from modules.contact.managers.contact_manager import ContactManager
from modules.contact.managers.type_manager import TypeManager
from modules.contact.objects.contact import Contact
from modules.contact.objects.type import Type
from modules.entity.managers.entity_manager import EntityManager
from modules.entity.objects.entity import Entity
from modules.util.managers.postgres_conn_manager import PostgresConnManager
from modules.util.objects.data_list import DataList
from tests.integration.setup.integration_setup import IntegrationSetup


class ContactManagerTest(IntegrationSetup):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.entity_manager: EntityManager = EntityManager()
        cls.contact_manager: ContactManager = ContactManager()
        cls.type_manager: TypeManager = TypeManager()
        cls.types: DataList = cls.type_manager.get_all()

    def test_add_adds_phone_contact_to_entity(self):
        entity = self.entity_manager.create(
            name="Some name",
            address="Empire State Building, New York City, NY"
        )
        self.__check_add(entity, self.types.PHONE, "+19998887777", "Some Phone")

    def test_add_adds_email_contact_to_entity(self):
        entity = self.entity_manager.create(
            name="Some name",
            address="Empire State Building, New York City, NY"
        )
        self.__check_add(entity, self.types.EMAIL, "email@website.com", "Some email")

    def test_add_adds_website_contact_to_entity(self):
        entity = self.entity_manager.create(
            name="Some name",
            address="Empire State Building, New York City, NY"
        )
        self.__check_add(entity, self.types.WEBSITE, "https://google.com", "Some website")

    def test_update_update_contact(self):
        entity = self.entity_manager.create(
            name="Some name",
            address="Empire State Building, New York City, NY"
        )
        contact_created = self.contact_manager.add(
            entity.get_id(),
            type_id=self.types.PHONE.get_id(),
            info="+19998887777",
            description="Some description"
        )

        contact_fetch_for_update = self.contact_manager.get(contact_created.get_id())
        contact_fetch_for_update.set_info("+17776665555")
        contact_fetch_for_update.set_description("New Description")

        self.contact_manager.update(contact_fetch_for_update)
        contact_updated = self.contact_manager.get(contact_fetch_for_update.get_id())
        self.assertEqual(contact_fetch_for_update.get_info(), contact_updated.get_info())
        self.assertEqual(contact_fetch_for_update.get_description(), contact_updated.get_description())

    def test_delete_deletes_contact(self):
        entity = self.entity_manager.create(
            name="Some name",
            address="Empire State Building, New York City, NY"
        )
        contact = self.contact_manager.add(
            entity.get_id(),
            type_id=self.types.PHONE.get_id(),
            info="+19998887777",
            description="Some description"
        )
        contact_fetched = self.contact_manager.get(contact.get_id())
        self.assertEqual(contact.get_id(), contact_fetched.get_id())

        self.contact_manager.delete(contact.get_id())
        with self.assertRaises(ContactSearchError):
            self.contact_manager.get(contact.get_id())
            self.fail("Failed to delete contact")

    def test_get_by_entity_id_returns_expected_contacts(self):
        entity_1 = self.entity_manager.create(
            name="Some name",
            address="Empire State Building, New York City, NY"
        )
        entity_2 = self.entity_manager.create(
            name="Some other name",
            address="Empire State Building, New York City, NY"
        )
        contact_1 = self.contact_manager.add(
            entity_1.get_id(),
            type_id=self.types.PHONE.get_id(),
            info="+19998887777",
            description="Some phone"
        )
        contact_2 = self.contact_manager.add(
            entity_1.get_id(),
            type_id=self.types.EMAIL.get_id(),
            info="email@website.com",
            description="Some email"
        )
        contact_3 = self.contact_manager.add(
            entity_2.get_id(),
            type_id=self.types.WEBSITE.get_id(),
            info="http://google.com",
            description="Some website"
        )

        self.__check_by_entity_id(entity_1, {
            contact_1.get_id(): contact_1,
            contact_2.get_id(): contact_2
        })

        self.__check_by_entity_id(entity_2, {
            contact_3.get_id(): contact_3
        })

    def __check_add(self, entity: Entity, contact_type: Type, info: str, description: str):
        """ Check add successful
        Args:
            entity (Entity):
            contact_type (Type):
            info (str):
            description (str):
        """
        contact_added = self.contact_manager.add(
            entity.get_id(),
            type_id=contact_type.get_id(),
            info=info,
            description=description
        )
        contact_fetch = self.contact_manager.get(contact_added.get_id())
        self.assertEqual(contact_fetch.get_id(), contact_added.get_id())
        self.assertEqual(entity.get_id(), contact_added.get_entity_id())
        self.assertEqual(contact_type.get_id(), contact_added.get_type().get_id())
        self.assertEqual(info, contact_added.get_info())
        self.assertEqual(description, contact_added.get_description())

    def __check_by_entity_id(self, entity: Entity, expected: dict):
        """ Check search by entity id successful
        Args:
            entity (Entity):
            expected (dict):        Represented as the following: {<CONTACT_ID>: <CONTACT_OBJ>...}
        """
        contacts = self.contact_manager.get_by_entity_id(entity.get_id())
        self.assertEqual(len(expected), len(contacts))
        contact: Contact
        for contact in contacts:
            expected_contact = expected[contact.get_id()]
            self.assertEqual(expected_contact.get_id(), contact.get_id())

    def tearDown(self) -> None:
        postgres_conn_manager: PostgresConnManager = PostgresConnManager()
        postgres_conn_manager.query(f"""
            TRUNCATE entity.entities CASCADE;
            TRUNCATE contact.contacts CASCADE;
        """)
