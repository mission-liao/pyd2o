import six
from .base import BaseObj, FieldMeta, is_array, is_map

class Pref(six.with_metaclass(FieldMeta, BaseObj)):
    __fields__ = {
        'color': dict(default='green'),
        'size': dict(default='medium'),
    }


class User(six.with_metaclass(FieldMeta, BaseObj)):
    """ User
    """
    __fields__ = {
        'email': dict(required=True), # field with required
        'id': dict(required=True, default=0), #  field with default
        'name': dict(required=True, default=''),
    }

    __children__ = {
        'preference': dict(child=Pref), # a normal child
        'pps': dict(child=is_array(Pref)), # container type: ArrayBase and MapBase are created dynamically by is_array and is_map
        'xxx': dict(child=is_map(is_array(Pref))), # is_array and is_map can be chained to match expected json structure
    }
