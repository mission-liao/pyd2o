import six
import json


class BaseObj(object):
    """
    """
    __fields__ = {}

    def __init__(self, val):
        """ only cache the data, all preparation would be done after accessing them
        """
        self._data = val # for properties
        self._c = {} # for children

class ArrayBase(object):
    """ container type: array of json
    """
    def __init__(self, val):
        self._c = []
        for v in val:
            self._c.append(self.__child_class__(v))

    def __getitem__(self, key):
        return self._c[key]

class MapBase(object):
    """ container type: map of json
    """
    def __init__(self, val):
        self._c = {}
        for k in six.iterkeys(val):
            self._c[k] = self.__child_class__(val[k])

    def __getitem__(self, key):
        return self._c[key]

    def __iter__(self):
        return self._c.iterkeys()

def is_array(child):
    """ class factory for ArrayBase
    """
    return type(
        'array_of_' + child.__name__,
        (ArrayBase,),
        dict(
            __child_class__=child,
        )
    )

def is_map(child):
    """ class factory for MapBase
    """
    return type(
        'map_of_' + child.__name__,
        (MapBase,),
        dict(
            __child_class__=child
        )
    )
    

def _property_factory_(name):
    def _getter_(self):
        if name in self._data:
            return self._data[name]
        else:
            opt = self.__fields__[name]
            if opt.get('required', False):
                raise Exception('property not found: {} in {}'.format(name, self.__class__.__name__))
            return opt.get('default', None)

        return self._data[name] if name in self._data else self.__fields__[name]['default']
    return _getter_

def _child_factory_(name):
    def _getter_(self):
        if name in self._c:
            return self._c[name]
        else:
            # lazy initialize of children
            if name in self._data:
                c = self.__children__[name]['child'](self._data[name])
                self._c[name] = c
                return c
            else:
                if self.__children__[name].get('required', False):
                    raise Exception('child not found: {} in {}'.format(name, self.__class__.__name__))
    return _getter_
    

class FieldMeta(type):
    """ meta class to create field
    """
    def __new__(metacls, name, bases, spec):
        """
        """
        # default value of field-declaration is {}
        spec['__fields__'] = spec['__fields__'] if '__fields__' in spec else {}
        spec['__children__'] = spec['__children__'] if '__children__' in spec else {}

        # inheritant field declaration from parent class
        for b in bases:
            if hasattr(b, '__fields__'):
                d = {}
                for k in set(b.__fields__.keys()) - set(spec['__fields__'].keys()):
                    d[k] = b.__fields__[k]
            if hasattr(b, '__children__'):
                d = {}
                for k in set(b.__children__.keys()) - set(spec['__children__'].keys()):
                    d[k] = b.__children__[k]

        # init properties based on field-declaration
        for n in six.iterkeys(spec['__fields__']):
            spec[n] = property(_property_factory_(n))
        for n in six.iterkeys(spec['__children__']):
            spec[n] = property(_child_factory_(n))

        return type.__new__(metacls, name, bases, spec)

