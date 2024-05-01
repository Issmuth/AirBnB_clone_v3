#!/usr/bin/python3
"""Routes for the blueprint."""
from api.v1.views import app_views
from flask import Response
import json


@app_views.route('/status')
def status():
    """Returns OK status in json format."""
    stat = {
        "status": "OK"
    }
    data = json.dumps(stat, indent=2) + '\n'
    resp = Response(response=data, status=200,
                    mimetype="application/json")
    return resp
