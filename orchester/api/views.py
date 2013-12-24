"""
Misc utils views for orchester API

"""

from flask import jsonify
from flask.views import MethodView

from orchester.api import api_version


def index(service, version, capabilities=[], api_version=api_version):
    """
    This is the API root endpoint for orchester services
    This helper function provide a standardized JSON rendering

    """
    data = {
        'service': service,
        'capabilities':  capabilities,
        'version': version,
        'api_version': api_version,
    }
    return jsonify(data)


class APIListCreateView(MethodView):
    """
    Helper class to implement API list/create view
    GET will return an object with a list and a count of object
    POST will create an object

    You must subclass it and add the following attributes:
     - required_fields: The required fields to POST
     - optional_fields: The optional fields to POST
     - view_name: the name of a view to generate reverse urls
     - view_arg_name: the of the view arg for reverse urls
     - data_list_key: The key for the returned url list
     - model: The MongoEngine document to deal with

    For *_fields, the arguments can be a string or a tuple, if a string
    or if the 2nd arg of the tupe is None, it means both the json field
    and the object attr have the same name which is either the string
    or the 1st arg of the tuple. If 2nd arg of the tuple is not None,
    it's the object attr name to use.

    """
    methods = ['GET', 'POST']
    data_list_key = 'list'
    required_fields = []
    optional_fields = []

    def get_queryset(self):
        """
        Returns the queryset for the view
        By default return all objects using self.model

        """
        return self.model.objects

    def get(self):
        """Returns the application list and count"""
        qs = self.get_queryset()
        data = {
            self.data_list_key: [],
            'count': qs.count()
        }
        for obj in qs:
            data[self.data_list_key].append(url_for(self.view_name,
                                                    **{self.view_arg_name: obj._id}))
        return jsonify(data)


class APIDetailView(MethodView):
    """
    Helper class for implementing API detail view
    You must subclass it and add the following attributes
     - display_fields: The fields that will be returned
     - required_fields: The required fields to PUT
     - optional_fields: The optional fields to PUT
     - model: The MongoEngine document to use
     - view_name: the view name for reverse urls
     - view_arg_name: the name of the view argument name for reverse urls

    For *_fields, the arguments can be a string or a tuple, if a string
    or if the 2nd arg of the tupe is None, it means both the json field
    and the object attr have the same name which is either the string
    or the 1st arg of the tuple. If 2nd arg of the tuple is not None,
    it's the object attr name to use.

    """
    methods = ['GET', 'PUT', 'DELETE']
    display_fields = []
    required_fields = []
    optional_fields = []

    def get_object(self, obj_id):
        """Returns the model object filtering by kwargs"""
        if not model:
            abort(404)
        return self.model.objects.get_or_404(_id=obj_id)

    def get_object_data(self, obj):
        """
        Returns the object data as a python dict
        This method looks for a display_fields attribute

        """
        def _get_keys(k):
            """Returns the correct keys for object and data"""
            if isinstance(f, tuple):
                (key, obj_key) = f
                if not obj_key:
                    obj_key = key
            else:
                key = f
                obj_key = f
            return (key, objkey)

        data = {}
        for f in self.display_fields:
            (k, obj_k) = _get_keys(f)
            data[k] = getattr(obj, obj_k)
        return data

    def get_object_url(self, obj):
        """
        Returns the object URL based on view_name attr

        """
        from flask import url_for
        return url_for(self.view_name, **{self.view_arg_name: obj._id})

    def get(self, obj_id):
        """
        This method is the GET endpoint
        It returns the data from object and adds a url field

        """
        obj = self.get_object(obj_id)
        data = self.get_object_data(obj)
        data['url'] = self.get_object_url(obj)
        return jsonify(data)

    def delete(self, obj_id):
        """
        This method is the DELETE endpoint for the object

        """
        obj = self.get_object(obj_id)
        obj.delete()
