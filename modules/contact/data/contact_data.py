from singleton_decorator import singleton
from modules.util.managers.postgres_conn_manager import PostgresConnManager
from modules.util.objects.result import Result


@singleton
class ContactData:
    def __init__(self, **kwargs):
        self.__postgres_conn_manager: PostgresConnManager = kwargs.get("postgres_conn_manager") or PostgresConnManager()

    def add(self, entity_id, **kwargs) -> Result:
        return self.__postgres_conn_manager.insert(f"""
        """, (
            entity_id,
            kwargs.get("type_id"),
            kwargs.get("info"),
            kwargs.get("description")
        ))

    def load(self, contact_id) -> Result:
        return self.__postgres_conn_manager.select(f"""
        """, (contact_id,))

    def update(self, contact_id, **kwargs) -> Result:
        return self.__postgres_conn_manager.query(f"""
        """, (
            kwargs.get("info"),
            kwargs.get("description"),
            contact_id
        ))
