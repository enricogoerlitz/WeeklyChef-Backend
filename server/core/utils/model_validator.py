""""""
import re

from typing import Any
from dateutil import parser
from datetime import datetime, date

from errors import errors


def validate_string(
        *,
        fieldname: str,
        value: str,
        min_length: int,
        max_length: int,
        nullable: bool = False
) -> None:
    """
    Validates the field by min and max length and is string.

    Args:
        fieldname (str): the name of the filed
        value (str): the value of the field
        min (int): minimum length
        max (int): maximum length

    Raises:
        errors.DbModelFieldRequieredException: if field was null
        errors.DbModelFieldLengthException: if field was to short or to long
    """

    if nullable and value is None:
        return

    validate_field_required(fieldname, value)

    if not isinstance(value, str):
        raise errors.DbModelFieldTypeError(fieldname, value, [str])

    vlen = len(value)
    if vlen < min_length or vlen > max_length:
        err_msg = f"The field {fieldname} should have a length of minumum {min_length} and maximum {max_length}."  # noqa
        raise errors.DbModelFieldLengthException(err_msg)


def validate_email(
        *,
        fieldname: str,
        email: str,
        max_length: int,
        nullable: bool = False
) -> None:
    """
    Validates a string as email.

    Args:
        fieldname (str): the name of the filed
        email (str): the email value
        max_length (int): maximum length

    Raises:
        errors.DbModelFieldEmailInvalidException: if email does not match email regex  # noqa
        errors.DbModelFieldRequieredException: if field was null
        errors.DbModelFieldLengthException: if field was to short or to long
    """

    if nullable and email is None:
        return

    validate_field_required(fieldname, email)

    if not isinstance(email, str):
        raise errors.DbModelFieldTypeError(fieldname, email, [str])

    email_regex = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        err_msg = "The E-Mail field does not contain a valid email."
        raise errors.DbModelFieldEmailInvalidException(err_msg)

    validate_string(
        fieldname=fieldname,
        value=email,
        min_length=3,
        max_length=max_length
    )


def validate_float(
        *,
        fieldname: str,
        value: float,
        min_: float = None,
        max_: float = None,
        nullable: bool = False
) -> None:
    """_summary_

    Args:
        fieldname (str): _description_
        value (float): _description_
        min (float, optional): _description_. Defaults to None.
        max (float, optional): _description_. Defaults to None.
        nullable (bool, optional): _description_. Defaults to False.

    Raises:
        errors.DbModelFieldTypeError: _description_
        errors.DbModelFieldValueError: _description_
    """
    if nullable and value is None:
        return

    validate_field_required(fieldname, value)

    if not isinstance(value, (float, int)):
        raise errors.DbModelFieldTypeError(fieldname, value, [float])

    if (
        (min_ is not None and value < min_) or
        (max_ is not None and value > max_)
    ):
        err_msg = f"The field {fieldname} should have a minumum value of {min_} and maximum value of {max_}."  # noqa
        raise errors.DbModelFieldValueError(err_msg)


def validate_integer(
        *,
        fieldname: str,
        value: int,
        min_: int = None,
        max_: int = None,
        nullable: bool = False
) -> None:
    """_summary_

    Args:
        fieldname (str): _description_
        value (int): _description_
        min (int, optional): _description_. Defaults to None.
        max (int, optional): _description_. Defaults to None.
        nullable (bool, optional): _description_. Defaults to False.

    Raises:
        errors.DbModelFieldTypeError: _description_
        errors.DbModelFieldValueError: _description_
    """
    if nullable and value is None:
        return

    validate_field_required(fieldname, value)

    if not isinstance(value, int):
        raise errors.DbModelFieldTypeError(fieldname, value, [int])

    if (
        (min_ is not None and value < min_) or
        (max_ is not None and value > max_)
    ):
        err_msg = f"The field {fieldname} should have a minumum value of {min_} and maximum value of {max_}."  # noqa
        raise errors.DbModelFieldValueError(err_msg)


def validate_boolean(
        *,
        fieldname: str,
        value: bool,
        nullable: bool = False
) -> None:
    if nullable and value is None:
        return

    validate_field_required(fieldname, value)

    if not isinstance(value, bool):
        raise errors.DbModelFieldTypeError(fieldname, value, [bool])


def validate_field_required(
        fieldname: str,
        value: Any
) -> None:
    """
    Checks is given value None and throws an exception if value is None

    Args:
        fieldname (str): fieldname
        value (Any): any value to compare

    Raises:
        errors.DbModelFieldRequieredException: if value is None
    """

    if value is None:
        raise errors.DbModelFieldRequieredException(fieldname)


def validate_datetime(
        fieldname: str,
        value: Any,
        min_datetime: datetime,
        max_datetime: datetime,
        nullable: bool = False
) -> None:
    if nullable and value is None:
        return

    validate_field_required(fieldname, value)

    try:
        value = parser.parse(value)
    except Exception:
        raise errors.DbModelFieldTypeError(fieldname, value, [datetime, date])

    if (
        (min_datetime is not None and value < min_datetime) or
        (max_datetime is not None and value > max_datetime)
    ):
        err_msg = f"The field {fieldname} should have a minumum value of {min_datetime} and maximum value of {max_datetime}."  # noqa
        raise errors.DbModelFieldValueError(err_msg)
