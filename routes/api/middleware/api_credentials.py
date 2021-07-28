from functools import wraps
from flask import request
from environment import Environment
from modules.api.handlers.abstracts.error_code_handler import ErrorCodeHandler
from modules.api.objects.response import Response


def api_credentials():
    """ API credential middleware
    Returns:
        json
    """
    def _api_credentials(func):
        @wraps(func)
        def __wrapper(*args, **kwargs):
            env: Environment = Environment()
            access_id = request.headers.get("access_id") or ""
            secret = request.headers.get("secret") or ""
            if access_id == env.get(env.API_ACCESS_ID) and secret == env.get(env.API_SECRET):
                return func(*args, **kwargs)
            return Response([], "Access Denied", ErrorCodeHandler.FORBIDDEN).get_response()
        return __wrapper
    return _api_credentials
