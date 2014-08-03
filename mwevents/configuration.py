import copy


def load(self, doc):
    config = copy.deepcopy(DEFAULT)
    config.update(doc)
    
    return config

DEFAULT = {
    'expiration_format': "expires %H:%M, %d %B %Y (UTC)",
    'indefinite': "indefinite"
}
