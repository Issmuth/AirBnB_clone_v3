#!/usr/bin/python3
"""creates an app that registers blueprints."""
from flask import Flask, Response
from models import storage
from api.v1.views import app_views
import json

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def clear(exc):
    """reloads storage using close method."""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    error = {
        "error": "Not found"
    }
    data = json.dumps(error, indent=2) + '\n'
    response = Response(data,
                        status=404,
                        mimetype="application/json")
    return response


if __name__ == "__main__":
    try:
        host = os.environ.get('HBNB_API_HOST')
    except Exception:
        host = '0.0.0.0'

    try:
        port = os.environ.get('HBNB_API_PORT')
    except Exception:
        port = '5000'
