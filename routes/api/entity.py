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
    error_code_parser = EntityErrorCodeParser()

    params = request.args
    name = params.get("name") if "name" in params else ""
    address = params.get("address") if "address" in params else ""
    statuses = params.get("statuses") if "statuses" in params else []
    try:
        entity_manager = EntityManager()
        entities = entity_manager.search(
            name=name,
            address=address,
            statuses=statuses
        )
        return Response([EntityTransformer(entity) for entity in entities]).get_response()
    except Exception as e:
        return Response(
            [],
            str(e),
            error_code_parser.get_code(type(e).__name__)
        ).get_response()


@entity_api.route(f"{ROOT}/search/<latitude>/<longitude>/<miles>", methods=["GET"])
def search_nearby(latitude: float, longitude: float, miles: int):
    error_code_parser = EntityErrorCodeParser()

    params = request.args
    name = params.get("name") if "name" in params else ""
    address = params.get("address") if "address" in params else ""
    statuses = params.get("statuses") if "statuses" in params else []
    try:
        entity_manager = EntityManager()
        entities = entity_manager.search_nearby(
            latitude,
            longitude,
            miles,
            name=name,
            address=address,
            statuses=statuses
        )
        return Response([EntityTransformer(entity) for entity in entities]).get_response()
    except Exception as e:
        return Response(
            [],
            str(e),
            error_code_parser.get_code(type(e).__name__)
        ).get_response()


@entity_api.route(f"{ROOT}/statuses")
def get_statuses():
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
