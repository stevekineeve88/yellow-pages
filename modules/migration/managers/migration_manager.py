from os import listdir
from os.path import isfile, join
from singleton_decorator import singleton
from modules.migration.data.migration_data import MigrationData
from modules.util.objects.result import Result


@singleton
class MigrationManager:
    """ Manager class for migration operations
    """
    def __init__(self, **kwargs):
        """ Constructor for MigrationManager
        Args:
            **kwargs:
                migration_data (MigrationData)
        """
        self.__migration_data: MigrationData = kwargs.get("migration_data") or MigrationData()

    def migrate(self, root: str) -> Result:
        """ Run migrations
        Args:
            root (str):       Root directory
        Returns:
            Result
        """
        result = self.__migration_data.create_migration_table()
        if not result.get_status():
            return Result(False, result.get_message())
        all_scripts = [f for f in listdir(root) if isfile(join(root, f))]
        result = self.__migration_data.load_all()
        if not result.get_status():
            return Result(False, result.get_message())
        used_scripts = self.__build_used_scripts_array(result.get_data())
        unused_scripts = list(set(all_scripts) - set(used_scripts))

        completed = []
        for script in unused_scripts:
            result = self.__migration_data.run(f"{root}/{script}")
            if not result.get_status():
                return Result(False, f"Error in {script}: {result.get_message()}", completed)
            self.__migration_data.insert(script)
            completed.append(script)
        return Result(True, "", completed)

    @classmethod
    def __build_used_scripts_array(cls, data: list) -> list:
        """ Build array of file names
        Args:
            data (iterable):
        Returns:
            list
        """
        used_scripts = []
        for datum in data:
            used_scripts.append(datum["file"])
        return used_scripts
