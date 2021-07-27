class ErrorCodeHandler:
    INTERNAL_SERVER_ERROR = 500
    NOT_FOUND = 404

    def __init__(self, lookup: dict):
        self.__lookup = lookup

    def get_code(self, exception: str) -> int:
        if exception not in self.__lookup:
            return self.INTERNAL_SERVER_ERROR
        return self.__lookup[exception]
