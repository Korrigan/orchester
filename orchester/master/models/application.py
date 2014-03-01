"""
This module contain application related models

"""

from orchester.master import db

from . import DisplayableModelMixin


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

    @property
    def private_key(self):
        """Read and returns the private key of the app"""
        return "toto"

    @property
    def public_key(self):
        """Read and returns the private key of the app"""
        return "tata"

    def delete(self, *args, **kwargs):
        """
        Deletes the application and all related services

        """
        from .worker import Worker

        Worker.bulk_delete(app=self)
        return super(Application, self).delete(*args, **kwargs)

    def gen_rsa_keypair(self):
        """
        This method generate a unique keypair for the application

        """
        pass

