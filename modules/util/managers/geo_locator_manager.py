from geopy.geocoders import Nominatim
from singleton_decorator import singleton
from modules.util.objects.location import Location
from modules.util.objects.result import Result


@singleton
class GeoLocatorManager:
    """ Manager for Geo location operations
    """
    def __init__(self):
        """ Constructor for GeoLocatorManager
        """
        self.__geo_locator = Nominatim(user_agent="yellow-pages")

    def get_by_address(self, address: str) -> Result:
        """ Get by address
        Args:
            address (str):      Address represented as mail notation
        Returns:
            Result
        """
        location = self.__geo_locator.geocode(address)
        if location is None:
            return Result(True, f"{address} is an invalid location")
        return Result(True, "", [
            Location(location.latitude, location.longitude, location.address)
        ])

    def get_by_coordinates(self, latitude: float, longitude: float) -> Result:
        """ Get by coordinates
        Args:
            latitude (float):
            longitude (float):
        Returns:
            Result
        """
        coordinates = f"{latitude}, {longitude}"
        location = self.__geo_locator.reverse(coordinates)
        if location is None:
            return Result(True, f"({latitude}, {longitude}) is an invalid location")
        return Result(True, "", [
            Location(location.latitude, location.longitude, location.address)
        ])
