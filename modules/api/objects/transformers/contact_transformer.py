from modules.api.objects.transformer import Transformer
from modules.contact.objects.contact import Contact


class ContactTransformer(Transformer):
    """ Child transformer object for Contact object
    """
    def __init__(self, contact: Contact):
        """ Constructor for ContactTransformer
        Args:
            contact (Contact):
        """
        super().__init__({
            "info": contact.get_info(),
            "type": contact.get_type().get_dict(),
            "description": contact.get_description(),
        })
