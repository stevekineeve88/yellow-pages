from os import listdir
from os.path import isfile, join

from singleton_decorator import singleton
from modules.migration.data.migration_data import MigrationData


@singleton
class MigrationManager:
    def __init__(self, **kwargs):
        self.__migration_data: MigrationData = kwargs.get("migration_data") or MigrationData()

    def migrate(self, root: str):
        result = self.__migration_data.create_migration_table()
        if not result.get_status():
            raise Exception(result.get_message())
        scripts = [f for f in listdir(root) if isfile(join(root, f))]
        print(scripts)
