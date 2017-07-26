import sys
import collections
import functools

def exit_with_error(func):
    '''Decorator for error messages'''
    def hidden_func(*args, **kwargs):
        func(*args, **kwargs)
        exit()
    return hidden_func

class memoized(object):
    '''Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
 {4}(not reevaluated).
    '''
    def __init__(self, func):
        self.func = func
        self.cache = {}
    def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value
    def __repr__(self):
        '''Return the function's docstring.'''
        return self.func.__doc__
    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj)

@memoized
def fibonacci(n):
    'Return the nth fibonacci number.'
    if n in (0, 1):
        return n
    return fibonacci(n-1) + fibonacci(n-2)

@exit_with_error
def err_wrong_param(param):
    'Print an error message if the parameter is not an int and exits'
    print '"{}" is not a valid positive number: exiting.'.format(param)

@exit_with_error
def err_no_param():   
    'Print an error message there has not been passed any parameter and exits'
    print 'No input provided'

@exit_with_error
def err_runtime_number_too_high(param):
    print '{} is too large. Insert a value between 0 and 165'.format(param)

def checkvalue(value):
    value = int(value)
    if value < 0:
        raise
    return value

if __name__=='__main__':
    try: nth = sys.argv[1]
    except IndexError: err_no_param()
    try: nth = checkvalue(nth)
    except: err_wrong_param(nth)
    try: print fibonacci(nth)
    except RuntimeError: err_runtime_number_too_high(nth)