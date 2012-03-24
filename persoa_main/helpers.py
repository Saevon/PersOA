import simplejson

def extract(params, whitelist):
    """
    Takes a json encoded string of arguments and extracts all expected
    arguments

    Whitelist:
        [(str)param names, (str)name, (str)type, (type)default]
    """
    final = {}

    for field in whitelist:
        valid = field.val(params)
    return final

def cascade(func):
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        return self
    return wrapper

class Field(object):

    def __init__(self, keys, name, form=str):
        self._keys = keys
        self._name = name
        self._type = form

        # defaults
        self._default = None
        self._validator = lambda val: True

    def val(self, params):
        return self._first_valid(params)

    @cascade
    def default(self, default):
        self._default = default

    @cascade
    def validator(self, func):
        self._validate = func

    def _first_valid(self, params):
        for key in self._keys:
            try:
                val = simplejson.loads(
                    params.get(key)
                )
            except simplejson.JSONDecodeError:
                continue
            # Make sure that only a valid type is returned"""
            if (val is not None and self._check_type(val)
            and self._validate(val)):
                return val
        return self._default

    def _check_type(self, val):
        return isinstance(val, self._type)

def field(keys, name, form=str, default=None, validator=None):
    new = Field(**{
        'keys': keys,
        'name': name,
        'form':  form,
    }).default(default)
    if validator is not None:
        new.validator(validator)

    return new