class Transformer:
    def __init__(self, data: dict):
        self.__data: dict = data

    def get_content(self) -> dict:
        return self.__data
