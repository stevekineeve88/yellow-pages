from singleton_decorator import singleton
from modules.tag.data.tag_data import TagData
from modules.tag.exceptions.tag_add_error import TagAddError
from modules.tag.exceptions.tag_delete_error import TagDeleteError
from modules.tag.exceptions.tag_search_error import TagSearchError
from modules.tag.managers.tag_type_manager import TagTypeManager
from modules.tag.objects.tag import Tag
from modules.util.objects.data_list import DataList


@singleton
class TagManager:
    """ Manager class for tag CRUD operations
    """
    def __init__(self, **kwargs):
        """ Constructor for TagManager
        Args:
            **kwargs:   Optional dependencies
                tag_data (TagData)
                tag_type_manager (TagTypeManager)
        """
        self.__tag_data: TagData = kwargs.get("tag_data") or TagData()
        type_manager: TagTypeManager = kwargs.get("tag_type_manager") or TagTypeManager()
        self.__types: DataList = type_manager.get_all()

    def add(self, entity_id, type_id) -> Tag:
        """ Add tag
        Args:
            entity_id (ID):     Entity ID
            type_id (ID):       Tag type ID
        Returns:
            Tag
        """
        result = self.__tag_data.add(entity_id, type_id)
        if not result.get_status():
            raise TagAddError("Could not add tag to entity")
        return Tag(result.get_insert_id(), entity_id, self.__types.get_by_id(type_id))

    def get(self, tag_id) -> Tag:
        """ Get tag by ID
        Args:
            tag_id (ID):
        Returns:
            Tag
        """
        result = self.__tag_data.load(tag_id)
        if len(result.get_data()) == 0:
            raise TagSearchError("Could not get tag")
        data = result.get_data()[0]
        return Tag(data["id"], data["entity_id"], self.__types.get_by_id(data["type_id"]))

    def get_by_entity_id(self, entity_id) -> list:
        """ Get tags by entity ID
        Args:
            entity_id (ID):
        Returns:
            list
        """
        result = self.__tag_data.load_by_entity_id(entity_id)
        if not result.get_status():
            raise TagSearchError("Could not get tags")
        data = result.get_data()
        tags = []
        for datum in data:
            tags.append(Tag(datum["id"], datum["entity_id"], self.__types.get_by_id(datum["type_id"])))
        return tags

    def delete(self, tag_id):
        """ Delete by ID
        Args:
            tag_id (ID):
        """
        result = self.__tag_data.delete(tag_id)
        if not result.get_status():
            raise TagDeleteError("Could not delete tag")
