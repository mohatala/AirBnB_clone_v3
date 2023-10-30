#!/usr/bin/python3
""" Authors : Mazoz / Talaini
State objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import abort, request, jsonify


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=["GET"])
def cities(state_id):
    """show cities"""
    cities_list = []
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    cities = state_obj.cities
    for city in cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["GET"])
def cities_id(city_id):
    """Retrieves a City object"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    return jsonify(city_obj.to_dict())


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["DELETE"])
def city_delete(city_id):
    """delete method"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    storage.delete(city_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=["POST"])
def create_city(state_id):
    """create a new post req"""
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    new_state = City(state_id=state_obj.id, **data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["PUT"])
def update_city(city_id):
    """update city"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    city_obj.name = data.get("name", city_obj.name)
    city_obj.save()
    return jsonify(city_obj.to_dict()), 200
