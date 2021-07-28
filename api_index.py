from flask import Flask
from routes.api.contact import contact_api
from routes.api.entity import entity_api
from routes.api.tag import tag_api

api = Flask(__name__)

api.register_blueprint(entity_api)
api.register_blueprint(contact_api)
api.register_blueprint(tag_api)
