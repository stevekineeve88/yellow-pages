from singleton_decorator import singleton
from modules.entity.data.type_data import TypeData
from modules.entity.objects.type import Type
from modules.util.objects.data_list import DataList


@singleton
class TypeManager:
    def __init__(self, **kwargs):
        self.__type_data: TypeData = kwargs.get("type_data") or TypeData()

    def get_all(self) -> DataList:
        result = self.__type_data.load_all()
        if not result.get_status():
            raise Exception("Failed to load types")
        data = result.get_data()
        types = []
        for datum in data:
            types.append(Type(datum["id"], datum["const"], datum["description"]))
        return DataList("TYPES", types, "id", "const")
