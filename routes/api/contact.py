from flask import Blueprint
from modules.api.handlers.contact_error_code_handler import ContactErrorCodeParser
from modules.api.objects.response import Response
from modules.api.objects.transformers.contact_transformer import ContactTransformer
from modules.contact.managers.contact_manager import ContactManager

contact_api = Blueprint("contact_api", __name__)
ROOT = "/api/contact"


@contact_api.route(f"{ROOT}/<entity_id>", methods=["GET"])
def get(entity_id):
    """ GET contacts by entity id API route
    Args:
        entity_id (ID):
    Returns:
        json
    """
    error_code_parser = ContactErrorCodeParser()

    try:
        contact_manager = ContactManager()
        contacts = contact_manager.get_by_entity_id(entity_id)
        return Response([ContactTransformer(contact) for contact in contacts]).get_response()
    except Exception as e:
        return Response([], str(e), error_code_parser.get_code(Exception.__name__)).get_response()
