from jsonable import JSONable


class UnavailableType(JSONable):
    """
    A NoneType-like singleton instance that represents missing data because it
    is unavailable -- as opposed to real None/NULL-type values.

    Example:
        >>> from mwevents.types import UnavailableType
        >>> Unavailable = UnavailableType()
        >>> Unavailable.to_json()
        {'Unavailable': True}
        >>> Unavailable(Unavailable.to_json())
        Unavailable
        >>> Unavailable is None
        False


    """
    NAME = "Unavailable"
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __call__(self, doc_or_inst):
        if isinstance(doc_or_inst, self.__class__):
            return doc_or_inst
        elif isinstance(doc_or_inst, dict):
            return self.from_json(doc_or_inst)
        else:
            raise TypeError("Expected {0}, ".format(self) + \
                            "got {0}".format(repr(doc_or_inst)))

    def __init__(self, *args, **kwargs): pass
    def initialize(self): pass

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.NAME
    
    @classmethod
    def otherwise(cls, val, func, none_ok=True):
        if none_ok and val is None:
            return val
        else:
            try:
                return cls._instance(val)
            except TypeError as e:
                return func(val)
            
    
    @classmethod
    def to_json(cls):
        return {cls.NAME: True}
    
    @classmethod
    def from_json(cls, doc):
        if isinstance(doc, dict) and cls.NAME in doc:
            return cls()
        else:
            raise TypeError("doc is not of the right type.  " + \
                            "Expected: {0} ".format(cls.to_json()) + \
                            "Got: {0}".format(doc))

 
Unavailable = UnavailableType()
"""
A NoneType-like singleton instance that represents missing data because it is
unavailable -- as opposed to real NULL values.

Example:
    >>> from mwevents.types import Unavailable
    >>> Unavailable.to_json()
    {'Unavailable': True}
    >>> Unavailable(Unavailable.to_json())
    Unavailable
    >>> Unavailable is None
    False

"""
