from singleton_decorator import singleton
from modules.util.managers.postgres_conn_manager import PostgresConnManager
from modules.util.objects.result import Result


@singleton
class StatusData:
    def __init__(self, **kwargs):
        self.__postgres_conn_manager: PostgresConnManager = kwargs.get("postgres_conn_manager") or PostgresConnManager()

    def load_all(self) -> Result:
        return self.__postgres_conn_manager.select("")
