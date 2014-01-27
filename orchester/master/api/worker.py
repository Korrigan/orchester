"""
Contains client API views related to workers
URL prefix: /worker

Classes in this module voluntary does not expose any method to create
worker objects, it's the role of application deploymennt

"""

from flask import Blueprint

from orchester.api.views import APIListView, APIDetailDeleteView
from orchester.master.models.worker import Worker


worker = Blueprint('worker', __name__)

class WorkerViewMixin(object):
    """
    This class defines view parameters for worker API views

    """
    view_name = 'worker.wkr_detail'
    view_arg_name = 'wkr_id'
    model = Worker


class WkrIndexView(WorkerViewMixin, APIListView):
    """
    /worker/ endpoint
    GET returns the worker url list

    """
    data_list_key = 'workers'


class WkrDetailView(WorkerViewMixin, APIDetailDeleteView):
    """
    /worker/<wkr_id> endpoint
    GET returns the worker detailed info
    DELETE deletes the worker

    """
    display_fields = [
        ('id', 'cleaned_id'),
#        'app',
#        'host',
    ]


worker.add_url_rule('/', 'index', WkrIndexView.as_view('index'))
worker.add_url_rule('/<wkr_id>', 'wkr_detail', WkrDetailView.as_view('wkr_detail'))
