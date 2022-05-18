import time
import os


def time_func(func):
    """
    Calculate the time of execution of a function
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, 'took ' + str(round((end - start), 3)) + ' seconds')
        return result

    return wrapper


def change_name_file(func):
    """
    Change the name of the 'model_copy.json' to the 'model.json' file
    """
    def wrapper_change_name_file(arg1, arg2):
        os.rename(arg1, arg2)
        func(arg1, arg2)

    return wrapper_change_name_file



