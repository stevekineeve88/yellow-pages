from flask import Blueprint, request

from modules.api.handlers.entity_error_code_handler import EntityErrorCodeParser
from modules.api.objects.response import Response
from modules.api.objects.transformers.entity_status_transformer import EntityStatusTransformer
from modules.api.objects.transformers.entity_transformer import EntityTransformer
from modules.entity.managers.entity_manager import EntityManager
from modules.entity.managers.entity_status_manager import EntityStatusManager

entity_api = Blueprint("entity_api", __name__)
ROOT = "/api/entity"


@entity_api.route(f"{ROOT}/<uuid>", methods=["GET"])
def get(uuid: str):
    """ GET entity API route
    Args:
        uuid (str):
    Returns:
        json
    """
    error_code_parser = EntityErrorCodeParser()

    try:
        entity_manager = EntityManager()
        entity = entity_manager.get_by_uuid(uuid)
        return Response([EntityTransformer(entity)]).get_response()
    except Exception as e:
        return Response(
            [],
            str(e),
            error_code_parser.get_code(type(e).__name__)
        ).get_response()


@entity_api.route(f"{ROOT}/search", methods=["GET"])
def search():
    """ GET entities by search API route
    Returns:
        json
    """
    error_code_parser = EntityErrorCodeParser()

    params = request.args
    name = params.get("name") if "name" in params else ""
    address = params.get("address") if "address" in params else ""
    statuses = params.get("statuses") if "statuses" in params else []
    tags = params.get("tags") if "tags" in params else []
    limit = params.get("limit") if "limit" in params else 100
    offset = params.get("offset") if "offset" in params else 0
    try:
        entity_manager = EntityManager()
        result = entity_manager.search(
            name=name,
            address=address,
            statuses=statuses,
            tags=tags,
            limit=int(limit),
            offset=int(offset)
        )
        entities = result.get_data()
        response = Response([EntityTransformer(entity) for entity in entities])
        response.set_meta_data({"full_count": result.get_full_count()})
        return response.get_response()
    except Exception as e:
        return Response(
            [],
            str(e),
            error_code_parser.get_code(type(e).__name__)
        ).get_response()


@entity_api.route(f"{ROOT}/search/<latitude>/<longitude>/<miles>", methods=["GET"])
def search_nearby(latitude: float, longitude: float, miles: int):
    """ GET nearby entities API route
    Args:
        latitude (float):           Current latitude
        longitude (float):          Current longitude
        miles (int):                Maximum distance
    Returns:
        json
    """
    error_code_parser = EntityErrorCodeParser()

    params = request.args
    name = params.get("name") if "name" in params else ""
    address = params.get("address") if "address" in params else ""
    statuses = params.get("statuses") if "statuses" in params else []
    tags = params.get("tags") if "tags" in params else []
    limit = params.get("limit") if "limit" in params else 100
    offset = params.get("offset") if "offset" in params else 0
    try:
        entity_manager = EntityManager()
        result = entity_manager.search_nearby(
            float(latitude),
            float(longitude),
            int(miles),
            name=name,
            address=address,
            statuses=statuses,
            tags=tags,
            limit=int(limit),
            offset=int(offset)
        )
        entities = result.get_data()
        response = Response([EntityTransformer(entity) for entity in entities])
        response.set_meta_data({"full_count": result.get_full_count()})
        return response.get_response()
    except Exception as e:
        return Response(
            [],
            str(e),
            error_code_parser.get_code(type(e).__name__)
        ).get_response()


@entity_api.route(f"{ROOT}/statuses")
def get_statuses():
    """ GET statuses API route
    Returns:
        json
    """
    error_code_parser = EntityErrorCodeParser()

    try:
        status_manager = EntityStatusManager()
        statuses = status_manager.get_all().get_all()
        return Response([EntityStatusTransformer(status) for key, status in statuses.items()]).get_response()
    except Exception as e:
        return Response(
            [],
            str(e),
            error_code_parser.get_code(type(e).__name__)
        ).get_response()
