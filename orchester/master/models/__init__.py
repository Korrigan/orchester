"""
This packages contains DB models for orchester master

"""

class DisplayableModelMixin(object):
    """
    Provide a property function to return the id as string instead of
    plain ObjectId
    
    """

    @property
    def cleaned_id(self):
        """
        Returns the internal id as a string

        """
        return str(self.id)
