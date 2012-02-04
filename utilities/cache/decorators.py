import os
import settings
from types import FunctionType
from functools import wraps

from django.core.cache import cache
from utilities.cache.dogpile import cache_get, cache_set

CURRENT_VERSION = getattr(settings, '', '')

def cacheable(key=None, ttl=60, is_enabled=True):
    """
    Decorator for cacheable function
    """
    def decorator(fxn):
        def arg2str(arg):
            if type(arg) == FunctionType:
                return arg.__name__
            else:
                return str(arg)

        if callable(key):
            key_fun = key
        else:
            if key is None:
                key_fun = lambda *args, **kwargs: '%s-%s-%s-%s' % \
                    (fxn.__module__, fxn.__name__, '-'.join(map(arg2str, args)),
                     '-'.join(["%s-%s" % (k, v) for k,v in kwargs.iteritems()]))
            else:
                key_fun = lambda *args, **kwargs: key % args[:key.count('%')]
        
        @wraps(fxn)
        def wrapper(*args, **kwargs):
            #TODO: print fxn.func_code.co_varnames[:fxn.func_code.co_argcount]
            if is_enabled:
                key = key_fun(*args, **kwargs)
                versioned_key = "%s-%s" % (CURRENT_VERSION, key)
                data = cache_get(cache, versioned_key)

                if data is None:
                    data = fxn(*args, **kwargs)
                    cache_set(cache, versioned_key, data, ttl)
                return data
            else:
                return fxn(*args, **kwargs)

        return wrapper
    return decorator 
