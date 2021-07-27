from modules.tag.objects.tag_type import TagType


class Tag:
    """ Object representing tag attributes
    """
    def __init__(self, tag_id, entity_id, tag_type):
        """ Constructor for Tag
        Args:
            tag_id (ID):        Tag ID
            entity_id (ID):     Entity ID
            tag_type (TagType):    Tag type
        """
        self.__id = tag_id
        self.__entity_id = entity_id
        self.__type: TagType = tag_type

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

    def get_type(self) -> TagType:
        """ Get type
        Returns:
            Type
        """
        return self.__type
