"""
This module contain application related models

"""

from orchester.master import db

from .worker import Worker


class Application(db.Document):
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
    workers = db.ListField(db.ReferenceField('Worker'))

    @property
    def cleaned_id(self):
        """
        Returns the internal id as a string

        TODO: this should be in a mixin

        """
        return str(self.id)

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
