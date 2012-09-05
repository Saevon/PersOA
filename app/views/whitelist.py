from app.views.field import Field
from collections import defaultdict
from utils.decorators import allow_list, cascade

class Whitelist(object):

    INCLUDE_NAME = 'include'
    INCLUDE_KEYS = ['include']

    def __init__(self):
        """
        Creates an empty Whitelist
        """
        self._whitelist = {
            Whitelist.INCLUDE_NAME: (Field(Whitelist.INCLUDE_KEYS, Whitelist.INCLUDE_NAME, basestring)
                .setting(Field.SETTINGS_LIST)
            ),
        }
        self._includes = {}
        self._include_names = {}

    @cascade
    @allow_list(1, 'field')
    def add(self, field):
        """
        Adds a list of fields to the whitelist
        Used to add constant field groups
        """
        key = field.get_name()
        if key in self._whitelist:
            raise KeyError
        self._whitelist[key] = field

    @cascade
    @allow_list(1, 'field')
    def remove(self, field):
        """
        Removes a field from the whitelist
        Useful if you add groups of fields
        """
        key = field.get_name()

        # Could raise a KeyEror
        self._whitelist.pop(key)
        self._includes.pop(key)
        self._include_names.pop(key)

    @cascade
    def include(self, keys, name):
        """
        Adds a new include choice
        """
        self._whitelist[Whitelist.INCLUDE_NAME].choice(keys)

        self._include_names[name] = False
        for key in keys:
            if self._includes.has_key(key):
                self._includes[key].append(name)
            else:
                self._includes[key] = [name]

    def process(self, params):
        """
        Reads params(dict) and returns a whitelisted dict.
        """
        self._final = {
            Whitelist.INCLUDE_NAME: self._include_names.copy()
        }
        self._fields = set(self._whitelist.keys())
        self._fields.remove(Whitelist.INCLUDE_NAME)

        # Find what is included
        try:
            includes = self._whitelist[Whitelist.INCLUDE_NAME].val(params)
        except KeyError:
            self._final.pop(Whitelist.INCLUDE_NAME)
            includes = False

        # TODO: Really... the best I can think of is a staircase?
        if includes:
            for key in includes:
                if self._includes.has_key(key):
                    for name in self._includes[key]:
                        self._final[Whitelist.INCLUDE_NAME][name] = True

        # Get the other fields
        self._process(params, list(self._fields))

        return self._final

    def _process(self, params, field_names):
        for name in field_names:
            # Check the field off
            self._fields.remove(name)

            field = self._whitelist[name]
            # Get the data
            try:
                valid = self._whitelist[name].val(params)
                self._final[field.get_name()] = valid
            except KeyError:
                pass
