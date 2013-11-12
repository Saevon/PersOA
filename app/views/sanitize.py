from django.http import HttpResponse

from app.errors import PersOAFieldError, PersOAWarning, PersOAEarlyFinish
from functools import wraps
from utils.decorators import allow_list, cascade

import simplejson

def json_return(func):
    """
    Wraps the returned object in a HttpResponse after a json dump,
    returning that instead
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = func(*args, **kwargs)

        response = HttpResponse(mimetype='application/json')
        simplejson.dump(data, response)
        return response
    return wrapper

class PersOAOutput(object):

    def __init__(self):
        self._out = {
            'errors': {
                'num': 0,
                'field': {},
                'misc': [],
                'warn': [],
            },
            'output': None,
        }

    @cascade
    def error(self, errors):
        """
        Adds a new error to show to the user
        """
        self.problem = False

        if isinstance(errors, list):
            for err in errors:
                self.__error(err)
        else:
            self.__error(errors)

        if self.problem:
            raise PersOAEarlyFinish

    def __error(self, err):
        if isinstance(err, PersOAFieldError):
            self._out['errors']['num'] += 1
            self._out['errors']['field'][err.field] = self.__sanitize_error(err)
            self.problem = True
        elif isinstance(err, PersOAWarning):
            self._out['errors']['warn'].append(self.__sanitize_error(err))
        else:
            self._out['errors']['misc'].append(self.__sanitize_error(err))
            self._out['errors']['num'] += 1
            self.problem = True

    def __sanitize_error(self, err):
        return {
            'message': unicode(err),
            'code': err.ERR_CODE,
        }

    @cascade
    def output(self, out):
        """
        Sets the output to show the user
        """
        self._out['output'] = out

    def sanitize(self):
        """
        Returns the proper data object to output
        """
        return self._out

def persoa_output(func):
    """
    Passes in a new PersOAOutput to the function every call and catches any problem with the input
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        out = PersOAOutput()
        kwargs['output'] = out
        try:
            func(*args, **kwargs)
        except PersOAEarlyFinish:
            pass
        return out.sanitize()
    return wrapper

