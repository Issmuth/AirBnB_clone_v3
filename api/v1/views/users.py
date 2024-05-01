#!/usr/bin/python3
"""
Module of view for Users objects api.
"""

from api.v1.views import app_views
from models import storage
from models.user import User
import json
from flask import Response, abort, jsonify, request


@app_views.route('/users',
                 strict_slashes=False,
                 methods=['GET'])
def users():
    """retrieves all user objects."""
    objects = storage.all(User)
    user_dicts = []
    for v in objects.values():
        user_dicts.append(v.to_dict())

    user_json = json.dumps(user_dicts, indent=2) + '\n'
    response = Response(response=user_json,
                        status=200,
                        mimetype='application/json')
    return response


@app_views.route('/users/<user_id>',
                 strict_slashes=False,
                 methods=['GET'])
def users_by_id(user_id):
    """retrieve a user object using id."""
    user = storage.get(User, user_id)
    if user is not None:
        data = json.dumps(user.to_dict(), indent=2) + '\n'
        reponse = Response(response=data,
                           status=200,
                           mimetype='application/json')
        return reponse
    else:
        abort(404)


@app_views.route('/users/<user_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def users_delete(user_id):
    """Deletes a user object using id."""
    user = storage.get(User, user_id)
    if user is not None:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users',
                 strict_slashes=False,
                 methods=['POST'])
def users_create():
    """creates a user object."""
    if not request.get_json():
        abort(400, "Not a JSON")

    if 'email' not in request.json:
        abort(400, "Missing email")

    if 'password' not in request.json:
        abort(400, "Missing password")

    attrs = request.get_json()
    user = User(**attrs)
    storage.new(user)
    storage.save()
    data = json.dumps(user.to_dict(), indent=2) + '\n'
    reponse = Response(response=data,
                       status=201,
                       mimetype='application/json')
    return reponse


@app_views.route('/users/<user_id>',
                 strict_slashes=False,
                 methods=['PUT'])
def user_update(user_id):
    """updates a user objects."""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user_update = request.get_json()
    if not user_update:
        abort(400, "Not a JSON")

    for k, v in user_update.items():
        skips = ["id", "created_at", "updated_at"]
        if k not in skips:
            setattr(user, k, v)

    user.save()
    data = json.dumps(user.to_dict(), indent=2) + '\n'
    reponse = Response(response=data,
                       status=200,
                       mimetype='application/json')
    return reponse
