#!/usr/bin/python3
"""
Module of view for City objects api.
"""

from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
import json
from os import getenv
from flask import Response, abort, jsonify, request


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False,
                 methods=['GET'])
def cities(state_id):
    """retrieve cities list."""
    state = storage.get(State, state_id)
    if state is not None:
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            cities = state.cities
        else:
            cities = state.cities()

        city_list = []
        for city in cities:
            city_list.append(city.to_dict())
        data = json.dumps(city_list, indent=2) + '\n'
        reponse = Response(response=data,
                           status=200,
                           mimetype='application/json')
        return reponse
    else:
        abort(404)


@app_views.route('/cities/<city_id>',
                 strict_slashes=False,
                 methods=['GET'])
def city_by_id(city_id):
    """retrieve a city object using id."""
    city = storage.get(City, city_id)
    if city is not None:
        data = json.dumps(city.to_dict(), indent=2) + '\n'
        reponse = Response(response=data,
                           status=200,
                           mimetype='application/json')
        return reponse
    else:
        abort(404)


@app_views.route('/cities/<city_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def cities_delete(city_id):
    """Deletes a city object using id."""
    city = storage.get(City, city_id)
    if city is not None:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False,
                 methods=['POST'])
def cities_create(state_id):
    """creates a city object."""
    attrs = request.get_json()

    if not attrs:
        abort(400, "Not a JSON")

    if 'name' not in attrs.keys():
        abort(400, "Missing name")

    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    city = City(**attrs)
    city.state_id = state.id
    storage.new(city)
    storage.save()
    data = json.dumps(city.to_dict(), indent=2) + '\n'
    reponse = Response(response=data,
                       status=201,
                       mimetype='application/json')
    return reponse


@app_views.route('/cities/<city_id>',
                 strict_slashes=False,
                 methods=['PUT'])
def city_update(city_id):
    """updates a city object."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city_update = request.get_json()
    if city_update is None:
        abort(400, "Not a JSON")

    for k, v in city_update.items():
        skips = ["id", "created_at", "updated_at"]
        if k not in skips:
            setattr(city, k, v)

    city.save()
    data = json.dumps(city.to_dict(), indent=2) + '\n'
    reponse = Response(response=data,
                       status=200,
                       mimetype='application/json')
    return reponse
