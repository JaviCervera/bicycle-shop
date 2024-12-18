from functools import wraps
import logging

def log(func):
    """
    This decorator logs the arguments for a method call,
    and then the result of calling the method.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        func_name = f'{self.__class__.__name__}.{func.__name__}'
        logging.debug(f'{func_name} arguments: {args} {kwargs}')
        result = func(self, *args, **kwargs)
        logging.debug(f'{func_name} return: {result}')
        return result
    return wrapper
