from modules.contact.exceptions.contact_parser_error import ContactParserError
from modules.contact.objects.contact_parser import ContactParser
import phonenumbers


class PhoneParser(ContactParser):
    def parse(self, info: str):
        phone_number = phonenumbers.parse(info)
        if not phonenumbers.is_possible_number(phone_number):
            raise ContactParserError("Invalid phone number")
