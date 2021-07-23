from modules.contact.exceptions.contact_parser_error import ContactParserError
from modules.contact.objects.contact_parser import ContactParser
import re


class EmailParser(ContactParser):
    """ Child ContactParser object for parsing emails
    """
    def parse(self, info: str):
        """ Parse email
        Args:
            info (str):
        """
        if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', info):
            raise ContactParserError("Invalid email")
