#!/usr/bin/python3
"""
Module of view for City objects api.
"""

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import City
import json
from os import getenv
from flask import Response, abort, jsonify, request


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False,
                 methods=['GET'])
def reviews(place_id):
    """retrieve reviews list."""
    place = storage.get(Place, place_id)
    if place is not None:
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            reviews = place.reviews
        else:
            reviews = place.reviews()

        review_list = []
        for review in reviews:
            review_list.append(city.to_dict())
        data = json.dumps(review_list, indent=2) + '\n'
        reponse = Response(response=data,
                           status=200,
                           mimetype='application/json')
        return reponse
    else:
        abort(404)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False,
                 methods=['GET'])
def review_by_id(city_id):
    """retrieve a review object using id."""
    review = storage.get(City, city_id)
    if review is not None:
        data = json.dumps(review.to_dict(), indent=2) + '\n'
        reponse = Response(response=data,
                           status=200,
                           mimetype='application/json')
        return reponse
    else:
        abort(404)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def reviews_delete(review_id):
    """Deletes a review object using id."""
    review = storage.get(City, city_id)
    if review is not None:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False,
                 methods=['POST'])
def reviews_create(place_id):
    """creates a review object."""
    attrs = request.get_json()

    if not attrs:
        abort(400, "Not a JSON")

    if 'user_id' not in attrs.keys():
        abort(400, "Missing user_id")

    if 'text' not in attrs.keys():
        abort(400, "Missing text")

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    review = City(**attrs)
    review.place_id = place.id
    storage.new(review)
    storage.save()
    data = json.dumps(review.to_dict(), indent=2) + '\n'
    reponse = Response(response=data,
                       status=201,
                       mimetype='application/json')
    return reponse


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False,
                 methods=['PUT'])
def review_update(city_id):
    """updates a review object."""
    review = storage.get(City, city_id)
    if review is None:
        abort(404)
    review_update = request.get_json()
    if not review_update:
        abort(400, "Not a JSON")

    for k, v in review_update.items():
        skips = ["user_id", "place_id", "id", "created_at", "updated_at"]
        if k not in skips:
            setattr(review, k, v)

    review.save()
    data = json.dumps(review.to_dict(), indent=2) + '\n'
    reponse = Response(response=data,
                       status=200,
                       mimetype='application/json')
    return reponse
