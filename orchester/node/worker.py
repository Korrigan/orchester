class Worker(object):
    """
    Worker class invoked by node to manage each and every plugin instantiation

    """
    def __init__(self, plugin):
        self.id = self.generate_id()
        self.plugin = plugin

    @staticmethod
    def generate_id():
        """
        Static helper method to generate an unique and pretty id.

        """
        from uuid import uuid4
        return unicode(uuid4())
