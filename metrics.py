import time


def runtime_eval(func, args):
    start = time.time()
    result = func(*args)
    end = time.time()
    return result, end - start
