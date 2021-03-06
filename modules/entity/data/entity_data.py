from singleton_decorator import singleton
from modules.util.managers.postgres_conn_manager import PostgresConnManager
from modules.util.objects.result import Result


@singleton
class EntityData:
    """ Data class for entity database operations
    """
    def __init__(self, **kwargs):
        """ Constructor for EntityData
        Args:
            **kwargs: Optional dependencies
                postgres_conn_manager (PostgresConnManager)
        """
        self.__postgres_conn_manager: PostgresConnManager = kwargs.get("postgres_conn_manager") or PostgresConnManager()

    def insert(self, **kwargs) -> Result:
        """ Insert entity
        Args:
            **kwargs:
                name (str)
                latitude (float)
                longitude (float)
                address (str)
                status_id (ID)
        Returns:
            Result
        """
        return self.__postgres_conn_manager.insert(f"""
            INSERT INTO entity.entities(name, latitude, longitude, address, status_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (
            kwargs.get("name"),
            kwargs.get("latitude"),
            kwargs.get("longitude"),
            kwargs.get("address"),
            kwargs.get("status_id")
        ))

    def load(self, entity_id) -> Result:
        """ Load entity by ID
        Args:
            entity_id (ID):      Entity ID
        Returns:
            Result
        """
        return self.__postgres_conn_manager.select(f"""
            SELECT
                id,
                uuid,
                name,
                latitude,
                longitude,
                address,
                status_id
            FROM entity.entities
            WHERE id = %s
        """, (entity_id,))

    def load_by_uuid(self, uuid: str) -> Result:
        """ Load entity by UUID
        Args:
            uuid (str):
        Returns:
            Result
        """
        return self.__postgres_conn_manager.select(f"""
            SELECT
                id,
                uuid,
                name,
                latitude,
                longitude,
                address,
                status_id
            FROM entity.entities
            WHERE uuid = %s
        """, (uuid,))

    def update(self, entity_id, name: str) -> Result:
        """ Update entity
        Args:
            entity_id (ID):     Entity ID
            name (str):         Entity name
        Returns:
            Result
        """
        return self.__postgres_conn_manager.query(f"""
            UPDATE entity.entities
            SET name = %s
            WHERE id = %s
        """, (
            name,
            entity_id
        ))

    def update_location(self, entity_id, **kwargs) -> Result:
        """ Update location
        Args:
            entity_id (ID):         Entity ID
            **kwargs:
                latitude (float)
                longitude (float)
                address (str)
        Returns:
            Result
        """
        return self.__postgres_conn_manager.query(f"""
            UPDATE entity.entities
            SET latitude = %s,
                longitude = %s,
                address = %s
            WHERE id = %s
        """, (
            kwargs.get("latitude"),
            kwargs.get("longitude"),
            kwargs.get("address"),
            entity_id
        ))

    def update_status(self, entity_id, status_id) -> Result:
        """ Update status
        Args:
            entity_id (ID):      Entity ID
            status_id (ID):      Status ID
        Returns:
            Result
        """
        return self.__postgres_conn_manager.query(f"""
            UPDATE entity.entities
            SET status_id = %s
            WHERE id = %s
        """, (
            status_id,
            entity_id
        ))

    def search(self, **kwargs) -> Result:
        """ Search entities by parameters
        Args:
            **kwargs:
                name (str)
                address (str)
                statuses (list)
                tags (list)
                limit (int)
                offset (int)
        Returns:
            Result
        """
        name = kwargs.get("name") or ""
        address = kwargs.get("address") or ""
        statuses = kwargs.get("statuses") or []
        tags = kwargs.get("tags") or []
        limit = kwargs.get("limit") or 100
        offset = kwargs.get("offset") or 0
        limit = limit if limit <= 100 else 100
        offset = offset if offset >= 0 else 0
        params = (
            f"%{name}%",
            f"%{address}%"
        )

        query_parts = []
        for status_id in statuses:
            query_parts.append(f"e.status_id = %s")
            params += (status_id,)
        status_query_string = f"AND ({' OR '.join(query_parts)})" if len(query_parts) != 0 else ""

        query_parts = []
        for tag_id in tags:
            query_parts.append(f"t.type_id = %s")
            params += (tag_id,)
        tag_query_string = f"AND ({' OR '.join(query_parts)})" if len(query_parts) != 0 else ""

        params += (limit, offset)

        return self.__postgres_conn_manager.select(f"""
            SELECT
                e.id,
                e.uuid,
                e.name,
                e.latitude,
                e.longitude,
                e.address,
                e.status_id,
                count(*) OVER() AS full_count
            FROM tag.tags AS t
            RIGHT JOIN entity.entities AS e
            ON t.entity_id = e.id
            WHERE e.name LIKE %s
            AND e.address LIKE %s
            {status_query_string}
            {tag_query_string}
            GROUP BY e.id
            ORDER BY e.name ASC
            LIMIT %s OFFSET %s
        """, params)

    def search_nearby(self, latitude: float, longitude: float, miles: int, **kwargs) -> Result:
        """ Search nearby entities by location
        Args:
            latitude (float):       Latitude coordinate
            longitude (float):      Longitude coordinate
            miles (int):            Miles to search within
            **kwargs:
                name (str)
                address (str)
                statuses (list)
                tags (list)
                limit (int)
                offset (int)
        Returns:
            Result
        """
        name = kwargs.get("name") or ""
        address = kwargs.get("address") or ""
        statuses = kwargs.get("statuses") or []
        tags = kwargs.get("tags") or []
        limit = kwargs.get("limit") or 100
        offset = kwargs.get("offset") or 0
        limit = limit if limit <= 100 else 100
        offset = offset if offset >= 0 else 0
        params = (
            longitude,
            latitude,
            f"%{name}%",
            f"%{address}%",
            longitude,
            latitude,
            miles
        )

        query_parts = []
        for status_id in statuses:
            query_parts.append(f"e.status_id = %s")
            params += (status_id,)
        status_query_string = f"AND ({' OR '.join(query_parts)})" if len(query_parts) != 0 else ""

        query_parts = []
        for tag_id in tags:
            query_parts.append(f"t.type_id = %s")
            params += (tag_id,)
        tag_query_string = f"AND ({' OR '.join(query_parts)})" if len(query_parts) != 0 else ""

        params += (limit, offset)

        return self.__postgres_conn_manager.select(f"""
            SELECT
                e.id,
                e.uuid,
                e.name,
                e.latitude,
                e.longitude,
                e.address,
                e.status_id,
                (point(%s, %s) <@> point(longitude, latitude)) AS distance,
                count(*) OVER() AS full_count
            FROM tag.tags AS t
            RIGHT JOIN entity.entities AS e
                ON t.entity_id = e.id
            WHERE e.name LIKE %s
            AND e.address LIKE %s
            AND (point(%s, %s) <@> point(longitude, latitude)) < %s
            {status_query_string}
            {tag_query_string}
            GROUP BY e.id
            ORDER BY distance ASC
            LIMIT %s OFFSET %s
        """, params)
