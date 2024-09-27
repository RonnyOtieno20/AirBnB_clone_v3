#!/usr/bin/python3
'''Contains a Flask web application API.'''
import os
from flask import Flask, jsonify
from flask_cors import CORS

from models import storage
from api.v1.views import app_views


app = Flask(__name__)
'''The Flask web application instance.'''
app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
app_port = int(os.getenv('HBNB_API_PORT', '5002'))  # Changed to 5002
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources={'/*': {'origins': '*'}})  # Allow all origins for now


@app.teardown_appcontext
def teardown_flask(exception):
    '''The Flask app/request context end event listener.'''
    storage.close()


@app.errorhandler(404)
def error_404(error):
    '''Handles the 404 HTTP error code.'''
    return jsonify(error='Not found'), 404


@app.errorhandler(400)
def error_400(error):
    '''Handles the 400 HTTP error code.'''
    msg = 'Bad request'
    if isinstance(error, Exception) and hasattr(error, 'description'):
        msg = error.description
    return jsonify(error=msg), 400


@app.route('/api/v1/states', methods=['GET'])
def get_states():
    '''Retrieves the list of all State objects'''
    states = storage.all("State").values()
    return jsonify([state.to_dict() for state in states])


if __name__ == '__main__':
    app.run(
        host=app_host,
        port=app_port,
        threaded=True,
        debug=True  # Enable debug mode
    )
