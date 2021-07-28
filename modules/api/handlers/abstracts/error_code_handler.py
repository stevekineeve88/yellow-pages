class ErrorCodeHandler:
    """ Abstract class for handling error codes
    """
    INTERNAL_SERVER_ERROR = 500
    FORBIDDEN = 403
    NOT_FOUND = 404

    def __init__(self, lookup: dict):
        """ Constructor for ErrorCodeHandler
        Args:
            (dict) lookup:      Dictionary of exception to code
                                <EXCEPTION_CLASS_NAME>: <CODE>
        """
        self.__lookup = lookup

    def get_code(self, exception: str) -> int:
        """ Get code by exception class name
        Args:
            exception (str):
        Returns:
            int
        """
        if exception not in self.__lookup:
            return self.INTERNAL_SERVER_ERROR
        return self.__lookup[exception]
