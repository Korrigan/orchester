"""
Root API endpoint for the master
Makes a clever use of the index generator for orchester

"""

from flask import Blueprint

from orchester.api import views

from .application import application

version = '0.0.1'
index = Blueprint('index', __name__)


@index.route('/')
def index_index():
    return views.index(service='master',
                       capabilities=[],
                       version=version)

def register(app):
    """Register all API modules"""

    app.register_blueprint(index)
    app.register_blueprint(application, url_prefix='/app')
