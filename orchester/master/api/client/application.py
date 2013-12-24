"""
Contains client API views related to applications
URL prefix: /app

"""

from flask import Blueprint
from flask import url_for, jsonify

from orchester.api.views import APIDetailView, APIListCreateView

from orchester.master.models.application import Application

application = Blueprint('application', __name__)


class AppViewMixin(object):
    """
    This class contains view parameters for application view classes

    """
    view_name = '.app_detail'
    view_arg_name = 'app_id'
    model = Application
    required_fields = [
        'domain_name',
        'code_type',
        'code_url',
        'min_workers'
    ]
    optional_fields = [
        'code_tag',
        'max_workers',
        'env_vars'
    ]


class AppIndexView(APIListCreateView, AppViewMixin):
    """
    /app/ endpoint
    GET returns the application list
    POST create a new application

    """
    data_list_key = 'apps'


class AppView(APIDetailView, AppViewMixin):
    """
    /app/<app_id>/ endpoint
    GET returns detailed info about application
    PUT updates the application
    DELETE deletes the application

    """
    display_fields = [
        ('id', '_id'),
        'code_tag',
        'max_workers',
        'env_vars',
        'domain_name',
        'code_type',
        'code_url',
        'min_workers'
    ]


application.add_url_rule('/', 'index', AppIndexView.as_view('index'))
application.add_url_rule('/<app_id>', 'app_detail', AppView.as_view('app_detail'))
