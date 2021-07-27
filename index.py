from flask import \
    Flask
from routes.api.entity import entity_api

app = Flask(__name__)

app.register_blueprint(entity_api)


@app.route("/")
def index():
    """ Home page
    Returns:
        str
    """
    return "Hello World"
