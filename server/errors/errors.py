from typing import Any


class UserAlreadyExistingException(Exception):
    """
    The user is already existing in the database
    """

    def __init__(self):
        message = "User already existing."
        super().__init__(message)


class DbModelAlreadyExistingException(Exception):
    """
    When the db model is already existing
    """

    def __init__(self, model: Any, data: dict):
        message = f"Model {model.__name__} already existing with the data {str(data)}"  # noqa
        super().__init__(message)


class DbModelNotFoundException(Exception):
    """
    The db model was not found in database.
    """

    def __init__(self, message: str):
        super().__init__(message)


class DbModelValidationException(Exception):
    """
    The db model validation has an error.
    """

    def __init__(self, message: str):
        super().__init__(message)


class DbModelFieldLengthException(DbModelValidationException):
    """
    The db model field is to short or to long
    """

    def __init__(self, message: str):
        super().__init__(message)


class DbModelFieldRequieredException(DbModelValidationException):
    """
    The db model field is required, but was null
    """

    def __init__(self, fieldname: str):
        message = f"The field '{fieldname}' is required but was null."
        super().__init__(message)


class DbModelFieldEmailInvalidException(DbModelValidationException):
    """
    The db model field email was invalid
    """

    def __init__(self, message: str):
        super().__init__(message)


class DbModelFieldTypeError(DbModelValidationException):
    """
    The db model field was invalid like
        -  int expected, was float
        -  int expected, was string ...
    """

    def __init__(self, fieldname: str, value: Any, expected_types: list[type]):
        expected_types = ", ".join([
            expected_type.__name__ for expected_type in expected_types])
        message = f"Field '{fieldname}' ({value}) was type of {type(value)} " \
                  + f", but expected types: {expected_types}"
        super().__init__(message)


class DbModelFieldValueError(DbModelValidationException):
    """
    The db model field was invalid like
        -  int expected, was float
        -  int expected, was string ...
    """

    def __init__(self, message: str):
        super().__init__(message)


class InvalidLoginCredentialsException(Exception):
    """
    When the email, username or passoword are invalid
    """

    def __init__(self):
        message = "User credentials are invalid."
        super().__init__(message)


class DbModelSerializationException(Exception):
    """
    When parameter mapping not working because of an unexpected attribute.
    """

    def __init__(self, message: str):
        super().__init__(message)


class DbModelUnqiueConstraintException(Exception):
    """
    When a column with a given value is already existing
    """

    def __init__(self, filedname: str, value: Any) -> None:
        err_msg = f"Field '{filedname}' with value '{str(value)}' is already existing."  # noqa
        super().__init__(err_msg)
