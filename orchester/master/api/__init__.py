"""
Root API endpoint for the master
Makes a clever use of the index generator for orchester

"""

from flask import Blueprint

from orchester.api import views


version = '0.0.1'
index = Blueprint('index', __name__)


@index.route('/')
def index_index():
    return views.index(service='master',
                       capabilities=[],
                       version=version)

def register(app):
    """Register all API modules"""
    from .client import register as register_client

    app.register_blueprint(index)
    register_client(app)
