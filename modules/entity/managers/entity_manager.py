from singleton_decorator import singleton
from modules.entity.data.entity_data import EntityData
from modules.entity.exceptions.entity_creation_error import EntityCreationError
from modules.entity.exceptions.entity_search_error import EntitySearchError
from modules.entity.exceptions.entity_update_error import EntityUpdateError
from modules.entity.managers.status_manager import StatusManager
from modules.entity.objects.entity import Entity
from modules.util.exceptions.geo_locator_error import GeoLocatorError
from modules.util.managers.geo_locator_manager import GeoLocatorManager
from modules.util.objects.location import Location


@singleton
class EntityManager:
    """ Manager class for entity CRUD operations
    """
    def __init__(self, **kwargs):
        """ Constructor for EntityManager
        Args:
            **kwargs:   Optional Dependencies
                entity_data (EntityData)
                geo_locator_manager (GeoLocatorManager)
                status_manager (StatusManager)
        """
        self.__entity_data: EntityData = kwargs.get("entity_data") or EntityData()
        self.__geo_locator_manager: GeoLocatorManager = kwargs.get("geo_locator_manager") or GeoLocatorManager()
        status_manager: StatusManager = kwargs.get("status_manager") or StatusManager()
        self.__statuses = status_manager.get_all()

    def create(self, **kwargs) -> Entity:
        """ Create entity
        Args:
            **kwargs:       Parameters needed
                name (str)
                address (str)
        Returns:
            Entity
        """
        address = kwargs.get("address")
        result = self.__geo_locator_manager.get_by_address(address)
        if not result.get_status():
            raise GeoLocatorError(result.get_message())
        location = result.get_data()[0]
        name = kwargs.get("name")
        result = self.__entity_data.insert(
            name=name,
            status_id=self.__statuses.ACTIVE.get_id(),
            latitude=location.get_latitude(),
            longitude=location.get_longitude(),
            address=address
        )
        if not result.get_status():
            raise EntityCreationError(f"Could not create entity with name {name}")
        return self.get(result.get_insert_id())

    def get(self, entity_id) -> Entity:
        """ Get entity by ID
        Args:
            entity_id (ID):     Entity ID
        Returns:
            Entity
        """
        result = self.__entity_data.load(entity_id)
        data = result.get_data()
        if len(data) == 0:
            raise EntitySearchError(f"Entity id {entity_id} not found")
        return self.__build_entity_object(data[0])

    def update(self, entity: Entity):
        """ Update entity
        Args:
            entity (Entity):       Entity object
        """
        result = self.__entity_data.update(entity.get_id(), entity.get_name())
        if not result.get_status():
            raise EntityUpdateError(f"Could not update entity id {entity.get_id()}")

    def update_location(self, entity_id, address: str) -> Entity:
        """ Update location
        Args:
            entity_id (ID):     Entity ID
            address (str):      New address
        Returns:
            Entity
        """
        result = self.__geo_locator_manager.get_by_address(address)
        if not result.get_status():
            raise GeoLocatorError(result.get_message())
        location = result.get_data()[0]
        result = self.__entity_data.update_location(
            entity_id,
            latitude=location.get_latitude(),
            longitude=location.get_longitude(),
            address=address
        )
        if not result.get_status():
            raise EntityUpdateError(f"Could not update entity id {entity_id}")
        return self.get(entity_id)

    def update_status(self, entity_id, status_id) -> Entity:
        """ Update status
        Args:
            entity_id (ID):     Entity ID
            status_id (ID):     Status ID
        Returns:
            Entity
        """
        status_id = self.__statuses.get_by_id(status_id).get_id()
        result = self.__entity_data.update_status(entity_id, status_id)
        if not result.get_status():
            raise EntityUpdateError(f"Could not update status for entity id {entity_id}")
        return self.get(entity_id)

    def search(self, **kwargs) -> list:
        """ Search entities by parameters
        Args:
            **kwargs:
                name (str)
                address (str)
                statuses (list)
        Returns:
            list
        """
        result = self.__entity_data.search(**kwargs)
        if not result.get_status():
            raise EntitySearchError("Failed to search for entities")
        return self.__build_entity_objects(result.get_data())

    def search_nearby(self, latitude: float, longitude: float, miles: int, **kwargs) -> list:
        """
        Args:
            latitude (float):       Latitude coordinate
            longitude (float):      Longitude coordinate
            miles (int):            Miles to search within
            **kwargs:
                name (str)
                address (str)
                statuses (list)
        Returns:
            list
        """
        result = self.__entity_data.search_nearby(latitude, longitude, miles, **kwargs)
        if not result.get_status():
            raise EntitySearchError("Failed to search for entities")
        return self.__build_entity_objects(result.get_data())

    def __build_entity_objects(self, data) -> list:
        """ Build entity object list
        Args:
            data (iterable):
        Returns:
            list
        """
        entities = []
        for datum in data:
            entities.append(self.__build_entity_object(datum))
        return entities

    def __build_entity_object(self, data: dict) -> Entity:
        """ Build entity object
        Args:
            data (dict):
        Returns:
            Entity
        """
        return Entity(
            id=data["id"],
            uuid=data["uuid"],
            name=data["name"],
            status=self.__statuses.get_by_id(data["status_id"]),
            location=Location(data["latitude"], data["longitude"], data["address"])
        )
