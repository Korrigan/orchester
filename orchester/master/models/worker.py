"""
This module handles worker related models

"""

from orchester.master import db

from . import DisplayableModelMixin
from .node import Node
from .application import Application


class Worker(db.Document, DisplayableModelMixin):
    """
    The sole use case of this class (in mongo-related terms) is to be used in
    Application object.
    This class provides helper function about how to deal with workers

    """
    host = db.ReferenceField(Node)
    app = db.ReferenceField(Application)
    worker_id = db.StringField(unique_with='host')

    def delete(self, *args, **kwargs):
        """
        Tell his node to delete the worker and then call the standard
        method to delete reference in BDD

        """
        self.host.stop_worker(self)
        return super(Worker, self).delete(*args, **kwargs)

    @classmethod
    def bulk_delete(kls, *args, **kwargs):
        """
        Deletes all workers which match *args and **kwargs filters

        """
        for w in kls.objects.filter(*args, **kwargs):
            w.delete()
