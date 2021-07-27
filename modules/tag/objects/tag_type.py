from modules.util.objects.dict_object import DictObject


class TagType(DictObject):
    """ Object representing tag types
    """
    def __init__(self, type_id, const: str, description: str):
        """ Constructor for TagType
        Args:
            type_id (ID):
            const (str):
            description (str):
        """
        self.__id = type_id
        self.__const: str = const
        self.__description: str = description

    def get_id(self):
        """ Get ID
        Returns:
            ID
        """
        return self.__id

    def get_const(self) -> str:
        """ Get const
        Returns:
            str
        """
        return self.__const

    def get_description(self) -> str:
        """ Get description
        Returns:
            str
        """
        return self.__description

    def get_dict(self) -> dict:
        """ Get dict
        Returns:
            dict
        """
        return {
            "id": self.get_id(),
            "const": self.get_const(),
            "description": self.get_description()
        }
