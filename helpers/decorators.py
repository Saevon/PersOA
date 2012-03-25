"""
Useful decorators
"""

def cascade(func):
    """
    class method decorator, always returns the
    object that called the method
    """
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        return self
    return wrapper

def allow_list(pos, name=None):
    """
    Decorator:
    Looks for the positional pos(int) or keyword name(str) argument and if
    the argument is a list calls the function once for each item

    This changes the function to always return void
    """
    def decorator(func):
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
