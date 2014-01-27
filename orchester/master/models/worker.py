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
    worker_id = db.IntField(unique_with='host')
