"""Util decorators for this app"""


def add_to_dict(cls):
    def to_dict(self):
        d = {attr: getattr(self, attr) for attr in vars(self)}
        del d["_sa_instance_state"]
        return d

    cls.to_dict = to_dict
    return cls
