class Location:
    def __init__(self, latitude: float, longitude: float, address: str):
        self.__latitude: float = latitude
        self.__longitude: float = longitude
        self.__address: str = address

    def get_latitude(self) -> float:
        return self.__latitude

    def get_longitude(self) -> float:
        return self.__longitude

    def get_address(self) -> str:
        return self.__address
