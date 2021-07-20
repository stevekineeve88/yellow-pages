from modules.entity.objects.status import Status
from modules.util.objects.location import Location


class Entity:
    def __init__(self, **kwargs):
        self.__id = kwargs.get("id")
        self.__uuid: str = kwargs.get("uuid")
        self.__name: str = kwargs.get("name")
        self.__status: Status = kwargs.get("status")
        self.__location: Location = kwargs.get("location")

    def get_id(self):
        return self.__id

    def get_uuid(self) -> str:
        return self.__uuid

    def get_name(self) -> str:
        return self.__name

    def set_name(self, name: str):
        self.__name = name

    def get_status(self) -> Status:
        return self.__status

    def get_location(self) -> Location:
        return self.__location
