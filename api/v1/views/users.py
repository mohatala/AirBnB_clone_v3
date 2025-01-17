#!/usr/bin/python3
"""Authors : Mazoz / Talaini
State objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from models.user import User
from flask import abort, request, jsonify


@app_views.route("/users", strict_slashes=False, methods=["GET"])
@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=["GET"])
def user(user_id=None):
    """show user and user with id"""
    user_list = []
    if user_id is None:
        all_objs = storage.all(User).values()
        for v in all_objs:
            user_list.append(v.to_dict())
        return jsonify(user_list)
    else:
        result = storage.get(User, user_id)
        if result is None:
            abort(404)
        return jsonify(result.to_dict())


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=["DELETE"])
def user_delete(user_id):
    """delete method"""
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)
    storage.delete(user_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def create_user():
    """create a new post req"""
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    if "email" not in data:
        abort(400, "Missing email")
    if "password" not in data:
        abort(400, "Missing password")
    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=["PUT"])
def update_user(user_id):
    """update user"""
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    user_obj.password = data.get("password", user_obj.password)
    user_obj.first_name = data.get("first_name", user_obj.first_name)
    user_obj.last_name = data.get("last_name", user_obj.last_name)
    user_obj.save()
    return jsonify(user_obj.to_dict()), 200
