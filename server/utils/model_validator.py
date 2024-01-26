""""""
import re

from errors import errors


def validate_length(fieldname: str, value: str, min: int, max: int) -> None:
    """
    Validates a field length

    Args:
        fieldname (str): the name of the filed
        value (str): the value of the field
        min (int): minimum length
        max (int): maximum length

    Raises:
        errors.DbModelFieldRequieredException: if field was null
        errors.DbModelFieldLengthException: if field was to short or to long
    """
    if value is None:
        err_msg = f"The field {fieldname} is required but was null."  # noqa
        raise errors.DbModelFieldRequieredException(err_msg)

    vlen = len(value)
    if vlen < min or vlen > max:
        err_msg = f"The field {fieldname} should have a length of minumum {min} and maximum {max}."  # noqa
        raise errors.DbModelFieldLengthException(err_msg)


def validate_email(fieldname: str, email: str, max_length: int) -> None:
    """_summary_

    Args:
        fieldname (str): the name of the filed
        email (str): the email value
        max_length (int): maximum length

    Raises:
        errors.DbModelFieldEmailInvalidException: if email does not match email regex  # noqa
        errors.DbModelFieldRequieredException: if field was null
        errors.DbModelFieldLengthException: if field was to short or to long
    """
    email_regex = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        err_msg = "The E-Mail field does not contain a valid email."
        raise errors.DbModelFieldEmailInvalidException(err_msg)

    validate_length(
        fieldname=fieldname,
        value=email,
        min=3,
        max=max_length
    )
