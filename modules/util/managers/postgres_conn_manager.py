import psycopg2
import psycopg2.extras
from singleton_decorator import singleton
from environment import Environment
from modules.util.objects.result import Result


@singleton
class PostgresConnManager:
    def __init__(self):
        environment: Environment = Environment()
        self.__connection = psycopg2.connect(
            host=environment.get(environment.POSTGRES_HOST),
            database=environment.get(environment.POSTGRES_DB_NAME),
            user=environment.get(environment.POSTGRES_USER),
            password=environment.get(environment.POSTGRES_PASS)
        )

    def get_connection(self):
        return self.__connection

    def get_cursor(self):
        return self.__connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def insert(self, sql: str, params=None) -> Result:
        cursor = self.get_cursor()
        try:
            if params is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, params)
            self.__connection.commit()
            result = Result(True)
            result.set_insert_id(cursor.fetchone()[0])
            return result
        except Exception as e:
            self.__connection.rollback()
            return Result(False, str(e))
        finally:
            cursor.close()

    def select(self, sql: str, params=None):
        cursor = self.get_cursor()
        try:
            if params is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, params)
            data = cursor.fetchall()
            return Result(True, "", data)
        except Exception as e:
            self.__connection.rollback()
            return Result(False, str(e))
        finally:
            cursor.close()

    def query(self, sql: str, params=None):
        cursor = self.get_cursor()
        try:
            if params is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, params)
            self.__connection.commit()
            result = Result(True)
            return result
        except Exception as e:
            self.__connection.rollback()
            return Result(False, str(e))
        finally:
            cursor.close()
