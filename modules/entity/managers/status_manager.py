from modules.entity.data.status_data import StatusData
from modules.entity.objects.status import Status
from modules.util.objects.data_list import DataList


class StatusManager:
    def __init__(self, **kwargs):
        self.__status_data: StatusData = kwargs.get("status_data") or StatusData()

    def get_all(self) -> DataList:
        result = self.__status_data.load_all()
        if not result.get_status():
            raise Exception("Failed to load statuses")
        data = result.get_data()
        statuses = []
        for datum in data:
            statuses.append(Status(datum["id"], datum["const"], datum["description"]))
        return DataList("STATUSES", statuses, "id", "const")
