from modules.util.objects.dict_object import DictObject


class DataList:
    def __init__(self, name: str, data, id_index: str, const_index: str):
        self.__name: str = name
        self.__data = {}
        self.__const_index_pointers = {}
        obj: DictObject
        for obj in data:
            obj_dict = obj.get_dict()
            item_id = obj_dict[id_index]
            self.__data[item_id] = obj
            self.__const_index_pointers[obj_dict[const_index]] = item_id

    def __getattr__(self, key: str):
        if key not in self.__const_index_pointers:
            raise Exception(f"{key} not in {self.__name} data list")
        return self.get_by_id(self.__const_index_pointers[key])

    def get_by_id(self, item_id):
        if item_id not in self.__data:
            raise Exception(f"{item_id} not in {self.__name} data list")
        return self.__data[item_id]
