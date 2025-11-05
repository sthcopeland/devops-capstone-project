import collections, collections.abc
for name in ("Callable","Mapping","MutableMapping","Sequence"):
    if not hasattr(collections, name):
        setattr(collections, name, getattr(collections.abc, name))
