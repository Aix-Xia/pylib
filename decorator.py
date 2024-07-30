import time
import matplotlib.pyplot as plt
import re


# length_print_string = 50
# filled_string = '*'
#
# def timer(func):
#     def wrapper(*args, **kwargs):
#         start_time = time.time()
#         result = func(*args, **kwargs)
#         end_time = time.time()
#         print_string = f'{func.__name__} has run {end_time - start_time}s'
#         print(print_string.center(length_print_string, filled_string))
#         return result
#     return wrapper

log_file = r'.\results.log'

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f'{func.__name__} took {end_time - start_time:.2f} seconds to execute.')
        return result
    return wrapper

def memoize(func):
    cache = {}
    def wrapper(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result
    return wrapper

def log_results(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        with open(log_file, 'a') as fa:
            fa.write(f'{func.__name__} - Result: {result}\n')
        return result
    return wrapper

def suppress_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f'Error in {func.__name__}: {e}')
            return None
    return wrapper

def retry(max_attempts, delay):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f'Attempts {attempts + 1} failed. Retrying in {delay} second.')
                    attempts += 1
                    time.sleep(delay)
            raise Exception('Max retry attempts exceeded.')
        return wrapper
    return decorator


def visualize_results(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        plt.figure()
        # Your visualizatin code here
        plt.show()
        return result
    return wrapper

def debug(func):
    def wrapper(*args, **kwargs):
        print(f'Debugging {func.__name__} - args: {args}, kwargs: {kwargs}')
        return func(*args, **kwargs)
    return wrapper

# def parameter_type(*plst):
#     def decorator(func):
#         def wrapper(*args):
#             if len(args) > len(plst):
#                 raise(ValueError(f'{func.__name__} parameter list num is too more'))
#             for key, value in enumerate(args):
#                 if (type(value) != plst[key]) and (type(value).__name__ != plst[key]) and (value not in plst[key]):
#                     raise(TypeError(f'{func.__name__}\'s parameter: {value} do not meet demand'))
#             return func(*args)
#         return wrapper
#     return decorator

def parameter_type(**pkwargs):
    def decorator(func):
        def wrappper(*args, **kwargs):
            if len(pkwargs) < (len(args) + len(kwargs)):
                raise(ValueError(f'{func.__name__} parameter list num is too more'))
            plst = []
            for key, value in pkwargs.items():
                plst.append(value)
            for key, value in enumerate(args):
                if type(value) != plst[key] and type(value).__name__ != plst[key] and (value not in plst[key]):
                    raise(TypeError(f'{func.__name__}\'s parameter: {value} do not meet demand'))
            for key, value in kwargs.items():
                if type(value) != pkwargs[key] and type(value).__name__ != pkwargs[key] and (value not in pkwargs[key]):
                    raise(TypeError(f'{func.__name__}\'s parameter: {value} do not meet demand'))
            return func(*args, **kwargs)
        return wrappper
    return decorator

# def parameter_range(*plst):
#     def decorator(func):
#         def wrapper(*args):
#             if len(args) > len(plst):
#                 raise(ValueError(f'{func.__name__} parameter list num is too more'))
#             for key, value in enumerate(args):
#                 if bool(plst[key]):
#                     search = re.search('([\(\[])\s*(\d*[\.]?\d*)\s*,\s*(\d*[\.]?\d*)\s*([\)\]])', plst[key])
#                     if search == None:
#                         raise(ValueError('Decorator format is error'))
#                     if type(value) != int and type(value) != float:
#                         raise(ValueError('parameter must int or float'))
#                     r1 = search.group(1)
#                     r2 = search.group(2)
#                     r3 = search.group(3)
#                     r4 = search.group(4)
#                     if r2 != '':
#                         if r1 == '(' and value <= eval(r2):
#                             raise(ValueError(f'{value} is out of limit'))
#                         elif r1 == '[' and value < eval(r2):
#                             raise (ValueError(f'{value} is out of limit'))
#                     if r3 != '':
#                         if r4 == ')' and value >= eval(r3):
#                             raise (ValueError(f'{value} is out of limit'))
#                         elif r4 == ']' and value > eval(r3):
#                             raise (ValueError(f'{value} is out of limit'))
#             return func(*args)
#         return wrapper
#     return decorator

def __is_in_range(dvalue, drange):
    search = re.search('([\(\[])\s*(\d*[\.]?\d*)\s*,\s*(\d*[\.]?\d*)\s*([\)\]])', drange)
    if search == None:
        return 'Decorator format is error'
    if type(dvalue) != int and type(dvalue) != float:
        return 'parameter must int or float'
    r1 = search.group(1)
    r2 = search.group(2)
    r3 = search.group(3)
    r4 = search.group(4)
    if r2 != '':
        if r1 == '(' and dvalue <= eval(r2):
            return f'{dvalue} is out of limit'
        elif r1 == '[' and dvalue < eval(r2):
            return f'{dvalue} is out of limit'
    if r3 != '':
        if r4 == ')' and dvalue >= eval(r3):
            return f'{dvalue} is out of limit'
        elif r4 == ']' and dvalue > eval(r3):
            return f'{dvalue} is out of limit'
    return None
def paramter_range(**pkwargs):
    def decorator(func):
        def wrappper(*args, **kwargs):
            if len(pkwargs) < (len(args) + len(kwargs)):
                raise(ValueError(f'{func.__name__} parameter list num is too more'))
            plst = []
            for key, value in pkwargs.items():
                plst.append(value)
            for key, value in enumerate(args):
                if plst[key] == None:
                    continue
                result = __is_in_range(value, plst[key])
                if result != None:
                    raise(ValueError(result))
            for key, value in kwargs.items():
                if pkwargs[key] == None:
                    continue
                result = __is_in_range(value, pkwargs[key])
                if result != None:
                    raise (ValueError(result))
            return func(*args, **kwargs)
        return wrappper
    return decorator

def singleton(cls):
    instance = [None]
    def wrapper(*args, **kwargs):
        if instance[0] is None:
            instance[0] = cls(*args, **kwargs)
        return instance[0]
    return wrapper


if __name__ == '__main__':
    pass