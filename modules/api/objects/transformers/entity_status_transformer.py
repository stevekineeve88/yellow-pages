from modules.api.objects.transformer import Transformer
from modules.entity.objects.entity_status import EntityStatus


class EntityStatusTransformer(Transformer):
    """ Child transformer object for EntityStatus object
    """
    def __init__(self, status: EntityStatus):
        """ Constructor for EntityStatusTransformer
        Args:
            status (EntityStatus):
        """
        super().__init__({
            "id": status.get_id(),
            "const": status.get_const(),
            "description": status.get_description(),
        })
