from singleton_decorator import singleton
from modules.contact.data.contact_data import ContactData
from modules.contact.exceptions.contact_add_error import ContactAddError
from modules.contact.exceptions.contact_delete_error import ContactDeleteError
from modules.contact.exceptions.contact_search_error import ContactSearchError
from modules.contact.exceptions.contact_update_error import ContactUpdateError
from modules.contact.managers.contact_type_manager import ContactTypeManager
from modules.contact.objects.contact import Contact
from modules.contact.objects.contact_parser import ContactParser
from modules.contact.objects.parsers.email_parser import EmailParser
from modules.contact.objects.parsers.phone_parser import PhoneParser
from modules.contact.objects.parsers.website_parser import WebsiteParser
from modules.util.objects.data_list import DataList


@singleton
class ContactManager:
    """ Manager class for contact CRUD operations
    """
    def __init__(self, **kwargs):
        """ Constructor for ContactManager
        Args:
            **kwargs:   Optional dependencies
                contact_data (ContactData)
                contact_type_manager (ContactTypeManager)
        """
        self.__contact_data: ContactData = kwargs.get("contact_data") or ContactData()
        type_manager: ContactTypeManager = kwargs.get("contact_type_manager") or ContactTypeManager()
        self.__types: DataList = type_manager.get_all()

    def add(self, entity_id, **kwargs) -> Contact:
        """ Add contact to entity
        Args:
            entity_id (ID):      Entity ID
            **kwargs:
                type_id (ID)
                info (str)
                description (str)
        Returns:
            Contact
        """
        type_id = kwargs.get("type_id")
        info = kwargs.get("info")

        parser = self.__get_parser(type_id)
        parser.parse(info)

        result = self.__contact_data.add(entity_id, **kwargs)
        if not result.get_status():
            raise ContactAddError("Could not add contact info")
        return self.get(result.get_insert_id())

    def update(self, contact: Contact):
        """ Update contact
        Args:
            contact (Contact):      Contact obj with updated info
        """
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
        """ Delete contact by ID
        Args:
            contact_id (ID):         Contact ID
        """
        result = self.__contact_data.delete(contact_id)
        if not result.get_status():
            raise ContactDeleteError("Could not delete contact")

    def get(self, contact_id) -> Contact:
        """ Get contact by ID
        Args:
            contact_id (ID):         Contact ID
        Returns:
            Contact
        """
        result = self.__contact_data.load(contact_id)
        if len(result.get_data()) == 0:
            raise ContactSearchError("Contact not found")
        return self.__build_contact_object(result.get_data()[0])

    def get_by_entity_id(self, entity_id) -> list:
        """ Get contacts by entity ID
        Args:
            entity_id (ID):      Entity ID
        Returns:
            list
        """
        result = self.__contact_data.load_by_entity_id(entity_id)
        if not result.get_status():
            raise ContactSearchError("Could not find contacts for entity")
        data = result.get_data()
        contacts = []
        for datum in data:
            contacts.append(self.__build_contact_object(datum))
        return contacts

    def __build_contact_object(self, data: dict) -> Contact:
        """ Build contact object
        Args:
            data (dict):
        Returns:
            Contact
        """
        return Contact(
            id=data["id"],
            entity_id=data["entity_id"],
            type=self.__types.get_by_id(data["type_id"]),
            info=data["info"],
            description=data["description"]
        )

    def __get_parser(self, type_id) -> ContactParser:
        """ Get parser by type ID
        Args:
            type_id (ID):        Type ID
        Returns:
            ContactParser
        """
        parsers = {
            self.__types.PHONE.get_id(): PhoneParser(),
            self.__types.EMAIL.get_id(): EmailParser(),
            self.__types.WEBSITE.get_id(): WebsiteParser()
        }
        if type_id not in parsers:
            raise Exception("Type cannot be parsed")
        return parsers[type_id]
