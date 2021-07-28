from modules.api.handlers.abstracts.error_code_handler import ErrorCodeHandler
from modules.contact.exceptions.contact_search_error import ContactSearchError


class ContactErrorCodeParser(ErrorCodeHandler):
    """ Child object for contact API error codes
    """
    def __init__(self):
        """ Constructor for ContactErrorCodeParser
        """
        super().__init__({
            ContactSearchError.__name__: self.NOT_FOUND
        })
