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

app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def close_db(exception):
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
    msg = {"error": "Not found"}
    return jsonify(msg), code


@app.errorhandler(400)
def handle_error_400(exception):
    """
    handles 400 errros
    """
    code = exception.__str__().split()[0]
    description = exception.description
    msg = {'error': description}
    return jsonify(msg), code



if __name__ == "__main__":
    """
    start Flask App
    """
    app.run(host=host, port=port, threaded=True)
