from argparse import ArgumentParser
from environment import Environment
from modules.entity.managers.entity_manager import EntityManager
from modules.tag.managers.tag_manager import TagManager
from modules.tag.managers.tag_type_manager import TagTypeManager

""" Script for running database migrations
"""


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
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    environment = Environment()
    environment.set(environment.POSTGRES_HOST, args.postgres_host)
    environment.set(environment.POSTGRES_USER, args.postgres_user)
    environment.set(environment.POSTGRES_PASS, args.postgres_password)
    environment.set(environment.POSTGRES_DB_NAME, args.postgres_db)

    entity_manager = EntityManager()
    tag_manager = TagManager()
    tag_type_manager = TagTypeManager()
    tags = tag_type_manager.get_all()
    print("creating samples...")
    entity = entity_manager.create(name="Bum Rogers", address="207 Central Ave, Seaside Park, NJ 08752")
    tag_manager.add(entity.get_id(), tags.RESTAURANT.get_id())

    entity = entity_manager.create(name="Maruca's Tomato Pies", address="601 Ocean Terrace, Seaside Heights, NJ 08751")
    tag_manager.add(entity.get_id(), tags.RESTAURANT.get_id())
    tag_manager.add(entity.get_id(), tags.BAR.get_id())

    entity_manager.create(name="Xina Restaurant", address="430 NJ-37, Toms River, NJ 08753")
    print("samples created!")
