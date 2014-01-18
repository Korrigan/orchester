"""
Contains client API views related to applications
URL prefix: /app

"""

from flask import Blueprint
from flask import url_for

from orchester.api.views import APIDetailUpdateDeleteView, APIListCreateView

from orchester.master.models.application import Application

application = Blueprint('application', __name__)


class AppViewMixin(object):
    """
    This class contains view parameters for application view classes

    """
    view_name = 'application.app_detail'
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


class AppIndexView(AppViewMixin, APIListCreateView):
    """
    /app/ endpoint
    GET returns the application list
    POST create a new application

    """
    data_list_key = 'apps'


class AppView(APIDetailUpdateDeleteView, AppViewMixin):
    """
    /app/<app_id>/ endpoint
    GET returns detailed info about application
    PUT updates the application
    DELETE deletes the application

    """
    display_fields = [
        ('id', 'cleaned_id'),
        'code_tag',
        'max_workers',
        'env_vars',
        'domain_name',
        'code_type',
        'code_url',
        'min_workers',
        'public_key',
    ]

    def get_object_data(self, obj):
        """
        This method overloads get_object_data to add worker list by urls

        """
        data = super(AppView, self).get_object_data(obj)
        data['workers'] = []
        for w in obj.workers:
            data['workers'].append(url_for('worker.wkr_detail', _external=True,
                                           id=str(w.id)))
        return data


application.add_url_rule('/', 'index', AppIndexView.as_view('index'))
application.add_url_rule('/<app_id>', 'app_detail', AppView.as_view('app_detail'))
