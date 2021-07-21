from modules.contact.objects.type import Type


class Contact:
    def __init__(self, **kwargs):
        self.__id = kwargs.get("id")
        self.__entity_id = kwargs.get("entity_id")
        self.__type: Type = kwargs.get("type")
        self.__info: str = kwargs.get("info")
        self.__description: str = kwargs.get("description")

    def get_id(self):
        return self.__id

    def get_entity_id(self):
        return self.__entity_id

    def get_type(self) -> Type:
        return self.__type

    def get_info(self) -> str:
        return self.__info

    def get_description(self) -> str:
        return self.__description
