from collections import defaultdict
from helpers.decorators import allow_list, cascade

class Whitelist(object):

    INCLUDE = 'include'

    def __init__(self):
        self._whitelist = {Whitelist.INCLUDE: IncludeField([])}
        self._required = set()
        self._optional = defaultdict(list)
        self._errors = []

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
        self._includes.discard(key)
        self._required.discard(key)
        self._optional.discard(key)

    @cascade
    @allow_list(1, 'field')
    def require(self, field):
        """
        Whitelist a list of fields labeling them as required
        """
        self.add(field)
        self._required.add(field.get_name())

    @cascade
    def add_if(self, case, field):
        """
        Adds a field that is whitelisted if another field fills a condition
        """
        self.add(field)
        self._optional[field.get_name()] = case

    @cascade
    @allow_list(1, 'choice')
    def include(self, choice):
        self._whitelist[Whitelist.INCLUDE].include(choice)

    @cascade
    def process(self, params):
        """
        Reads params(dict) and returns a whitelisted dict.
        """
        self._final = {}
        self._fields = set(self._whitelist.keys())

        # First add Includes
        self._process(params, [self._whitelist[Whitelist.INCLUDE]])

    def _process(self, params, field_names):
        for name in field_names:
            # Check the field off
            self._fields.remove(name)

            # Check for any pre-conditions
            for case in self._optional[name]:
                error = case.check(self._final):
                if error is not None:
                    # process error
                    # Keep only the first error per field
                    break

            # Get the data
            valid = self._whitelist[name].val(params)
            self._final[field.get_name()] = valid

            # Check for any post-conditions

    def _error(self, field_name, message):
        pass

    def errors(self):
        pass
