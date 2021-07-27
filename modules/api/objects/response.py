from flask import jsonify


class Response:
    def __init__(self, content: list, message: str = "", code: int = 200):
        self.__message = message
        self.__content = content
        self.__code = code

    def get_response(self) -> tuple:
        return (jsonify({
            "content": [item.get_content() for item in self.__content],
            "message": self.__message
        }), self.__code)
