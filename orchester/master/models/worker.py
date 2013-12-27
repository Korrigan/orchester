"""
This module handles worker related models

"""

from orchester.master import db

from .node import Node


class Worker(db.EmbeddedDocument):
    """
    The sole use case of this class (in mongo-related terms) is to be used in
    Application object.
    This class provides helper function about how to deal with workers

    """
    host = db.ReferenceField(Node)
    worker_id = db.IntField(unique_with='host')
