"""
Useful decorators
"""
from django.http import HttpResponse

from functools import wraps
from utils.seed import Seed
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

def cascade(func):
    """
    class method decorator, always returns the
    object that called the method
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        return self
    return wrapper

def seeded(pos):
    """
    Decorator:
    Looks for the positional pos(int) or keyword name(str) argument and if
    the argument is a list calls the function once for each item

    This changes the function to always return void
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            valid = lambda val: (
                Seed(val) if isinstance(val, int) and not val is None
                else Seed()
            )
            if len(args) > pos:
                args = list(args)
                args[pos] = valid(args[pos])
            elif kwargs.has_key('seed'):
                kwargs['seed'] = valid(kwargs['seed'])
            else:
                kwargs['seed'] = Seed()
            return func(*args, **kwargs)
        return wrapper
    return decorator

def allow_list(pos, name=None):
    """
    Decorator:
    Looks for the positional pos(int) or keyword name(str) argument and if
    the argument is a list calls the function once for each item

    This changes the function to always return void
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if len(args) > pos:
                # args is normally an immutable tuple
                args = list(args)
                source = args
                key = pos
            elif name is not None and kwargs.has_key(name):
                source = kwargs
                key = name
            else:
                # The argument wasn't passed in .: original call
                func(*args, **kwargs)
                return

            # Make sure we'll loop through a list of one index
            if not isinstance(source[key], list):
                source[key] = [source[key]]
            for item in source[key]:
                source[key] = item
                func(*args, **kwargs)
        return wrapper
    return decorator
