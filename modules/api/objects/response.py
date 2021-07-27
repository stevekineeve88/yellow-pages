from flask import jsonify


class Response:
    """ Object for representing API response
    """
    def __init__(self, content: list, message: str = "", code: int = 200):
        """ Constructor for Response
        Args:
            content (list):         Content as list of transformers
            message (str):          Error message
            code (int):             Response code
        """
        self.__content: list = content
        self.__message: str = message
        self.__code: int = code
        self.__meta_data: dict = {}

    def set_meta_data(self, meta_data: dict):
        """ Set meta data
        Args:
            meta_data (dict):
        """
        self.__meta_data = meta_data

    def get_response(self) -> tuple:
        """ Get response as tuple
        Returns:
            tuple
        """
        return (jsonify({
            "content": [item.get_content() for item in self.__content],
            "metadata": self.__meta_data,
            "message": self.__message
        }), self.__code)
