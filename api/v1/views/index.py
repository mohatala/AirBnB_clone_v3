#!/usr/bin/python3xx
'''api status'''
import models
from models import storage
from models.base_model import BaseModel
from flask import jsonify
from api.v1.views import app_views
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User

@app_views.route('/status', strict_slashes=False)
def returnstuff():
    '''return ok'''
    return jsonify(status='OK')


@app_views.route('/stats', strict_slashes=False)
def stuff():
    '''JSON Response'''
    classes = {'states': State,
             'users': User,
             'amenities': Amenity,
             'cities': City,
             'places': Place,
             'reviews': Review}
    for key in classes:
        classes[key] = storage.count(classes[key])
    return jsonify(classes)
