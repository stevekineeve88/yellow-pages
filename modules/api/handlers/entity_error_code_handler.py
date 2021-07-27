from modules.api.handlers.abstracts.error_code_handler import ErrorCodeHandler
from modules.entity.exceptions.entity_search_error import EntitySearchError


class EntityErrorCodeParser(ErrorCodeHandler):
    """ Child object for entity API error codes
    """
    def __init__(self):
        """ Constructor for EntityErrorCodeParser
        """
        super().__init__({
            EntitySearchError.__name__: self.NOT_FOUND
        })
