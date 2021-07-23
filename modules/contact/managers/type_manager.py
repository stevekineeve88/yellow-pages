from singleton_decorator import singleton
from modules.contact.data.type_data import TypeData
from modules.contact.exceptions.contact_type_error import ContactTypeError
from modules.contact.objects.type import Type
from modules.util.objects.data_list import DataList


@singleton
class TypeManager:
    """ Manager class for type CRUD operations
    """
    def __init__(self, **kwargs):
        """ Constructor for TypeManager
        Args:
            **kwargs:   Optional dependencies
                type_data (TypeData)
        """
        self.__type_data: TypeData = kwargs.get("type_data") or TypeData()

    def get_all(self) -> DataList:
        """ Get all types
        Returns:
            DataList
        """
        result = self.__type_data.load_all()
        if not result.get_status():
            raise ContactTypeError("Could not load types")
        data = result.get_data()
        types = []
        for datum in data:
            types.append(Type(datum["id"], datum["const"], datum["description"]))
        return DataList("CONTACT_TYPES", types, "id", "const")
