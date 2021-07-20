from singleton_decorator import singleton
from modules.util.managers.postgres_conn_manager import PostgresConnManager
from modules.util.objects.result import Result


@singleton
class MigrationData:
    """ Data class for migration database operations
    """
    def __init__(self, **kwargs):
        """ Constructor for MigrationData
        Args:
            **kwargs:
                postgres_conn_manager (PostgresConnManager)
        """
        self.__postgres_conn_manager: PostgresConnManager = kwargs.get("postgres_conn_manager") or PostgresConnManager()

    def create_migration_table(self) -> Result:
        """ Create default migration table
        Returns:
            Result
        """
        return self.__postgres_conn_manager.query(f"""
            CREATE TABLE IF NOT EXISTS public.db_migrations
            (
                id serial NOT NULL,
                file character varying(100) COLLATE pg_catalog."default" NOT NULL UNIQUE,
                run_date date NOT NULL DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT "DB_Migration_PK" PRIMARY KEY (id)
            );
        """)

    def insert(self, file: str) -> Result:
        """ Insert new migration record
        Args:
            file (str):     File name
        Returns:
            Result
        """
        return self.__postgres_conn_manager.insert(f"""
            INSERT INTO public.db_migrations (file)
            VALUES (%s)
        """, (file,))

    def load_all(self) -> Result:
        """ Load all run scripts
        Returns:
            Result
        """
        return self.__postgres_conn_manager.select(f"""
            SELECT
                id,
                file,
                run_date
            FROM public.db_migrations
        """)

    def run(self, file: str) -> Result:
        """ Run sql file script
        Args:
            file (str):     File with root directory
        Returns:
            Result
        """
        file = open(file, "r")
        try:
            self.__postgres_conn_manager.get_cursor().execute(file.read())
            return Result(True)
        except Exception as e:
            return Result(False, str(e))
        finally:
            file.close()
