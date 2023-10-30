#!/usr/bin/python3
"""
Flask App
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, render_template, url_for
from flask_cors import CORS, cross_origin
from models import storage
import os
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

app.url_map.strict_slashes = False

host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)

cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """
    after each request, this method calls .close()
    """
    storage.close()


@app.errorhandler(404)
def handle_error_404(exception):
    """
    handles 404 errors
    """
    code = exception.__str__().split()[0]
    description = exception.description
    msg = {'error': description}
    return make_response(jsonify(msg), code)


@app.errorhandler(400)
def handle_error_404(exception):
    """
    handles 400 errros
    """
    code = exception.__str__().split()[0]
    description = exception.description
    msg = {'error': description}
    return make_response(jsonify(msg), code)


@app.errorhandler(Exception)
def global_error_handler(err):
    """
        Global Route to handle All Error Codes
    """
    if isinstance(err, HTTPException):
        if type(err).__name__ == 'NotFound':
            err.description = "Not found"
        msg = {'error': err.description}
        code = err.code
    else:
        msg = {'error': err}
        code = 500
    return make_response(jsonify(msg), code)


def setup_global_errors():
    """
    This updates HTTPException Class with custom error function
    """
    for cls in HTTPException.__subclasses__():
        app.register_error_handler(cls, global_error_handler)


if __name__ == "__main__":
    """
    MAIN Flask App
    """
    # initializes global error handling
    setup_global_errors()
    # start Flask app
    app.run(host=host, port=port)
