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


class APIModelViewMixin(object):
    """
    A simple Mixin to provide model object related methods

    """

    def get_queryset(self):
        """
        Returns the queryset for the view
        By default return all objects using self.model

        """
        return self.model.objects

    def get_object(self, obj_id):
        """Returns the model object filtering by kwargs"""
        if not self.model:
            abort(404)
        return self.model.objects.get_or_404(id=obj_id)

    def get_object_url(self, obj):
        """
        Returns the object URL based on view_name attr

        """
        return url_for(self.view_name, _external=True, **{self.view_arg_name: obj.id})

    def get_object_data(self, obj):
        """
        Returns the object data as a python dict
        This method looks for a display_fields attribute

        """
        data = {}
        for f in self.display_fields:
            (k, obj_k) = get_field_keys(f)
            v = getattr(obj, obj_k)
            if v != None:
                data[k] = v
        return data

    def get_object_kwargs(self, data):
        """
        Returns a dict for object creation based on json decoded data
        This method abort(400) if a required field is not here of if
        an unexpected field is found

        """
        kw = {}
        allowed_fields = self.required_fields + self.optional_fields
        for (k, v) in data.iteritems():
            (key, obj_key) = check_field_key(k, allowed_fields)
            if not key:
                abort(400)
            kw[obj_key] = v
        for k in self.required_fields:
            (key, obj_key) = get_field_keys(k)
            if not obj_key in kw:
                abort(400)
        return kw


class APIListView(MethodView, APIModelViewMixin):
    """
    Helper class to implement API list view
    GET will return an object with a list and a count of object

    You must subclass it and add the following attributes:
     - view_name: the name of a view to generate reverse urls
     - view_arg_name: the of the view arg for reverse urls
     - data_list_key: The key for the returned url list
     - model: The MongoEngine document to deal with

    """
    methods = ['GET',]

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


class APICreateView(MethodView, APIModelViewMixin):
    """
    Helper class to implement API create view
    POST will create an object

    You must subclass it and add the following attributes:
     - required_fields: The required fields to POST
     - optional_fields: The optional fields to POST
     - view_name: the name of a view to generate reverse urls
     - view_arg_name: the of the view arg for reverse urls
     - model: The MongoEngine document to deal with

    For *_fields, the arguments can be a string or a tuple, if a string
    or if the 2nd arg of the tupe is None, it means both the json field
    and the object attr have the same name which is either the string
    or the 1st arg of the tuple. If 2nd arg of the tuple is not None,
    it's the object attr name to use.

    """
    methods = ['POST',]

    def post(self):
        """
        This method creates an object from the post data
        If successfull redirects to the detail handler for the newly
        created object.

        """
        from flask import request

        data = json.loads(request.data)
        kw = self.get_object_kwargs(data)
        obj = self.model(**kw)
        obj.save()
        return api_redirect(url_for(self.view_name, _external=True,
                                    **{self.view_arg_name: obj.id}))


class APIListCreateView(APIListView, APICreateView):
    """
    Helper class to build API list/create endpoints
    This class combines APIListView and APICreateView

    """
    methods = ['GET', 'POST']


class APIDetailView(MethodView, APIModelViewMixin):
    """
    Helper class for implementing API detail view
    GET returns the object detailed info

    You must subclass it and add the following attributes
     - display_fields: The fields that will be returned
     - model: The MongoEngine document to use
     - view_name: the view name for reverse urls
     - view_arg_name: the name of the view argument name for reverse urls

    """
    methods = ['GET',]

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


class APIUpdateView(MethodView, APIModelViewMixin):
    """
    Helper class providing a way to update objects
    PUT will updated the object and redirect to it's url

    You must subclass it and add the following attributes
     - model: The MongoEngine document to use
     - view_name: the view name for reverse urls
     - view_arg_name: the name of the view argument name for reverse urls
     - required_fields: The required fields to PUT
     - optional_fields: The optional fields to PUT

    For *_fields, the arguments can be a string or a tuple, if a string
    or if the 2nd arg of the tupe is None, it means both the json field
    and the object attr have the same name which is either the string
    or the 1st arg of the tuple. If 2nd arg of the tuple is not None,
    it's the object attr name to use.

    """
    methods = ['PUT',]

    def put(self, **kwargs):
        """
        Like the POST handle but updates the object with given ID

        """
        from flask import request

        data = json.loads(request.data)
        kw = self.get_object_kwargs(data)
        obj_id = kwargs[self.view_arg_name]
        obj = self.get_object(obj_id)
        for (k, v) in kw.iteritems():
            setattr(obj, k, v)
        obj.save()
        return api_redirect(self.get_object_url(obj))


class APIDeleteView(MethodView, APIModelViewMixin):
    """
    Helper class providing a way to delete objects
    DELETE will delete the object

    You must subclass it and add the following attributes
     - model: The MongoEngine document to use
     - view_name: the view name for reverse urls
     - view_arg_name: the name of the view argument name for reverse urls

    """
    method = ['DELETE',]

    def delete(self, **kwargs):
        """
        This method is the DELETE endpoint for the object

        """
        obj_id = kwargs[self.view_arg_name]
        obj = self.get_object(obj_id)
        obj.delete()
        return jsonify({"status": "OK"})


class APIDetailUpdateView(APIDetailView, APIUpdateView):
    """
    Helper class providing both GET and PUT methods for model related API
    Combines APIDetailView and APIUpdateView classes

    """
    methods = ['GET', 'PUT']


class APIDetailDeleteView(APIDetailView, APIDeleteView):
    """
    Helper class providing both GET and DELETE methods for model related APIs
    Combines APIDetailView and APIDeleteView classes

    """
    methods = ['GET', 'DELETE']


class APIUpdateDeleteView(APIUpdateView, APIDeleteView):
    """
    Helper class providing both PUT and DELETE methods for model related APIs
    Combines APIDeleteView and APIUpdateView classes

    """
    methods = ['DELETE', 'PUT']


class APIDetailUpdateDeleteView(APIDetailView, APIUpdateView, APIDeleteView):
    """
    Helper class providing all model related endpoints:
    GET shows the object detailed info
    PUT updates the object
    DELETE deletes the object

    Combines APIDetailView, APIUpdateView, and APIDeleteView classes

    """
    methods = ['GET', 'PUT', 'DELETE']
