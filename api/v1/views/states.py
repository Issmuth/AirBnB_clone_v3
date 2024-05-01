#!/usr/bin/python3
"""
Module of view for States objects api.
"""
from api.v1.views import app_views
from models import storage
from models.state import State
import json
from flask import Response, abort, jsonify, request


@app_views.route('/states',
                 strict_slashes=False,
                 methods=['GET'])
def states():
    """retrieves all state objects."""
    objects = storage.all(State)
    state_dicts = []
    for v in objects.values():
        state_dicts.append(v.to_dict())

    state_json = json.dumps(state_dicts, indent=2) + '\n'
    response = Response(response=state_json,
                        status=200,
                        mimetype='application/json')
    return response


@app_views.route('/states/<state_id>',
                 strict_slashes=False,
                 methods=['GET'])
def states_by_id(state_id):
    """retrieve a state object using id."""
    state = storage.get(State, state_id)
    if state is not None:
        data = json.dumps(state.to_dict(), indent=2) + '\n'
        reponse = Response(response=data,
                           status=200,
                           mimetype='application/json')
        return reponse
    else:
        abort(404)


@app_views.route('/states/<state_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def states_delete(state_id):
    """Deletes a state object using id."""
    state = storage.get(State, state_id)
    if state is not None:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states',
                 strict_slashes=False,
                 methods=['POST'])
def states_create():
    """creates a state object."""
    if not request.get_json():
        abort(400, "Not a JSON")

    if 'name' not in request.json:
        abort(400, "Missing name")

    name = request.get_json()['name']
    state = State(name=name)
    storage.new(state)
    storage.save()
    data = json.dumps(state.to_dict(), indent=2) + '\n'
    reponse = Response(response=data,
                       status=201,
                       mimetype='application/json')
    return reponse


@app_views.route('/states/<state_id>',
                 strict_slashes=False,
                 methods=['PUT'])
def state_update(state_id):
    """updates a state objects."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state_update = request.get_json()
    if not state_update:
        abort(400, "Not a JSON")

    for k, v in state_update.items():
        skips = ["id", "created_at", "updated_at"]
        if k not in skips:
            setattr(state, k, v)

    state.save()
    data = json.dumps(state.to_dict(), indent=2) + '\n'
    reponse = Response(response=data,
                       status=200,
                       mimetype='application/json')
    return reponse
