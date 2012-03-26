import simplejson

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

class IncludeField(Field):
    """
    A field for includes
    """

    NAME= 'include'
    KEYS = ['include']

    def __init__(self, choices):
        Field.__init__(self, Field.KEYS, Field.NAME, list)
        self._limit = set(choices)
        self._validate = IncludeField.validate

    @classmethod
    def validate(val):
        # TODO: if one include fails they all fail?
        # I need to fix that
        def allowed(val):
            return (
                isinstance(val, basestring)
                and val in self._limit
            )
        return (
            isinstance(val, list)
            and filter(allowed, val)
        )

    @cascade
    def include(choice):
        self._limit.add(choice)

def field(name, keys=None, form=str, default=None, validator=None):
    # This is already a Field
    if isinstance(name, Field):
        return name

    new = Field(**{
        'keys': keys,
        'name': name,
        'form':  form,
    }).default(default)
    if validator is not None:
        new.validator(validator)

    return new
