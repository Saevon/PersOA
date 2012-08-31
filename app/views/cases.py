from app.views.whitelist import Whitelist
from helpers.decorators import cascade

class Case(object):
    def passed(self, params):
        raise NotImplementedError

class IncludeCase(object):

    def __init__(self, keys):
        self._keys = set(keys)

    @cascade
    def key(self, key):
        self._keys.add(key)

    def passed(self, params):
        includes = params.get(Whitelist.INCLUDE_NAME, None)
        if includes is None:
            includes = []

        for key in self._keys:
            if key not in includes:
                return False
        return True
