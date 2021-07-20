import os


class Environment:
    POSTGRES_USER = "POSTGRES_USER"
    POSTGRES_PASS = "POSTGRES_PASS"
    POSTGRES_HOST = "POSTGRES_HOST"
    POSTGRES_DB_NAME = "POSTGRES_DB_NAME"

    @classmethod
    def set(cls, key: str, value):
        os.environ[key] = value

    @classmethod
    def get(cls, key: str):
        if key not in os.environ:
            raise Exception(f"{key} not found in environment")
        return os.environ[key]
