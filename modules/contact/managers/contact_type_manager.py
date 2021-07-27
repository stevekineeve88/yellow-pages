from singleton_decorator import singleton
from modules.contact.data.contact_type_data import ContactTypeData
from modules.contact.exceptions.contact_type_error import ContactTypeError
from modules.contact.objects.contact_type import ContactType
from modules.util.objects.data_list import DataList


@singleton
class ContactTypeManager:
    """ Manager class for type CRUD operations
    """
    def __init__(self, **kwargs):
        """ Constructor for ContactTypeManager
        Args:
            **kwargs:   Optional dependencies
                contact_type_data (ContactTypeData)
        """
        self.__type_data: ContactTypeData = kwargs.get("contact_type_data") or ContactTypeData()

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
            types.append(ContactType(datum["id"], datum["const"], datum["description"]))
        return DataList("CONTACT_TYPES", types, "id", "const")
