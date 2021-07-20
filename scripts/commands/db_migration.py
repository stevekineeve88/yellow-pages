from argparse import ArgumentParser

from environment import Environment
from modules.migration.managers.migration_manager import MigrationManager


def parse_args():
    """Parses argument parameters
    """
    parser = ArgumentParser()
    parser.add_argument(
        '--postgres_host',
        action="store",
        dest="postgres_host",
        help="Postgres Host",
        required=True
    )
    parser.add_argument(
        '--postgres_user',
        action="store",
        dest="postgres_user",
        help="Postgres User",
        required=True
    )
    parser.add_argument(
        '--postgres_password',
        action="store",
        dest="postgres_password",
        help="Postgres Password",
        required=True
    )
    parser.add_argument(
        '--postgres_db',
        action="store",
        dest="postgres_db",
        help="Postgres DB",
        required=True
    )
    parser.add_argument(
        '--directory',
        action="store",
        dest="directory",
        help="Directory Root",
        required=True
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    environment = Environment()
    environment.set(environment.POSTGRES_HOST, args.postgres_host)
    environment.set(environment.POSTGRES_USER, args.postgres_user)
    environment.set(environment.POSTGRES_PASS, args.postgres_password)
    environment.set(environment.POSTGRES_DB_NAME, args.postgres_db)

    migration_manager = MigrationManager()
    migration_manager.migrate(args.directory)
