from singleton_decorator import singleton
from modules.util.managers.postgres_conn_manager import PostgresConnManager
from modules.util.objects.result import Result


@singleton
class ContactTypeData:
    """ Data class for type database operations
    """
    def __init__(self, **kwargs):
        """ Constructor for ContactTypeData
        Args:
            **kwargs:   Optional dependencies
                postgres_conn_manager (PostgresConnManager)
        """
        self.__postgres_conn_manager: PostgresConnManager = kwargs.get("postgres_conn_manager") or PostgresConnManager()

    def load_all(self) -> Result:
        """ Load all types
        Returns:
            Result
        """
        return self.__postgres_conn_manager.select(f"""
            SELECT
                id,
                const,
                description
            FROM contact.types
        """)
