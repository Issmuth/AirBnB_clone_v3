#!/usr/bin/python3
"""Routes for the blueprint."""
from api.v1.views import app_views
import json


@app_views.route('/status')
def status():
    """Returns OK status in json format."""
    stat = {
        "status": "OK"
    }
    return (json.dumps(stat, indent=2) + '\n')
