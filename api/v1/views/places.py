#!/usr/bin/python3
"""
Module of view for Place objects api.
"""

from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
import json
from os import getenv
from flask import Response, abort, jsonify, request


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False,
                 methods=['GET'])
def places(city_id):
    """retrieve places list."""
    city = storage.get(City, city_id)
    if city is not None:
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            places = city.places
        else:
            places = city.places()

        place_list = []
        for place in places:
            place_list.append(place.to_dict())
        data = json.dumps(place_list, indent=2) + '\n'
        reponse = Response(response=data,
                           status=200,
                           mimetype='application/json')
        return reponse
    else:
        abort(404)


@app_views.route('/places/<place_id>',
                 strict_slashes=False,
                 methods=['GET'])
def place_by_id(place_id):
    """retrieve a place object using id."""
    place = storage.get(Place, place_id)
    if place is not None:
        data = json.dumps(place.to_dict(), indent=2) + '\n'
        reponse = Response(response=data,
                           status=200,
                           mimetype='application/json')
        return reponse
    else:
        abort(404)


@app_views.route('/places/<place_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def places_delete(place_id):
    """Deletes a place object using id."""
    place = storage.get(Place, place_id)
    if place is not None:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False,
                 methods=['POST'])
def places_create(city_id):
    """creates a place object."""
    attrs = request.get_json()

    if not attrs:
        abort(400, "Not a JSON")

    if 'user_id' not in attrs.keys():
        abort(400, "Missing user_id")

    if 'name' not in attrs.keys():
        abort(400, "Missing name")

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    place = Place(**attrs)
    place.city_id = city.id
    storage.new(place)
    storage.save()
    data = json.dumps(place.to_dict(), indent=2) + '\n'
    reponse = Response(response=data,
                       status=201,
                       mimetype='application/json')
    return reponse


@app_views.route('/places/<place_id>',
                 strict_slashes=False,
                 methods=['PUT'])
def place_update(place_id):
    """updates a place object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place_update = request.get_json()
    if not place_update:
        abort(400, "Not a JSON")

    for k, v in place_update.items():
        skips = ["id", "created_at", "updated_at"]
        if k not in skips:
            setattr(place, k, v)

    place.save()
    data = json.dumps(place.to_dict(), indent=2) + '\n'
    reponse = Response(response=data,
                       status=200,
                       mimetype='application/json')
    return reponse
