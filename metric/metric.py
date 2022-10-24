import functools

import numpy as np
import functools


# def metric(name: str = None):
#     def metric_decorator(func):
#         @functools.wraps(func)
#         def _wrapper(*args, **kwargs):
#             func.__name__ = func.__name__ if name is None else name
#             return func(*args, **kwargs)
#         return _wrapper
#     return metric_decorator


def metric(name: str, precision: int):
    def _wrapper(func):
        func.metric_name = name
        func.precision = precision
        return func
    return _wrapper


@metric('rpm', 0)
def rpm(x, **kwargs):
    return np.sum(x)


@metric('avg', 0)
def avg(x, **kwargs):
    return np.average(x)
