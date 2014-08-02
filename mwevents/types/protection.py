import re

from jsonable import instance, JSONable

from .. import defaults
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
                         indefinite=defaults.PARAMS_INDEFINITE,
                         time_format=defaults.PARAMS_TIME_FORMAT):
    
        for match in cls.LOG_PARAMS_RE.finditer(params):
            action, group, expiration, _ = match.groups()
            
            if expiration == indefinite:
                expiration = None
            else:
                expiration = Timestamp.strptime(expiration, time_format)
            
            yield cls(action, group, expiration)
