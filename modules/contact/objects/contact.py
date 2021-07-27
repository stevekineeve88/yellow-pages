from modules.contact.objects.contact_type import ContactType


class Contact:
    """ Object representing contact properties
    """
    def __init__(self, **kwargs):
        """ Constructor for Contact
        Args:
            **kwargs:
                id (ID)
                entity_id (ID)
                type (Type)
                info (str)
                description (str)
        """
        self.__id = kwargs.get("id")
        self.__entity_id = kwargs.get("entity_id")
        self.__type: ContactType = kwargs.get("type")
        self.__info: str = kwargs.get("info")
        self.__description: str = kwargs.get("description")

    def get_id(self):
        """ Get ID
        Returns:
            ID
        """
        return self.__id

    def get_entity_id(self):
        """ Get entity ID
        Returns:
            ID
        """
        return self.__entity_id

    def get_type(self) -> ContactType:
        """ Get type
        Returns:
            Type
        """
        return self.__type

    def get_info(self) -> str:
        """ Get info
        Returns:
            str
        """
        return self.__info

    def set_info(self, info: str):
        """ Set info
        Args:
            info (str):
        """
        self.__info = info

    def get_description(self) -> str:
        """ Get description
        Returns:
            str
        """
        return self.__description

    def set_description(self, description: str):
        """ Set description
        Args:
            description (str):
        """
        self.__description = description
