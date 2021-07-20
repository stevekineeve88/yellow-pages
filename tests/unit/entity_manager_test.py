import unittest
from unittest.mock import patch, MagicMock
from modules.entity.data.entity_data import EntityData
from modules.entity.exceptions.entity_creation_error import EntityCreationError
from modules.entity.exceptions.entity_search_error import EntitySearchError
from modules.entity.exceptions.entity_update_error import EntityUpdateError
from modules.entity.managers.entity_manager import EntityManager
from modules.entity.managers.status_manager import StatusManager
from modules.entity.objects.entity import Entity
from modules.entity.objects.status import Status
from modules.util.exceptions.data_list_item_exception import DataListItemException
from modules.util.exceptions.geo_locator_error import GeoLocatorError
from modules.util.managers.geo_locator_manager import GeoLocatorManager
from modules.util.managers.postgres_conn_manager import PostgresConnManager
from modules.util.objects.data_list import DataList
from modules.util.objects.location import Location
from modules.util.objects.result import Result


class EntityManagerTest(unittest.TestCase):
    @classmethod
    @patch("modules.util.managers.postgres_conn_manager.PostgresConnManager")
    @patch("modules.util.managers.geo_locator_manager.GeoLocatorManager")
    @patch("modules.entity.managers.status_manager.StatusManager")
    def setUpClass(cls, postgres_conn_manager, geo_locator_manager, status_manager) -> None:
        cls.postgres_conn_manager: PostgresConnManager = postgres_conn_manager
        cls.geo_locator_manager: GeoLocatorManager = geo_locator_manager
        cls.status_manager: StatusManager = status_manager

        cls.status_active = Status(1, "ACTIVE", "Active Status")
        cls.status_deleted = Status(2, "DELETED", "Deleted Status")
        cls.status_manager.get_all = MagicMock(return_value=DataList(
            "STATUSES",
            [cls.status_active, cls.status_deleted],
            "id",
            "const"
        ))

        cls.entity_manager: EntityManager = EntityManager(
            entity_data=EntityData(
                postgres_conn_manager=cls.postgres_conn_manager
            ),
            geo_locator_manager=cls.geo_locator_manager,
            status_manager=cls.status_manager
        )

    def test_create_returns_entity(self):
        entity_id = 1
        uuid = "ERT-345"
        name = "Entity"
        status_id = self.status_active.get_id()
        latitude = 30.456
        longitude = 43.123
        address = "Some address"

        result = Result(True)
        result.set_insert_id(entity_id)
        self.postgres_conn_manager.insert = MagicMock(return_value=result)
        self.postgres_conn_manager.select = MagicMock(return_value=Result(
            True,
            "",
            [{
                "id": entity_id,
                "uuid": uuid,
                "name": name,
                "status_id": status_id,
                "latitude": latitude,
                "longitude": longitude,
                "address": address
            }]
        ))
        self.geo_locator_manager.get_by_address = MagicMock(return_value=Result(
            True,
            "",
            [Location(latitude, longitude, address)]
        ))

        created_entity = self.entity_manager.create(
            name=name,
            address=address
        )
        self.postgres_conn_manager.insert.assert_called_once()
        self.postgres_conn_manager.select.assert_called_once()
        self.geo_locator_manager.get_by_address.assert_called_once_with(address)
        self.assertEqual(entity_id, created_entity.get_id())
        self.assertEqual(status_id, created_entity.get_status().get_id())
        self.assertEqual(name, created_entity.get_name())
        self.assertEqual(latitude, created_entity.get_location().get_latitude())
        self.assertEqual(longitude, created_entity.get_location().get_longitude())
        self.assertEqual(address, created_entity.get_location().get_address())

    def test_create_fails_on_invalid_address(self):
        self.geo_locator_manager.get_by_address = MagicMock(return_value=Result(False))
        self.postgres_conn_manager.insert = MagicMock(return_value=Result(True))
        with self.assertRaises(GeoLocatorError):
            self.entity_manager.create(
                name="name",
                address="Fake Address"
            )
            self.postgres_conn_manager.insert.assert_not_called()

    def test_create_fails_on_create_error(self):
        self.geo_locator_manager.get_by_address = MagicMock(return_value=Result(
            True,
            "",
            [Location(123.123, 456.456, "Some Address")]
        ))
        self.postgres_conn_manager.insert = MagicMock(return_value=Result(False))
        self.postgres_conn_manager.select = MagicMock(return_value=Result(True))
        with self.assertRaises(EntityCreationError):
            self.entity_manager.create(
                address="Some Address"
            )
            self.postgres_conn_manager.insert.assert_called_once()
            self.postgres_conn_manager.select.assert_not_called()

    def test_get_fails_on_search_error(self):
        self.postgres_conn_manager.select = MagicMock(return_value=Result(False))
        with self.assertRaises(EntitySearchError):
            self.entity_manager.get(1)

    def test_update_updates_entity(self):
        entity = Entity(
            id=1,
            uuid="ERT-345",
            name="Entity",
            location=Location(30.456, 43.123, "Some address")
        )
        self.postgres_conn_manager.query = MagicMock(return_value=Result(True))
        try:
            self.entity_manager.update(entity)
            self.postgres_conn_manager.query.assert_called_once()
        except Exception as e:
            self.fail(str(e))

    def test_update_fails(self):
        self.postgres_conn_manager.query = MagicMock(return_value=Result(False))
        with self.assertRaises(EntityUpdateError):
            self.entity_manager.update(
                Entity(
                    id=1,
                    uuid="ERT-345",
                    name="Some Name",
                    location=Location(30.456, 43.123, "Some address")
                )
            )
            self.postgres_conn_manager.query.assert_called_once()

    def test_update_location_updates_entity_location(self):
        entity_id = 1
        location = Location(123.123, 456.456, "Some address")

        self.postgres_conn_manager.query = MagicMock(return_value=Result(True))
        self.postgres_conn_manager.select = MagicMock(return_value=Result(
            True,
            "",
            [{
                "id": entity_id,
                "uuid": "ERT-1234",
                "name": "Name",
                "status_id": self.status_active.get_id(),
                "latitude": location.get_latitude(),
                "longitude": location.get_longitude(),
                "address": location.get_address()
            }]
        ))
        self.geo_locator_manager.get_by_address = MagicMock(return_value=Result(
            True,
            "",
            [location]
        ))

        entity = self.entity_manager.update_location(entity_id, location.get_address())
        self.postgres_conn_manager.query.assert_called_once()
        self.postgres_conn_manager.select.assert_called_once()
        self.geo_locator_manager.get_by_address.assert_called_once_with(location.get_address())
        self.assertEqual(entity_id, entity.get_id())
        self.assertEqual(location.get_latitude(), entity.get_location().get_latitude())
        self.assertEqual(location.get_longitude(), entity.get_location().get_longitude())
        self.assertEqual(location.get_address(), entity.get_location().get_address())

    def test_update_location_fails_on_invalid_address(self):
        self.geo_locator_manager.get_by_address = MagicMock(return_value=Result(False))
        self.postgres_conn_manager.query = MagicMock(return_value=Result(True))
        with self.assertRaises(GeoLocatorError):
            self.entity_manager.update_location(1, "Fake Address")
            self.postgres_conn_manager.query.assert_not_called()

    def test_update_location_fails_on_update_error(self):
        self.geo_locator_manager.get_by_address = MagicMock(return_value=Result(
            True,
            "",
            [Location(123.123, 456.456, "Some address")]
        ))
        self.postgres_conn_manager.query = MagicMock(return_value=Result(False))
        self.postgres_conn_manager.select = MagicMock(return_value=Result(True))
        with self.assertRaises(EntityUpdateError):
            self.entity_manager.update_location(1, "Some Address")
            self.geo_locator_manager.get_by_address.assert_called_once()
            self.postgres_conn_manager.query.assert_called_once()
            self.postgres_conn_manager.select.assert_not_called()

    def test_update_status_updates_entity_status(self):
        entity_id = 1
        status_id = self.status_deleted.get_id()
        self.postgres_conn_manager.query = MagicMock(return_value=Result(True))
        self.postgres_conn_manager.select = MagicMock(return_value=Result(
            True,
            "",
            [{
                "id": entity_id,
                "uuid": "ERT-1234",
                "name": "Name",
                "status_id": status_id,
                "latitude": 123.123,
                "longitude": 456.456,
                "address": "Some Address"
            }]
        ))
        entity_updated = self.entity_manager.update_status(entity_id, status_id)
        self.postgres_conn_manager.query.assert_called_once()
        self.postgres_conn_manager.select.assert_called_once()
        self.assertEqual(entity_id, entity_updated.get_id())
        self.assertEqual(status_id, entity_updated.get_status().get_id())

    def test_update_status_fails_with_invalid_status(self):
        self.postgres_conn_manager.query = MagicMock(return_value=Result(True))
        with self.assertRaises(DataListItemException):
            self.entity_manager.update_status(1, 12345)
            self.postgres_conn_manager.query.assert_not_called()

    def test_update_status_fails_on_update_error(self):
        self.postgres_conn_manager.query = MagicMock(return_value=Result(False))
        self.postgres_conn_manager.select = MagicMock(return_value=Result(True))
        with self.assertRaises(EntityUpdateError):
            self.entity_manager.update_status(1, self.status_active.get_id())

    def test_search_gets_entities(self):
        entity_1 = {
            "id": 1,
            "uuid": "ID1",
            "name": "Name 1",
            "status_id": self.status_active.get_id(),
            "latitude": 123.123,
            "longitude": 456.456,
            "address": "Some Address 1"
        }
        entity_2 = {
            "id": 2,
            "uuid": "ID2",
            "name": "Name 2",
            "status_id": self.status_active.get_id(),
            "latitude": 456.456,
            "longitude": 789.789,
            "address": "Some Address 2"
        }
        self.postgres_conn_manager.select = MagicMock(return_value=Result(
            True,
            "",
            [entity_1, entity_2]
        ))
        entities = self.entity_manager.search(
            name="Some Address",
            statuses=[self.status_active.get_id()],
            address="Some Address"
        )
        self.postgres_conn_manager.select.assert_called_once()
        entity_obj_1: Entity = entities[0]
        entity_obj_2: Entity = entities[1]
        self.assertEqual(entity_1["id"], entity_obj_1.get_id())
        self.assertEqual(entity_1["uuid"], entity_obj_1.get_uuid())
        self.assertEqual(entity_1["name"], entity_obj_1.get_name())
        self.assertEqual(entity_1["status_id"], entity_obj_1.get_status().get_id())
        self.assertEqual(entity_1["latitude"], entity_obj_1.get_location().get_latitude())
        self.assertEqual(entity_1["longitude"], entity_obj_1.get_location().get_longitude())
        self.assertEqual(entity_1["address"], entity_obj_1.get_location().get_address())

        self.assertEqual(entity_2["id"], entity_obj_2.get_id())
        self.assertEqual(entity_2["uuid"], entity_obj_2.get_uuid())
        self.assertEqual(entity_2["name"], entity_obj_2.get_name())
        self.assertEqual(entity_2["status_id"], entity_obj_2.get_status().get_id())
        self.assertEqual(entity_2["latitude"], entity_obj_2.get_location().get_latitude())
        self.assertEqual(entity_2["longitude"], entity_obj_2.get_location().get_longitude())
        self.assertEqual(entity_2["address"], entity_obj_2.get_location().get_address())

    def test_search_fails_on_search_error(self):
        self.postgres_conn_manager.select = MagicMock(return_value=Result(False))
        with self.assertRaises(EntitySearchError):
            self.entity_manager.search()

    def test_search_nearby_gets_entities(self):
        entity_1 = {
            "id": 1,
            "uuid": "ID1",
            "name": "Name 1",
            "status_id": self.status_active.get_id(),
            "latitude": 123.123,
            "longitude": 456.456,
            "address": "Some Address 1"
        }
        entity_2 = {
            "id": 2,
            "uuid": "ID2",
            "name": "Name 2",
            "status_id": self.status_active.get_id(),
            "latitude": 456.456,
            "longitude": 789.789,
            "address": "Some Address 2"
        }
        self.postgres_conn_manager.select = MagicMock(return_value=Result(
            True,
            "",
            [entity_1, entity_2]
        ))
        entities = self.entity_manager.search_nearby(
            123.123,
            456.456,
            10,
            name="Some Name",
            statuses=[self.status_active.get_id()]
        )
        self.postgres_conn_manager.select.assert_called_once()
        entity_obj_1: Entity = entities[0]
        entity_obj_2: Entity = entities[1]
        self.assertEqual(entity_1["id"], entity_obj_1.get_id())
        self.assertEqual(entity_1["uuid"], entity_obj_1.get_uuid())
        self.assertEqual(entity_1["name"], entity_obj_1.get_name())
        self.assertEqual(entity_1["status_id"], entity_obj_1.get_status().get_id())
        self.assertEqual(entity_1["latitude"], entity_obj_1.get_location().get_latitude())
        self.assertEqual(entity_1["longitude"], entity_obj_1.get_location().get_longitude())
        self.assertEqual(entity_1["address"], entity_obj_1.get_location().get_address())

        self.assertEqual(entity_2["id"], entity_obj_2.get_id())
        self.assertEqual(entity_2["uuid"], entity_obj_2.get_uuid())
        self.assertEqual(entity_2["name"], entity_obj_2.get_name())
        self.assertEqual(entity_2["status_id"], entity_obj_2.get_status().get_id())
        self.assertEqual(entity_2["latitude"], entity_obj_2.get_location().get_latitude())
        self.assertEqual(entity_2["longitude"], entity_obj_2.get_location().get_longitude())
        self.assertEqual(entity_2["address"], entity_obj_2.get_location().get_address())

    def test_search_nearby_fails_on_search_error(self):
        self.postgres_conn_manager.select = MagicMock(return_value=Result(False))
        with self.assertRaises(EntitySearchError):
            self.entity_manager.search_nearby(123.123, 456.456, 15)
