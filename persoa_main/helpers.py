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
        final[field.get_name()] = valid
    return final

class Field(object):

    def __init__(self, keys, name, form=str):
        self._keys = keys
        self._name = name
        self._type = form

        # defaults
        self._default = None
        self._validate = lambda val: True

    def val(self, params):
        return self._first_valid(params)

    def get_name(self):
        return self._name

    @cascade
    def default(self, default):
        self._default = default

    @cascade
    def validator(self, func):
        self._validate = func

    def _first_valid(self, params):
        for key in self._keys:
            val = params.get(key)
            if val is None:
                continue
            try:
                val = simplejson.loads(val)
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
