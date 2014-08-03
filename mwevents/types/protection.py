import re

from jsonable import instance, JSONable

from .. import configuration
from .timestamp import Timestamp


class Protection(JSONable):
    __slots__ = ('action', 'group', 'expiration')
    
    LOG_PARAMS_RE = re.compile(r"\[([^=]+)=([^\]]+)\] \(([^\]]+)\)([\ \n]|$)")
    
    def initialize(self, action=None, group=None, expiration=None):
        self.action = str(action) if action is not None else None
        
        self.group = str(group) if group is not None else None
        
        self.expiration = Timestamp(expiration) if expiration is not None \
                          else None
    
    @classmethod
    def from_params(cls, params,
            indefinite=configuration.DEFAULT['indefinite'],
            expiration_format=configuration.DEFAULT['expiration_format']):
    
        for match in cls.LOG_PARAMS_RE.finditer(params):
            action, group, expiration, _ = match.groups()
            
            if expiration == indefinite:
                expiration = None
            else:
                expiration = Timestamp.strptime(expiration, expiration_format)
            
            yield cls(action, group, expiration)
