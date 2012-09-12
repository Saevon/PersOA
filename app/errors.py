from app.views.field import FieldError

class PersOAError(Exception):
    ERR_CODE = 9000

class PersOAWarning(PersOAError, Warning):
    ERR_CODE = 9900

class PersOALeftoverField(PersOAWarning):
    ERR_CODE = 9901
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return 'This argument was passed in but not used: %s' % (
            self.name
        )

class PersOAEarlyFinish(PersOAError):
    pass

class PersOANotFound(PersOAError):
    ERR_CODE = 9001
    def __str__(self):
        return 'The item was not found.'

class PersOAFieldError(PersOAError, FieldError):
    ERR_CODE = 9010
    def __init__(self, field_name, field_keys):
        self.field = field_name
        self.keys = field_keys

class PersOARequiredFieldError(PersOAFieldError):
    ERR_CODE = 9011
    def __str__(self):
        return 'This field is a required field. try passing it in one of the following keys: %s' % (
                ", ".join(self.keys)
        )
