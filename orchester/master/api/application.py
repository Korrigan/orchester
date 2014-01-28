"""
Contains client API views related to applications
URL prefix: /app

"""

from flask import Blueprint
from flask import url_for
from flask.views import MethodView

from orchester.api.views import APIDetailUpdateDeleteView, APIListCreateView, APIModelViewMixin
from orchester.api.views import api_redirect

from orchester.master.models.application import Application
from orchester.master.models.worker import Worker


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
        for w in Worker.objects.filter(app=obj):
            data['workers'].append(url_for('worker.wkr_detail', _external=True,
                                           id=w.cleaned_id))
        return data


class AppDeployView(MethodView, APIModelViewMixin, AppViewMixin):
    """
    Handles a POST request with no data and deploy an application

    """
    methods = ['POST',]

    def post(self, *args, **kwargs):
        """
        Deploy an application
        This method takes custom overrides for the following attributes
        (application will be updated):
        - to be defined and implemented

        """
        from orchester.master import master

        app = self.get_object(kwargs['app_id'])
        master.deploy(app)
        return api_redirect(self.get_object_url(app))


application.add_url_rule('/', 'index', AppIndexView.as_view('index'))
application.add_url_rule('/<app_id>', 'app_detail', AppView.as_view('app_detail'))
application.add_url_rule('/<app_id>/deploy', 'app_deploy', AppDeployView.as_view('app_deploy'))
