"""
Misc utils views for orchester API

"""

from flask import json
from flask import abort, url_for, jsonify
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


def api_redirect(url):
    """
    This function uses the flask.redirect function and returns a 302
    response with a json body

    """
    from flask import make_response

    return make_response((jsonify({'url': url}),
                          302, {"Location": url}))


def get_field_keys(k):
    """
    This function takes either a tuple or a string as parameter and returns
    a tuple of two strings.

    The first arg of the tuple is either the string or the first arg of the
    tuple.
    The second arg is the string or the first arg if k is a string or if the
    2nd arg of k is None; else it's the string or the first arg of the tuple.

    This function is here to deal with fields list in classes below.

    """
    key = None
    obj_key = None
    if isinstance(k, tuple):
        (key, obj_key) = k
        if not obj_key:
            obj_key = key
    else:
        key = k
        obj_key = k
    return (key, obj_key)


def check_field_key(k, list):
    """
    This function check if the key is in the field list

    This function is here to deal with fields list in classes below

    """
    for cmp in list:
        (key, obj_key) = get_field_keys(cmp)
        if key == k:
            return (key, obj_key)
    return (None, None)


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
            data[self.data_list_key].append(url_for(self.view_name, _external=True,
                                                    **{self.view_arg_name: obj.id}))
        return jsonify(data)

    def post(self):
        """
        This method creates an object from the post data
        If successfull redirects to the detail handler for the newly
        created object.

        """
        from flask import request

        data = json.loads(request.data)
        kw = {}
        allowed_fields = self.required_fields + self.optional_fields
        for (k, v) in data.iteritems():
            (key, obj_key) = check_field_key(k, allowed_fields)
            if not key:
                print "invaild field %s" % k
                abort(400)
            kw[obj_key] = v
        for k in self.required_fields:
            (key, obj_key) = get_field_keys(k)
            if not obj_key in kw:
                print "missing field %s" % k
                abort(400)
        obj = self.model(**kw)
        obj.save()
        return api_redirect(url_for(self.view_name, _external=True,
                                    **{self.view_arg_name: obj.id}))


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
        if not self.model:
            abort(404)
        return self.model.objects.get_or_404(id=obj_id)

    def get_object_data(self, obj):
        """
        Returns the object data as a python dict
        This method looks for a display_fields attribute

        """
        data = {}
        for f in self.display_fields:
            (k, obj_k) = get_field_keys(f)
            v = getattr(obj, obj_k)
            if v:
                data[k] = v
        return data

    def get_object_url(self, obj):
        """
        Returns the object URL based on view_name attr

        """
        return url_for(self.view_name, _external=True, **{self.view_arg_name: obj.id})

    def get(self, **kwargs):
        """
        This method is the GET endpoint
        It returns the data from object and adds a url field

        """
        obj_id = kwargs[self.view_arg_name]
        obj = self.get_object(obj_id)
        data = self.get_object_data(obj)
        data['url'] = self.get_object_url(obj)
        return jsonify(data)

    def delete(self, **kwargs):
        """
        This method is the DELETE endpoint for the object

        """
        obj_id = kwargs[self.view_arg_name]
        obj = self.get_object(obj_id)
        obj.delete()
        return jsonify({"status": "OK"})
