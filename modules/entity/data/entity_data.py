from singleton_decorator import singleton
from modules.util.managers.postgres_conn_manager import PostgresConnManager
from modules.util.objects.result import Result


@singleton
class EntityData:
    def __init__(self, **kwargs):
        self.__postgres_conn_manager: PostgresConnManager = kwargs.get("postgres_conn_manager") or PostgresConnManager()

    def insert(self, **kwargs) -> Result:
        return self.__postgres_conn_manager.insert("", (
            kwargs.get("name"),
            kwargs.get("type_id"),
            kwargs.get("latitude"),
            kwargs.get("longitude"),
            kwargs.get("address"),
            kwargs.get("status_id")
        ))

    def load(self, entity_id) -> Result:
        return self.__postgres_conn_manager.select("", (entity_id,))

    def update(self, entity_id, name: str) -> Result:
        return self.__postgres_conn_manager.query("", (
            name,
            entity_id
        ))

    def update_location(self, entity_id, **kwargs):
        return self.__postgres_conn_manager.query("", (
            kwargs.get("latitude"),
            kwargs.get("longitude"),
            kwargs.get("address"),
            entity_id
        ))

    def update_status(self, entity_id, status_id):
        return self.__postgres_conn_manager.query("", (
            status_id,
            entity_id
        ))

    def search(self, **kwargs) -> Result:
        params = (
            kwargs.get("name") or "",
            kwargs.get("address") or ""
        )
        type_query_string = self.__build_or_search("type_id", kwargs.get("types") or [], params)
        status_query_string = self.__build_or_search("status_id", kwargs.get("statuses") or [], params)
        return self.__postgres_conn_manager.select(f"""
            {type_query_string} 
            {status_query_string}
        """, params)

    def search_nearby(self, latitude: float, longitude: float, miles: int) -> Result:
        """
            select SQRT(POW(69.1 * (latitude::float -  p_lat::float), 2) +
                POW(69.1 * (p_lon::float - longitude::float) * COS(latitude::float / 57.3), 2)
            )
        """
        return self.__postgres_conn_manager.select("", (
            latitude,
            longitude,
            miles
        ))

    @classmethod
    def __build_or_search(cls, column: str, items: list, params) -> str:
        query_parts = []
        for item in items:
            query_parts.append(f"{column} = %s")
            params += (item,)
        return f"AND ({' OR '.join(query_parts)})" if len(query_parts) != 0 else ""
