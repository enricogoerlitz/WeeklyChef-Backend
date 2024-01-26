"""
Collection of app errors
"""


class UserAlreadyExistingException(Exception):
    """
    The user is already existing in the database
    """

    def __init__(self):
        self.message = "User already existing."
        super().__init__(self.message)


class DbModelNotFoundException(Exception):
    """
    The db model was not found in database.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class DbModelValidationException(Exception):
    """
    The db model validation has an error.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class DbModelFieldLengthException(DbModelValidationException):
    """
    The db model field is to short or to long
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class DbModelFieldRequieredException(DbModelValidationException):
    """
    The db model field is required, but was null
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class DbModelFieldEmailInvalidException(DbModelValidationException):
    """
    The db model field email was invalid
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class InvalidLoginCredentialsException(Exception):
    """
    When the email, username or passoword are invalid
    """

    def __init__(self):
        self.message = "User credentials are invalid."
        super().__init__(self.message)


class DbModelSerializationException(Exception):
    """
    When parameter mapping not working because of an unexpected attribute.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
