"""
Root API endpoint for the master
Makes a clever use of the index generator for orchester

"""

from flask import Blueprint

from orchester.api import views

from .application import application
from .worker import worker
from .node import node


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
    app.register_blueprint(worker, url_prefix='/worker')
    app.register_blueprint(node, url_prefix='/node')
