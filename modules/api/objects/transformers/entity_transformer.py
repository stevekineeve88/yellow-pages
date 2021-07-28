from modules.api.objects.transformer import Transformer
from modules.entity.objects.entity import Entity


class EntityTransformer(Transformer):
    """ Child transformer object for Entity object
    """
    def __init__(self, entity: Entity):
        """ Constructor for EntityTransformer
        Args:
            entity (Entity):
        """
        super().__init__({
            "id": entity.get_id(),
            "uuid": entity.get_uuid(),
            "name": entity.get_name(),
            "status": entity.get_status().get_dict(),
            "address": entity.get_location().get_address()
        })
