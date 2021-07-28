from flask import Flask
from routes.api.contact import contact_api
from routes.api.entity import entity_api

app = Flask(__name__)

app.register_blueprint(entity_api)
app.register_blueprint(contact_api)


@app.route("/")
def index():
    """ Home page
    Returns:
        str
    """
    return "Hello World"
