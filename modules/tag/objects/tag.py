from modules.tag.objects.type import Type


class Tag:
    """ Object representing tag attributes
    """
    def __init__(self, tag_id, entity_id, tag_type):
        """ Constructor for Tag
        Args:
            tag_id (ID):        Tag ID
            entity_id (ID):     Entity ID
            tag_type (Type):    Tag type
        """
        self.__id = tag_id
        self.__entity_id = entity_id
        self.__type: Type = tag_type

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

    def get_type(self) -> Type:
        """ Get type
        Returns:
            Type
        """
        return self.__type
