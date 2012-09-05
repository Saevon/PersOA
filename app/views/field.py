import simplejson
from utils.decorators import allow_list, cascade

class Field(object):
    """
    An input Field which can read a dict and transform the
    data in it into a proper form for this field
    """

    __type_checkers = dict()

    # Special settings for a field
    # If you combine both then all items in the list must be part of the choices
    SETTINGS_LIST = 'list'
    SETTINGS_LIMIT = 'limit'

    def __init__(self, keys, name, cls=basestring):
        """
        keys -- A list of input keys that are read
        name -- A str representing the name of this field
        cls  -- (OPTIONAL) The type of input that is expected
        """
        self._keys = set(keys)
        self._name = name

        self._settings = set()

        # defaults
        self._default = KeyError()
        self._validators = []
        self._type = cls

    @staticmethod
    def type_checker(cls):
        """
        Returns a comparison function
        """
        cache_key = cls
        if not Field.__type_checkers.has_key(cache_key):
            Field.__type_checkers[cache_key] = lambda val: isinstance(val, cls)
        return Field.__type_checkers[cache_key]

    @cascade
    @allow_list(1, 'setting')
    def setting(self, setting):
        """
        Enables a Field setting. Passing in a setting twice resets any arguments it stores
        """
        self._settings.add(setting)
        if setting == Field.SETTINGS_LIMIT:
            self._limit = set()
            self.validator(lambda val: (val in self._limit))

    @cascade
    @allow_list(1, 'choice')
    def choice(self, choice):
        """
        If the LIMIT setting is disabled enables it
        Then adds choice to the possible choices for this field
        """
        if not Field.SETTINGS_LIMIT in self._settings:
            self.setting(Field.SETTINGS_LIMIT)
        self._limit.add(choice)

    @cascade
    def default(self, default):
        """
        Sets the default that is returned if this field can't find a value
        If the default is a subclass of Exception, the default is raised instead
        make sure you pass in an instance of the exception, not the class
        """
        self._default = default

    @cascade
    @allow_list(1, 'key')
    def key(self, key):
        """
        Adds a new input field to read from
        """
        self._keys.add(key)

    @cascade
    @allow_list(1, 'func')
    def validator(self, func):
        """
        Adds a new validation function which requires the form:
            (val) -> bool
        """
        self._validators.append(func)

    def get_name(self):
        """
        Returns the name of the field
        """
        return self._name

    def val(self, params):
        """
        Calculates the value of the field from the dict params
        Returning the calculated value
        """
        return self._first_valid(params)

    def _first_valid(self, params):
        """
        Tries to find the first valid field in params that fits the set criteria.
        returns/raises the default value if none was found
        """
        for key in self._keys:
            val = params.get(key)
            if val is None:
                continue
            try:
                val = simplejson.loads(val)
            except simplejson.JSONDecodeError:
                continue

            # Make sure that only a valid type is returned
            if Field.SETTINGS_LIST in self._settings:
                # Check every single value for validity
                valid = True
                for index in range(len(val)):
                    value = val[index]
                    if not Field.type_checker(self._type)(value):
                        try:
                            val[index] = self._type(value)
                        except TypeError:
                            valid = False
                            break
                    valid = self._validate_val(value) and valid
                    # optimize by breaking out at first False
                    if not valid:
                        break
                if valid:
                    return val
            else:
                valid = True
                if not Field.type_checker(self._type)(val):
                    try:
                        val = self._type(val)
                    except TypeError:
                        valid = False
                if valid and self._validate_val(val):
                    return val

        # Since nothing was found the default applies
        if isinstance(self._default, BaseException):
            raise self._default
        return self._default

    def _validate_val(self, val):
        """
        Runs all the validators on the val
        Returns a bool success value
        """
        for validator in self._validators:
            if not validator(val):
                return False
        return True
