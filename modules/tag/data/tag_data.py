from singleton_decorator import singleton
from modules.util.managers.postgres_conn_manager import PostgresConnManager
from modules.util.objects.result import Result


@singleton
class TagData:
    """ Data class for tag database operations
    """
    def __init__(self, **kwargs):
        """ Constructor for TagData
        Args:
            **kwargs:   Optional dependencies
                postgres_conn_manager (PostgresConnManager)
        """
        self.__postgres_conn_manager = kwargs.get("postgres_conn_manager") or PostgresConnManager()

    def add(self, entity_id, type_id) -> Result:
        """ Add tag to entity
        Args:
            entity_id (ID):     Entity ID
            type_id (ID):       Tag type ID
        Returns:
            Result
        """
        return self.__postgres_conn_manager.insert(f"""
            INSERT INTO tag.tags (entity_id, type_id)
            VALUES (%s, %s)
            RETURNING id
        """, (
            entity_id,
            type_id
        ))

    def load(self, tag_id) -> Result:
        """ Load by tag ID
        Args:
            tag_id (ID):
        Returns:
            Result
        """
        return self.__postgres_conn_manager.select(f"""
            SELECT
                id,
                entity_id,
                type_id
            FROM tag.tags
            WHERE id = %s
        """, (tag_id,))

    def load_by_entity_id(self, entity_id) -> Result:
        """ Load by entity ID
        Args:
            entity_id (ID):
        Returns:
            Result
        """
        return self.__postgres_conn_manager.select(f"""
            SELECT
                id,
                entity_id,
                type_id
            FROM tag.tags
            WHERE entity_id = %s
        """, (entity_id,))

    def delete(self, tag_id) -> Result:
        """ Delete by ID
        Args:
            tag_id (ID):
        Returns:
            Result
        """
        return self.__postgres_conn_manager.query(f"""
            DELETE FROM tag.tags
            WHERE id = %s
        """, (tag_id,))
