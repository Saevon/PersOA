from app.views.whitelist import Whitelist
from utils.decorators import cascade

class Case(object):
    """
    A check that ensures that the given Whitelist has a given property
    """

    INCLUDE_NAME = Whitelist.INCLUDE_NAME

    def passed(self, params):
        """
        A boolean check that checks if params has the expected property
        """
        raise NotImplementedError

class IncludeCase(object):
    """
    A Case that ensures that the every prerequisite INCLUDES have been supplies
        Use IncludeCase.key('field') to add expected fields
    """

    def __init__(self, keys):
        self._keys = set(keys)

    @cascade
    def key(self, key):
        """
        Adds a new fields to check for, always makes sure ALL the fields have been included
        """
        self._keys.add(key)

    def passed(self, params):
        """
        A boolean check that checks if params has the expected include fields enabled
        """
        includes = params.get(Case.INCLUDE_NAME, None)
        if includes is None:
            includes = []

        for key in self._keys:
            if key not in includes:
                return False
        return True
