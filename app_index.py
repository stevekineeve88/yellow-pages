from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    """ Home page
    Returns:
        str
    """
    return "Welcome to the Yellow Pages home page"
