from app.views.field import FieldError

class PersOAError(Exception):
    pass

class PersOAFieldError(PersOAError, FieldError):
    def __init__(self, field_name, field_keys):
        self.field = field_name
        self.keys = field_keys

class PersOARequiredFieldError(PersOAFieldError):
    def __str__(self):
        return 'This field is a required field. try passing it in one of the following keys: %s' % (
                ", ".join(self.keys)
        )

def persoa_errors(errs):
    """
    Formatter for errors in PersOAError
    """
    errors = {'fields': {}}

    for err in errs:
        if isinstance(err, PersOAFieldError):
            errors['fields'][err.field] = str(err)

    return {
        'error': errors
    }
