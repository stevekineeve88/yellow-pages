from singleton_decorator import singleton
from modules.contact.data.type_data import TypeData
from modules.util.objects.data_list import DataList


@singleton
class TypeManager:
    def __init__(self, **kwargs):
        self.__type_data: TypeData = kwargs.get("type_data") or TypeData()

    def get_all(self) -> DataList:
        pass
