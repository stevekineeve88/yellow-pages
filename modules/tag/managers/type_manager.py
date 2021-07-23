from singleton_decorator import singleton
from modules.tag.data.type_data import TypeData
from modules.tag.exceptions.tag_type_error import TagTypeError
from modules.tag.objects.type import Type
from modules.util.objects.data_list import DataList


@singleton
class TypeManager:
    """ Manager class for tag type CRUD operations
    """
    def __init__(self, **kwargs):
        """ Constructor for TypeManager
        Args:
            **kwargs:   Optional dependencies
                type_data (TypeData)
        """
        self.__type_data: TypeData = kwargs.get("type_data") or TypeData()

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
            types.append(Type(datum["id"], datum["const"], datum["description"]))
        return DataList("TAG_TYPES", types, "id", "const")
