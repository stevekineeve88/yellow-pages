from modules.contact.exceptions.contact_parser_error import ContactParserError
from modules.contact.objects.contact_parser import ContactParser
import re


class WebsiteParser(ContactParser):
    """ Child ContactParser object for parsing websites
    """
    def parse(self, info: str):
        """ Parse website
        Args:
            info (str):
        """
        regex = re.compile(
            r'^(?:http|ftp)s?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if re.match(regex, info) is None:
            raise ContactParserError("Invalid website")

