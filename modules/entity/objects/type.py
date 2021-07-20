from modules.util.objects.dict_object import DictObject


class Type(DictObject):
    def __init__(self, type_id, const: str, description: str):
        self.__id = type_id
        self.__const: str = const
        self.__description: str = description

    def get_id(self):
        return self.__id

    def get_const(self) -> str:
        return self.__const

    def get_description(self) -> str:
        return self.__description

    def get_dict(self) -> dict:
        return {
            "id": self.get_id(),
            "const": self.get_const(),
            "description": self.get_description()
        }
