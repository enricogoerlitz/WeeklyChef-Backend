"""
Util decorators for this app
"""

from errors import errors


def add_to_dict(cls):
    def to_dict(self):
        d = self.__dict__  # {attr: getattr(self, attr) for attr in vars(self)}
        del d["_sa_instance_state"]
        return d

    cls.to_dict = to_dict
    return cls


def add__str__(cls):
    def to_str(self):
        d = self.__dict__
        del d["_sa_instance_state"]
        return str(d)

    cls.__str__ = to_str
    cls.__repr__ = to_str
    return cls


def add_from_json_method(cls):
    """
    Class decorator to add from_json method to a class.

    Args:
        cls: The class to which the from_json method will be added.

    Returns:
        cls: The modified class.
    """
    @staticmethod
    def from_json(obj: dict) -> cls:
        """
        Creates object from JSON dictionary.

        Args:
            obj (dict): The JSON dictionary.

        Returns:
            cls: An instance of the class.
        """
        try:
            return cls(**obj)
        except TypeError as e:
            err_msg = str(e).replace("__init__() ", "").capitalize()
            raise errors.DbModelSerializationException(err_msg)

    # Add the from_json method to the class
    setattr(cls, "from_json", from_json)

    return cls
