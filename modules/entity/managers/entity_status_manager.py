from modules.entity.data.entity_status_data import EntityStatusData
from modules.entity.exceptions.entity_status_error import EntityStatusError
from modules.entity.objects.entity_status import EntityStatus
from modules.util.objects.data_list import DataList


class EntityStatusManager:
    """ Manager class for status CRUD operations
    """
    def __init__(self, **kwargs):
        """ Constructor for EntityStatusManager
        Args:
            **kwargs:   Optional Dependencies
                entity_status_data (EntityStatusData)
        """
        self.__status_data: EntityStatusData = kwargs.get("entity_status_data") or EntityStatusData()

    def get_all(self) -> DataList:
        """ Get all statuses
        Returns:
            DataList
        """
        result = self.__status_data.load_all()
        if not result.get_status():
            raise EntityStatusError("Failed to load statuses")
        data = result.get_data()
        statuses = []
        for datum in data:
            statuses.append(EntityStatus(datum["id"], datum["const"], datum["description"]))
        return DataList("ENTITY_STATUSES", statuses, "id", "const")
