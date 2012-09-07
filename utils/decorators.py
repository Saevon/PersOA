"""
Useful decorators
"""
from functools import wraps

from utils.seed import Seed

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
            if not (len(args) > pos or kwargs.has_key('seed')):
                kwargs['seed'] = Seed();
            else:
                if len(args) > pos:
                    args[pos] = Seed(args[pos])
                else:
                    kwargs['seed'] = Seed(kwarg['seed'])
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
