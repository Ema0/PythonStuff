# monkeypatching built-in types is a mess: the following is a way to do it.
# it could be not safe at all!
# (found this from Armin R. on Twitter, what a beautiful gem ;))
# read further for other methods

import ctypes
from types import DictProxyType, MethodType

# figure out side of _Py_ssize_t
if hasattr(ctypes.pythonapi, 'Py_InitModule4_64'):
    _Py_ssize_t = ctypes.c_int64
else:
    _Py_ssize_t = ctypes.c_int

# regular python
class _PyObject(ctypes.Structure):
    pass
_PyObject._fields_ = [
    ('ob_refcnt', _Py_ssize_t),
    ('ob_type', ctypes.POINTER(_PyObject))
]

# python with trace
if object.__basicsize__ != ctypes.sizeof(_PyObject):
    class _PyObject(ctypes.Structure):
        pass
    _PyObject._fields_ = [
        ('_ob_next', ctypes.POINTER(_PyObject)),
        ('_ob_prev', ctypes.POINTER(_PyObject)),
        ('ob_refcnt', _Py_ssize_t),
        ('ob_type', ctypes.POINTER(_PyObject))
    ]


class _DictProxy(_PyObject):
    _fields_ = [('dict', ctypes.POINTER(_PyObject))]


def reveal_dict(proxy):
    if not isinstance(proxy, DictProxyType):
        raise TypeError('dictproxy expected')
    dp = _DictProxy.from_address(id(proxy))
    ns = {}
    ctypes.pythonapi.PyDict_SetItem(ctypes.py_object(ns),
                                    ctypes.py_object(None),
                                    dp.dict)
    return ns[None]


def get_class_dict(cls):
    d = getattr(cls, '__dict__', None)
    if d is None:
        raise TypeError('given class does not have a dictionary')
    if isinstance(d, DictProxyType):
        return reveal_dict(d)
    return d


d = get_class_dict(int)
d['minutes'] = lambda x: x*60


class Test:
    def __init__(self):
        print('class created')

    def test(self):
        print('test')

# (safer??) alternative: use the forbiddenfruit library

#   from forbiddenfruit import curse

#   def new_method(self)
#       print('new method')

#   curse(int, 'new_method', new_method) 

# extend python classes like this

#   def new_method(self):
#       print('new method')

#   Class_to_extend.new_method = new_method