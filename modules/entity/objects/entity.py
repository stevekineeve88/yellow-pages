from modules.entity.objects.status import Status
from modules.util.objects.location import Location


class Entity:
    """ Object for entity properties
    """
    def __init__(self, **kwargs):
        """ Constructor for Entity
        Args:
            **kwargs:
                id (ID)
                uuid (str)
                name (str)
                status (Status)
                location (Location)
        """
        self.__id = kwargs.get("id")
        self.__uuid: str = kwargs.get("uuid")
        self.__name: str = kwargs.get("name")
        self.__status: Status = kwargs.get("status")
        self.__location: Location = kwargs.get("location")

    def get_id(self):
        """ Get ID
        Returns:
            ID
        """
        return self.__id

    def get_uuid(self) -> str:
        """ Get UUID
        Returns:
            str
        """
        return self.__uuid

    def get_name(self) -> str:
        """ Get name
        Returns:
            str
        """
        return self.__name

    def set_name(self, name: str):
        """ Set name
        Args:
            name (str):     New name
        """
        self.__name = name

    def get_status(self) -> Status:
        """ Get status
        Returns:
            Status
        """
        return self.__status

    def get_location(self) -> Location:
        """ Get location
        Returns:
            Location
        """
        return self.__location
