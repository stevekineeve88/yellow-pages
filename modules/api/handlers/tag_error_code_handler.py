from modules.api.handlers.abstracts.error_code_handler import ErrorCodeHandler
from modules.tag.exceptions.tag_type_error import TagTypeError


class TagErrorCodeParser(ErrorCodeHandler):
    """ Child object for tag API error codes
    """
    def __init__(self):
        """ Constructor for TagErrorCodeParser
        """
        super().__init__({
            TagTypeError.__name__: self.NOT_FOUND
        })
