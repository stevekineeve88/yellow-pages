from flask import Blueprint
from modules.api.handlers.tag_error_code_handler import TagErrorCodeParser
from modules.api.objects.response import Response
from modules.api.objects.transformers.tag_type_transformer import TagTypeTransformer
from modules.tag.managers.tag_type_manager import TagTypeManager
from routes.api.middleware.api_credentials import api_credentials

tag_api = Blueprint("tag_api", __name__)
ROOT = "/tag"


@tag_api.route(f"{ROOT}", methods=["GET"])
@api_credentials()
def get():
    """ Get tag types API route
    Returns:
        json
    """
    error_code_parser = TagErrorCodeParser()

    try:
        tag_type_manager = TagTypeManager()
        types = tag_type_manager.get_all().get_all()
        return Response([TagTypeTransformer(tag_type) for key, tag_type in types.items()]).get_response()
    except Exception as e:
        return Response(
            [],
            str(e),
            error_code_parser.get_code(type(e).__name__)
        ).get_response()
