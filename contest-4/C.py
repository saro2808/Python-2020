import sys
from functools import wraps


def takes(*types):
    def san_decor(func):
        @wraps(func)
        def wrapper(*args):
            Len = min(len(types), len(args))
            for i in range(Len):
                if not isinstance(args[i], types[i]):
                    raise TypeError
            return func(*args)
        return wrapper
    return san_decor

exec(sys.stdin.read())
