class Result:
    def __init__(self, status: bool = True, message: str = "", data: list = None):
        self.__status: bool = status
        self.__message: str = message
        self.__data: list = [] if data is None else data
        self.__insert_id = None

    def get_status(self) -> bool:
        return self.__status

    def get_message(self) -> str:
        return self.__message

    def get_data(self) -> list:
        return self.__data

    def set_insert_id(self, insert_id):
        self.__insert_id = insert_id

    def get_insert_id(self):
        return self.__insert_id
