#!/usr/bin/python3
"""
Module of view for Amenity objects api.
"""

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
import json
from flask import Response, abort, jsonify, request


@app_views.route('/amenities',
                 strict_slashes=False,
                 methods=['GET'])
def amenities():
    """retrieves all amenity objects."""
    objects = storage.all(Amenity)
    amenity_dicts = []
    for v in objects.values():
        amenity_dicts.append(v.to_dict())

    amenity_json = json.dumps(amenity_dicts, indent=2) + '\n'
    response = Response(response=amenity_json,
                        status=200,
                        mimetype='application/json')
    return response


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['GET'])
def amenities_by_id(amenity_id):
    """retrieve a amenity object using id."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is not None:
        data = json.dumps(amenity.to_dict(), indent=2) + '\n'
        reponse = Response(response=data,
                           status=200,
                           mimetype='application/json')
        return reponse
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def amenities_delete(amenity_id):
    """Deletes a amenity object using id."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is not None:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities',
                 strict_slashes=False,
                 methods=['POST'])
def amenities_create():
    """creates a amenity object."""
    if not request.get_json():
        abort(400, "Not a JSON")

    if 'name' not in request.json.keys():
        abort(400, "Missing name")

    attrs = request.get_json()
    amenity = Amenity(**attrs)
    storage.new(amenity)
    storage.save()
    data = json.dumps(amenity.to_dict(), indent=2) + '\n'
    reponse = Response(response=data,
                       status=201,
                       mimetype='application/json')
    return reponse


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['PUT'])
def amenity_update(amenity_id):
    """updates a amenity objects."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity_update = request.get_json()
    if not amenity_update:
        abort(400, "Not a JSON")

    for k, v in amenity_update.items():
        skips = ["id", "created_at", "updated_at"]
        if k not in skips:
            setattr(amenity, k, v)

    amenity.save()
    data = json.dumps(amenity.to_dict(), indent=2) + '\n'
    reponse = Response(response=data,
                       status=200,
                       mimetype='application/json')
    return reponse
