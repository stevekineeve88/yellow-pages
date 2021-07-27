class Result:
    """ Object for generic result properties
    """
    def __init__(self, status: bool = True, message: str = "", data: list = None):
        """ Constructor for Result
        Args:
            status (bool):      Status of result
            message (str):      Error message
            data (list):        List of data from result
        """
        self.__status: bool = status
        self.__message: str = message
        self.__data: list = [] if data is None else data
        self.__insert_id = None
        self.__full_count: int = 0

    def get_status(self) -> bool:
        """ Get status
        Returns:
            bool
        """
        return self.__status

    def get_message(self) -> str:
        """ Get message
        Returns:
            str
        """
        return self.__message

    def get_data(self) -> list:
        """ Get data
        Returns:
            list
        """
        return self.__data

    def set_insert_id(self, insert_id):
        """ Set ID
        Args:
            insert_id (ID):         ID from a create operation
        """
        self.__insert_id = insert_id

    def get_insert_id(self):
        """ Get ID
        Returns:
            ID
        """
        return self.__insert_id

    def set_full_count(self, full_count: int):
        """ Set full count of result without offset or limit
        Args:
            full_count (int):
        """
        self.__full_count = full_count

    def get_full_count(self) -> int:
        """ Get full count
        Returns:
            int
        """
        return self.__full_count
