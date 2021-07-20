class Location:
    """ Object for location properties
    """
    def __init__(self, latitude: float, longitude: float, address: str):
        """ Constructor for Location
        Args:
            latitude (float):
            longitude (float):
            address (str):
        """
        self.__latitude: float = float(latitude)
        self.__longitude: float = float(longitude)
        self.__address: str = address

    def get_latitude(self) -> float:
        """ Get latitude
        Returns:
            float
        """
        return self.__latitude

    def get_longitude(self) -> float:
        """ Get longitude
        Returns:
            float
        """
        return self.__longitude

    def get_address(self) -> str:
        """ Get address
        Returns:
            str
        """
        return self.__address
