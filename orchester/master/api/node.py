"""
Contains API views related to node
URL prefix: /node

"""

from flask import Blueprint
from flask import url_for

from orchester.api.views import APIDetailUpdateDeleteView, APIListCreateView

from orchester.master.models.node import Node
from orchester.master.models.worker import Worker

node = Blueprint('node', __name__)


class NodeViewMixin(object):
    """
    This mixin class contains view parameters for node view classes

    """
    view_name = '.node_detail'
    view_arg_name = 'node_id'
    model = Node
    required_fields = [
        'host',
    ]
    optional_fields = []


class NodeIndexView(NodeViewMixin, APIListCreateView):
    """
    /node/ endpoint
    GET list the nodes
    POST create a new node

    """
    data_list_key = 'nodes'


class NodeView(APIDetailUpdateDeleteView, NodeViewMixin):
    """
    /node/<node_id>/ endpoint
    GET returns detailed node info
    PUT update the node
    DELETE delete the node

    """
    display_fields = [
        ('id', 'cleaned_id'),
        'host',
    ]

    def get_object_data(self, obj):
        """
        This method overrides get_object_data to add a worker list

        """
        data = super(NodeView, self).get_object_data(obj)
        data['workers'] = []
        for w in Worker.objects.filter(host=obj):
            data['workers'].append(url_for('worker.wkr_detail', _external=True,
                                           id=w.cleaned_id))
        return data


node.add_url_rule('/', 'index', NodeIndexView.as_view('index'))
node.add_url_rule('/<node_id>', 'node_detail', NodeView.as_view('node_detail'))
