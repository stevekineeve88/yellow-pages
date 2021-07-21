from modules.entity.managers.entity_manager import EntityManager
from modules.entity.managers.status_manager import StatusManager
from modules.entity.objects.status import Status
from modules.util.managers.geo_locator_manager import GeoLocatorManager
from modules.util.managers.postgres_conn_manager import PostgresConnManager
from modules.util.objects.location import Location
from tests.integration.setup.integration_setup import IntegrationSetup


class EntityManagerTest(IntegrationSetup):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.entity_manager: EntityManager = EntityManager()
        cls.geo_locator_manager: GeoLocatorManager = GeoLocatorManager()
        cls.status_manager: StatusManager = StatusManager()
        statuses = cls.status_manager.get_all()
        cls.status_active: Status = statuses.ACTIVE
        cls.status_deleted: Status = statuses.DELETED

    def test_create_creates_entity_successfully(self):
        name = "Momma's Chicken Parm"
        address = "Empire State Building New York City NY"
        entity = self.entity_manager.create(
            name=name,
            address=address
        )
        entity_retrieved = self.entity_manager.get(entity.get_id())
        self.assertEqual(entity.get_id(), entity_retrieved.get_id())
        self.assertEqual(entity.get_uuid(), entity_retrieved.get_uuid())
        self.assertEqual(name, entity_retrieved.get_name())
        self.assertEqual(entity.get_location().get_latitude(), entity_retrieved.get_location().get_latitude())
        self.assertEqual(entity.get_location().get_longitude(), entity_retrieved.get_location().get_longitude())
        self.assertEqual(address, entity_retrieved.get_location().get_address())

    def test_update_updates_name_successfully(self):
        old_name = "old name"
        new_name = "new name"
        created_entity = self.entity_manager.create(
            name=old_name,
            address="Empire State Building New York City NY"
        )
        old_entity = self.entity_manager.get(created_entity.get_id())
        self.assertEqual(old_name, old_entity.get_name())

        old_entity.set_name(new_name)
        self.entity_manager.update(old_entity)
        new_entity = self.entity_manager.get(old_entity.get_id())
        self.assertEqual(new_name, new_entity.get_name())

    def test_update_location_updates_location_successfully(self):
        old_address = "Empire State Building New York City NY"
        new_address = "Statue of Liberty New York City NY"

        result = self.geo_locator_manager.get_by_address(old_address)
        old_location: Location = result.get_data()[0]
        result = self.geo_locator_manager.get_by_address(new_address)
        new_location: Location = result.get_data()[0]

        created_entity = self.entity_manager.create(
            name="Some Name",
            address=old_address
        )
        self.assertEqual(old_location.get_latitude(), created_entity.get_location().get_latitude())
        self.assertEqual(old_location.get_longitude(), created_entity.get_location().get_longitude())
        self.assertEqual(old_address, created_entity.get_location().get_address())

        self.entity_manager.update_location(created_entity.get_id(), new_address)
        new_entity = self.entity_manager.get(created_entity.get_id())
        self.assertEqual(new_location.get_latitude(), new_entity.get_location().get_latitude())
        self.assertEqual(new_location.get_longitude(), new_entity.get_location().get_longitude())
        self.assertEqual(new_address, new_entity.get_location().get_address())

    def test_update_status_updates_status_successfully(self):
        entity = self.entity_manager.create(
            name="Some Name",
            address="Empire State Building New York City NY"
        )
        self.assertEqual(self.status_active.get_id(), entity.get_status().get_id())
        self.entity_manager.update_status(entity.get_id(), self.status_deleted.get_id())
        new_entity = self.entity_manager.get(entity.get_id())
        self.assertEqual(self.status_deleted.get_id(), new_entity.get_status().get_id())

    def test_search_retrieves_expected_result(self):
        empire_st_building = "Empire State Building New York City NY"
        statue_of_liberty = "Statue of Liberty New York City NY"
        self.entity_manager.create(
            name="Some Name",
            address=empire_st_building
        )
        self.entity_manager.create(
            name="Some Name 2",
            address=empire_st_building
        )
        entity = self.entity_manager.create(
            name="Some Name 3",
            address=empire_st_building
        )
        self.entity_manager.update_status(entity.get_id(), self.status_deleted.get_id())
        self.entity_manager.create(
            name="Other Name",
            address=statue_of_liberty
        )

        entities = self.entity_manager.search(
            name="Some Name"
        )
        self.assertEqual(3, len(entities))

        entities = self.entity_manager.search(
            name="Some Name",
            statuses=[self.status_active.get_id()]
        )
        self.assertEqual(2, len(entities))

        entities = self.entity_manager.search(
            address="Statue of Liberty"
        )
        self.assertEqual(1, len(entities))

    def test_search_nearby_returns_nearby_entities(self):
        address_1 = "Empire State Building New York City NY"
        address_2 = "Statue of Liberty NYC, New York"
        address_3 = "Golden Gate Bridge San Francisco, California"
        near_ny: Location = self.geo_locator_manager.get_by_address("205 E Houston St, New York City, NY 10002").get_data()[0]
        near_san_fran: Location = self.geo_locator_manager.get_by_address("1701 Jones St, San Francisco, CA 94109").get_data()[0]

        self.entity_manager.create(
            name="Some Name",
            address=address_1
        )
        self.entity_manager.create(
            name="Some Name 2",
            address=address_2
        )
        self.entity_manager.create(
            name="Other Name",
            address=address_2
        )
        entity = self.entity_manager.create(
            name="Some Name 3",
            address=address_2
        )
        self.entity_manager.update_status(entity.get_id(), self.status_deleted.get_id())
        self.entity_manager.create(
            name="Some Name 4",
            address=address_3
        )

        entities = self.entity_manager.search_nearby(
            near_ny.get_latitude(),
            near_ny.get_longitude(),
            100
        )
        self.assertEqual(4, len(entities))

        entities = self.entity_manager.search_nearby(
            near_san_fran.get_latitude(),
            near_san_fran.get_longitude(),
            100
        )
        self.assertEqual(1, len(entities))

        entities = self.entity_manager.search_nearby(
            near_ny.get_latitude(),
            near_ny.get_longitude(),
            100,
            name="Some Name"
        )
        self.assertEqual(3, len(entities))

        entities = self.entity_manager.search_nearby(
            near_ny.get_latitude(),
            near_ny.get_longitude(),
            100,
            statuses=[self.status_deleted.get_id()]
        )
        self.assertEqual(1, len(entities))

        entities = self.entity_manager.search_nearby(
            near_ny.get_latitude(),
            near_ny.get_longitude(),
            100,
            address="Statue of Liberty",
            statuses=[self.status_active.get_id()]
        )
        self.assertEqual(2, len(entities))

    def tearDown(self) -> None:
        postgres_conn_manager: PostgresConnManager = PostgresConnManager()
        postgres_conn_manager.query(f"""
            TRUNCATE entity.entities
        """)
