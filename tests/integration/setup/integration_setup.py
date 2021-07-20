import unittest
from environment import Environment
from modules.migration.managers.migration_manager import MigrationManager
from tests.integration.setup.config.config import config


class IntegrationSetup(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        environment: Environment = Environment()
        config_vars = config()

        environment.set(environment.POSTGRES_HOST, config_vars[environment.POSTGRES_HOST])
        environment.set(environment.POSTGRES_USER, config_vars[environment.POSTGRES_USER])
        environment.set(environment.POSTGRES_PASS, config_vars[environment.POSTGRES_PASS])
        environment.set(environment.POSTGRES_DB_NAME, config_vars[environment.POSTGRES_DB_NAME])

        migration_manager: MigrationManager = MigrationManager()
        migration_manager.migrate("scripts/migration")
