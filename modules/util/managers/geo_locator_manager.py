from geopy.geocoders import Nominatim
from singleton_decorator import singleton
from modules.util.objects.location import Location
from modules.util.objects.result import Result


@singleton
class GeolocatorManager:
    def __init__(self):
        self.__geolocator = Nominatim(user_agent="yellow-pages")

    def get_by_address(self, address: str) -> Result:
        location = self.__geolocator.geocode(address)
        if location is None:
            return Result(True, f"{address} is an invalid location")
        return Result(True, "", [
            Location(location.latitude, location.longitude, location.address)
        ])

    def get_by_coordinates(self, latitude: float, longitude: float) -> Result:
        coordinates = f"{latitude}, {longitude}"
        location = self.__geolocator.reverse(coordinates)
        if location is None:
            return Result(True, f"({latitude}, {longitude}) is an invalid location")
        return Result(True, "", [
            Location(location.latitude, location.longitude, location.address)
        ])
