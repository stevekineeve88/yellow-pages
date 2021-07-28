from modules.api.objects.transformer import Transformer
from modules.tag.objects.tag_type import TagType


class TagTypeTransformer(Transformer):
    """ Child transformer object for TagType object
    """
    def __init__(self, tag_type: TagType):
        """ Constructor for TagTypeTransformer
        Args:
            tag_type (TagType):
        """
        super().__init__(tag_type.get_dict())
