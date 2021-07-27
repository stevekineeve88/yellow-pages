from modules.util.exceptions.data_list_item_exception import DataListItemException
from modules.util.objects.dict_object import DictObject


class DataList:
    """ Object for generic data lists that are represented by a constant
        and ID
    """
    def __init__(self, name: str, data, id_index: str, const_index: str):
        """ Constructor for DataList
        Args:
            name (str):         Name for logging
            data (list):        List of DictObject objects
            id_index (str):     ID key name for fetching from DictObject
            const_index (str):  Const key name for fetching from DictObject
        """
        self.__name: str = name
        self.__data = {}
        self.__const_index_pointers: dict = {}
        obj: DictObject
        for obj in data:
            obj_dict = obj.get_dict()
            item_id = obj_dict[id_index]
            self.__data[item_id] = obj
            self.__const_index_pointers[obj_dict[const_index]] = item_id

    def __getattr__(self, key: str):
        """ Get item from data by constant property
        Args:
            key (str):      Constant property
        Returns:
            any
        """
        if key not in self.__const_index_pointers:
            raise DataListItemException(f"{key} not in {self.__name} data list")
        return self.get_by_id(self.__const_index_pointers[key])

    def get_by_id(self, item_id):
        """ Get item from data by ID property
        Args:
            item_id:        Item ID
        Returns:
            any
        """
        if item_id not in self.__data:
            raise DataListItemException(f"{item_id} not in {self.__name} data list")
        return self.__data[item_id]

    def get_all(self) -> dict:
        return self.__data
