from modules.util.objects.dict_object import DictObject


class Status(DictObject):
    """ Object for status properties
    """
    def __init__(self, status_id, const: str, description: str):
        """ Constructor for Status
        Args:
            status_id (ID):         Status ID
            const (str):            Constant representing object
            description (str):      Description of status
        """
        self.__id = status_id
        self.__const: str = const
        self.__description: str = description

    def get_id(self):
        """ Get ID
        Returns:
            ID
        """
        return self.__id

    def get_const(self) -> str:
        """ Get constant
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
        """ Get dict representing Status
        Returns:
            dict
        """
        return {
            "id": self.get_id(),
            "const": self.get_const(),
            "description": self.get_description()
        }
