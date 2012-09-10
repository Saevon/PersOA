from app.views.field import Field, FieldError
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
        self.clear()

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

    @cascade
    def error(self, err):
        """
        Adds a new error to its list
        """
        self._errors.append(err)

    def errors(self):
        """
        Returns the list of errors that occured
        """
        return self._errors

    @cascade
    def leftover(self, Err):
        """
        Adds any unused params to errors if type Err
        """
        for key in self._left:
            self.error(Err(key))

    @cascade
    def clear(self):
        """
        clears any errors that may have occured
        """
        self._errors = []
        self._left = []

    def process(self, params):
        """
        Reads params(dict) and returns a whitelisted dict.
        """
        self._final = {
            Whitelist.INCLUDE_NAME: self._include_names.copy()
        }
        self._fields = set(self._whitelist.keys())
        self._fields.remove(Whitelist.INCLUDE_NAME)

        # Get the list of all keys, to subtract those that get used
        self._left = params.keys()

        # Find what is included
        try:
            includes = self._whitelist[Whitelist.INCLUDE_NAME].val(params)
            self._left.remove(self._whitelist[Whitelist.INCLUDE_NAME].used_key())
        except FieldError:
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
                if not field.used_key() is None:
                    self._left.remove(field.used_key())
            except FieldError, err:
                self.error(err)
