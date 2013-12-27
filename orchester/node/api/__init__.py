"""
Root API endpoint for orchester-node
Based on index helper for orchester

"""

from flask import Blueprint

from orchester.api import views


version = '0.0.1'
index = Blueprint('index', __name__)


@index.route('/')
def index_index():
    return views.index(service='node',
                       capabilities=['worker', 'lb'],
                       version=version)
