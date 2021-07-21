from singleton_decorator import singleton
from modules.contact.data.contact_data import ContactData
from modules.contact.exceptions.contact_add_error import ContactAddError
from modules.contact.exceptions.contact_search_error import ContactSearchError
from modules.contact.exceptions.contact_update_error import ContactUpdateError
from modules.contact.managers.type_manager import TypeManager
from modules.contact.objects.contact import Contact
from modules.contact.objects.contact_parser import ContactParser
from modules.contact.objects.parsers.email_parser import EmailParser
from modules.contact.objects.parsers.phone_parser import PhoneParser
from modules.contact.objects.parsers.website_parser import WebsiteParser
from modules.util.objects.data_list import DataList


@singleton
class ContactManager:
    def __init__(self, **kwargs):
        self.__contact_data: ContactData = kwargs.get("contact_data") or ContactData()
        type_manager: TypeManager = kwargs.get("type_manager") or TypeManager()
        self.__types: DataList = type_manager.get_all()

    def add(self, entity_id, **kwargs) -> Contact:
        type_id = kwargs.get("type_id")
        info = kwargs.get("info")

        parser = self.__get_parser(type_id)
        parser.parse(info)

        result = self.__contact_data.add(entity_id, **kwargs)
        if not result.get_status():
            raise ContactAddError("Could not add contact info")
        return self.get(result.get_insert_id())

    def update(self, contact: Contact):
        parser = self.__get_parser(contact.get_type().get_id())
        parser.parse(contact.get_info())

        result = self.__contact_data.update(
            contact.get_id(),
            info=contact.get_info(),
            description=contact.get_description()
        )
        if not result.get_status():
            raise ContactUpdateError("Could not update contact info")

    def delete(self, contact_id):
        pass

    def get(self, contact_id) -> Contact:
        result = self.__contact_data.load(contact_id)
        if len(result.get_data()) == 0:
            raise ContactSearchError("Contact not found")
        return self.__build_contact_object(result.get_data()[0])

    def get_by_entity_id(self, entity_id) -> list:
        pass

    def __build_contact_object(self, data: dict) -> Contact:
        return Contact(
            id=data["id"],
            entity_id=data["entity_id"],
            type=self.__types.get_by_id(data["type_id"]),
            info=data["info"],
            description=data["description"]
        )

    def __get_parser(self, type_id) -> ContactParser:
        parsers = {
            self.__types.PHONE.get_id(): PhoneParser(),
            self.__types.EMAIL.get_id(): EmailParser(),
            self.__types.WEBSITE.get_id(): WebsiteParser()
        }
        if type_id not in parsers:
            raise Exception("Type cannot be parsed")
        return parsers[type_id]
