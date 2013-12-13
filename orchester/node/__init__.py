"""
This module is the entry point of the orchester-node daemon

"""

from flask import Flask
from flask import jsonify

version = '0.0.1'
api_version = '0.0.1'

app = Flask('orchester.node')


@app.route('/')
def index():
    """
    The API root endpoint.
    Provides information about the node and its capacities.

    """
    data = {
        'service': 'node',
        'capabilities': [
            'instance',
            'lb',
        ],
        'version': version,
        'api_version': api_version,
    }
    return jsonify(data)
 
