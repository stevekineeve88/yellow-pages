class Transformer:
    """ Object representing object transformation to API format
    """
    def __init__(self, data: dict):
        """ Constructor for Transformer
        Args:
            data (dict):        Dict format of object
        """
        self.__data: dict = data

    def get_content(self) -> dict:
        """ Get content
        Returns:
            dict
        """
        return self.__data
