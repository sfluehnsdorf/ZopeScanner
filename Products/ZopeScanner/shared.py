"""Zope Scanner - Shared Resources."""


from Products.ZopeScanner.imports_zope import Item


__all__ = [
    'cmp',
    'sort_by_key',
    'token_sort_by_key',
]


try:  # until Python-2.7.18
    cmp
except NameError:
    def cmp(a, b):
        """Compare a and b (polyfill for Python 2.4 or newer)."""
        return (a > b) - (a < b)


def sort_by_key(items, key):
    """Sort items by key."""
    try:
        items.sort(key=lambda item: item[key])
    except Exception:  # TODO: specify Exception

        def compare_by_key(x, y):
            return cmp(x[key], y[key])

        items.sort(compare_by_key)
    return items


# TODO: implement (maybe rename) human readable sort function
# - for example: '__A', '__a', '_A', '_a', 'A', 'a'
# - for example: '5', '10', '15', '20', '25'
token_sort_by_key = sort_by_key


class ObjectRetrievalError(Exception):
    """Exception for errors raised if object can not be ."""

    def __init__(self, root_object, path, key, parents):
        super(ObjectRetrievalError, self).__init__(
            'Can not retrieve object "%s" of path "%s"' % (key, path))
        self.root_object = root_object
        self.path = path
        self.key = key
        self.parents = parents

    def __reduce__(self):
        return (ObjectRetrievalError, (self.root_object, self.path, self.key))


def get_object_from_path(root_object, path):
    """Return object found by starting at root and traversing path."""
    if path and path[0] != '/':
        path = '/' + path
    index = 0
    item = root_object
    parents = [('', item),]
    while index < len(path):
        if path[index] == '/':
            key = ''
            index = index + 1
            while index < len(path) and path[index] != '/':
                key = key + path[index]
                index = index + 1
            try:
                key = int(key)
                item = item[key]
            except Exception:  # TODO: review Exception
                try:
                    key in item
                    item = item[key]
                except Exception:  # TODO: review Exception
                    try:
                        item = getattr(item, key)
                    except Exception:  # TODO: review Exception
                        raise ObjectRetrievalError(
                            root_object=root_object,
                            path=path,
                            key=key,
                            parents=parents
                        )
            parents.append((key, item))
        else:
            break
    return parents, item


def get_id_of_object(specimen):
    """Return the id of an OFS object."""
    object_id = None
    if isinstance(specimen, Item):
        if hasattr(specimen, 'getId'):
            try:
                object_id = specimen.getId()
            except TypeError:
                pass
        if object_id is None and hasattr(specimen, 'id'):
            if callable(specimen.id):
                try:
                    object_id = specimen.id()
                except TypeError:
                    pass
            else:
                object_id = specimen.id
    if object_id is None and hasattr(specimen, '__name__'):
        object_id = specimen.__name__
    return object_id
