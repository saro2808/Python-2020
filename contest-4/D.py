# thanks to https://stackoverflow.com/questions/10220599/how-to-hash-args-kwargs-for-function-cache
# and https://github.com/python/cpython/blob/main/Lib/functools.py#L449

from functools import wraps


def cache(N):
    def decorator(f):
        queue = {}
        filled = 0

        @wraps(f)
        def internal(*args, **kwargs):
            nonlocal queue, filled
            sentinel = object()
            hashed_key = hash(args + (sentinel,) +
                              tuple(sorted(kwargs.items())))
            value = queue.get(hashed_key, sentinel)
            if value is not sentinel:
                return value
            value = f(*args, **kwargs)
            queue[hashed_key] = value
            if filled == N:
                del queue[next(iter(queue))]
            else:
                filled += 1
            return value
        return internal
    return decorator

# (time limit exceeded)
