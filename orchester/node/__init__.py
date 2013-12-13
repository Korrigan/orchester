"""
This module is the entry point of the orchester-node daemon

"""

from flask import Flask
from flask import jsonify

version = '0.0.1'
api_version = '0.0.1'

app = Flask(__name__)


@app.route('/')
def index():
    """
    The API root
    Provides nothing useful unless version reports.

    """
    data = {
        'version': version,
        'api_version': api_version,
    }
    return jsonify(data)
 
