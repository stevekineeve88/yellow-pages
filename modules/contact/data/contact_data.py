from singleton_decorator import singleton
from modules.util.managers.postgres_conn_manager import PostgresConnManager
from modules.util.objects.result import Result


@singleton
class ContactData:
    """ Data class for contact database operations
    """
    def __init__(self, **kwargs):
        """ Constructor for ContactData
        Args:
            **kwargs:   Optional dependencies
                postgres_conn_manager (PostgresConnManager)
        """
        self.__postgres_conn_manager: PostgresConnManager = kwargs.get("postgres_conn_manager") or PostgresConnManager()

    def add(self, entity_id, **kwargs) -> Result:
        """ Add contact
        Args:
            entity_id (ID):      Entity ID to attach to
            **kwargs:
                type_id (ID)
                info (str)
                description (str)
        Returns:
            Result
        """
        return self.__postgres_conn_manager.insert(f"""
            INSERT INTO contact.contacts (entity_id, type_id, info, description)
            VALUES (%s, %s, %s, %s) 
            RETURNING id
        """, (
            entity_id,
            kwargs.get("type_id"),
            kwargs.get("info"),
            kwargs.get("description")
        ))

    def load(self, contact_id) -> Result:
        """ Load contact by ID
        Args:
            contact_id (ID):        Contact ID
        Returns:
            Result
        """
        return self.__postgres_conn_manager.select(f"""
            SELECT
                id,
                entity_id,
                type_id,
                info,
                description
            FROM contact.contacts
            WHERE id = %s
        """, (contact_id,))

    def update(self, contact_id, **kwargs) -> Result:
        """ Update contact info
        Args:
            contact_id (ID):         Contact ID
            **kwargs:
                info (str)
                description (str)
        Returns:
            Result
        """
        return self.__postgres_conn_manager.query(f"""
            UPDATE contact.contacts
            SET info = %s,
                description = %s
            WHERE id = %s
        """, (
            kwargs.get("info"),
            kwargs.get("description"),
            contact_id
        ))

    def delete(self, contact_id) -> Result:
        """ Delete contact by ID
        Args:
            contact_id (ID):     Contact ID
        Returns:
            Result
        """
        return self.__postgres_conn_manager.query(f"""
            DELETE FROM contact.contacts
            WHERE id = %s
        """, (contact_id,))

    def load_by_entity_id(self, entity_id) -> Result:
        """ Load contacts by entity ID
        Args:
            entity_id (ID):      Entity ID
        Returns:
            Result
        """
        return self.__postgres_conn_manager.select(f"""
            SELECT
                id,
                entity_id,
                type_id,
                info,
                description
            FROM contact.contacts
            WHERE entity_id = %s
        """, (entity_id,))
