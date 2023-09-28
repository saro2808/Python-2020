from functools import wraps
import time


def profiler(f):
    start_time = time.time()

    @wraps(f)
    def internal(*args, **kwargs):
        nonlocal start_time
        if internal.depth == 0:
            internal.calls = 0
        internal.depth += 1
        result = f(*args, **kwargs)
        internal.calls += 1
        internal.depth -= 1
        internal.last_time_taken = time.time() - start_time
        return result
    internal.depth = 0
    return internal
