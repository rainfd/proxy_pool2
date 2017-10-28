import sys


def import_string(import_name):
    """Imports an object based on a string.
    """
    import_name = str(import_name)
    try:
        __import__(import_name)
    except ImportError:
        if '.' not in import_name:
            raise
    else:
        return sys.modules[import_name]

    module_name, obj_name = import_name.rsplit('.', 1)
    try:
        module = __import__(module_name, None, None, [obj_name])
    except ImportError:
        module = import_string(module_name)

    try:
        return getattr(module, obj_name)
    except AttributeError:
        raise


def from_object(ins, obj):
    """Load the upper variable from obj to ins
    """
    if isinstance(obj, str):
        obj = import_string(obj)
    for key in dir(obj):
        if key.isupper():
            ins[key] = getattr(obj, key)
