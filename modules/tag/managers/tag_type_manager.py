from singleton_decorator import singleton
from modules.tag.data.tag_type_data import TagTypeData
from modules.tag.exceptions.tag_type_error import TagTypeError
from modules.tag.objects.tag_type import TagType
from modules.util.objects.data_list import DataList


@singleton
class TagTypeManager:
    """ Manager class for tag type CRUD operations
    """
    def __init__(self, **kwargs):
        """ Constructor for TagTypeManager
        Args:
            **kwargs:   Optional dependencies
                tag_type_data (TagTypeData)
        """
        self.__type_data: TagTypeData = kwargs.get("tag_type_data") or TagTypeData()

    def get_all(self) -> DataList:
        """ Get all
        Returns:
            DataList
        """
        result = self.__type_data.load_all()
        if not result.get_status():
            raise TagTypeError("Could not fetch types")
        data = result.get_data()
        types = []
        for datum in data:
            types.append(TagType(datum["id"], datum["const"], datum["description"]))
        return DataList("TAG_TYPES", types, "id", "const")
