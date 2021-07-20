import os


class Environment:
    """ Wrapper class for environment variables
    """
    POSTGRES_USER = "POSTGRES_USER"
    POSTGRES_PASS = "POSTGRES_PASS"
    POSTGRES_HOST = "POSTGRES_HOST"
    POSTGRES_DB_NAME = "POSTGRES_DB_NAME"

    @classmethod
    def set(cls, key: str, value):
        """ Set environment variable
        Args:
            key (str):          Key to set
            value (any):        Value set to key
        """
        os.environ[key] = value

    @classmethod
    def get(cls, key: str):
        """ Get environment variable by key
        Args:
            key (str):      Key to fetch by
        Returns:
            any
        """
        if key not in os.environ:
            raise Exception(f"{key} not found in environment")
        return os.environ[key]
