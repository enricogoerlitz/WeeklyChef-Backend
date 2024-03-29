from server.errors import errors


def add_to_dict_method(cls):
    def to_dict(self):
        d = self.__dict__
        if "_sa_instance_state" in d.keys():
            del d["_sa_instance_state"]
        return d

    setattr(cls, "to_dict", to_dict)

    return cls


def add__str__method(cls):
    def to_str(self):
        d = self.__dict__
        if "_sa_instance_state" in d.keys():
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
    def from_json(obj: dict, api_model) -> cls:
        """
        Creates object from JSON dictionary.

        Args:
            obj (dict): The JSON dictionary.

        Returns:
            cls: An instance of the class.
        """
        base_json = {key: None for key in api_model.keys()}
        final_obj = {**base_json, **obj}

        try:
            return cls(**final_obj)
        except TypeError as e:
            err_msg = str(e).replace("__init__() ", "").capitalize()
            raise errors.DbModelSerializationException(err_msg)

    setattr(cls, "from_json", from_json)

    return cls
