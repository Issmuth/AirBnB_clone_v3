#!/usr/bin/python3
"""Routes for the blueprint."""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.user import User


@app_views.route('/status')
def status():
    """Returns OK status in json format."""
    stat = {
        "status": "OK"
    }
    return jsonify(stat)


@app_views.route('/stats')
def stats():
    """Return objects count of the classes."""
    stat = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(stat)
