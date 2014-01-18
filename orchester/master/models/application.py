"""
This module contain application related models

"""

from orchester.master import db

from . import DisplayableModelMixin
from .worker import Worker


class Application(db.Document, DisplayableModelMixin):
    """
    This class represents an application

    """
    domain_name = db.StringField(unique=True)
    code_type = db.StringField()
    code_url = db.StringField()
    code_tag = db.StringField()
    min_workers = db.IntField()
    max_workers = db.IntField()
    env_vars = db.DictField()
    workers = db.ListField(db.ReferenceField(Worker))

    @property
    def private_key(self):
        """Read and returns the private key of the app"""
        return "toto"

    @property
    def public_key(self):
        """Read and returns the private key of the app"""
        return "tata"

    def gen_rsa_keypair(self):
        """
        This method generate a unique keypair for the application

        """
        pass

