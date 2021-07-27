from modules.api.objects.transformer import Transformer
from modules.entity.objects.entity import Entity


class EntityTransformer(Transformer):
    def __init__(self, entity: Entity):
        super().__init__({
            "uuid": entity.get_uuid(),
            "name": entity.get_name(),
            "status": entity.get_status().get_dict(),
            "address": entity.get_location().get_address()
        })
