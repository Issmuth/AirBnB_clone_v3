#!/usr/bin/python3
"""Routes for the blueprint."""
from api.v1.views import app_views
from flask import jsonify
import json

@app_views.route('/status')
def status():
    """Returns OK status in json format."""
    stat = { 
        "status": "OK"
    }
    return jsonify(stat)
