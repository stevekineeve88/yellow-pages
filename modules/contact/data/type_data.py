from singleton_decorator import singleton
from modules.util.managers.postgres_conn_manager import PostgresConnManager


@singleton
class TypeData:
    def __init__(self, **kwargs):
        self.__postgres_conn_manager: PostgresConnManager = kwargs.get("postgres_conn_manager") or PostgresConnManager()
