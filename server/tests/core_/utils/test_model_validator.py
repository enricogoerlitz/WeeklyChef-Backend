import pytest

from server.errors import errors
from server.core.utils import model_validator as ModelValidator


def test_validate_field_required():
    # given
    value = "Value is set"

    # when + then
    ModelValidator.validate_field_required(
        fieldname="value",
        value=value
    )  # assert no Exception


def test_validate_field_required_field_is_none():
    # given
    value = None

    # when + then
    with pytest.raises(errors.DbModelFieldRequieredException):
        ModelValidator.validate_field_required(
            fieldname="value",
            value=value
        )


def test_validate_string():
    # given
    value = "This is a valid string."

    # when + then
    ModelValidator.validate_string(
        fieldname="value",
        value=value,
        min_length=1,
        max_length=50,
        nullable=False
    )  # assert no Exception


def test_validate_string_field_is_none_and_nullable():
    # given
    value = None

    # when + then
    ModelValidator.validate_string(
        fieldname="value",
        value=value,
        min_length=1,
        max_length=50,
        nullable=True
    )  # assert no Exception


def test_validate_string_field_is_none_and_not_nullable():
    # given
    value = None

    # when + then
    with pytest.raises(errors.DbModelFieldRequieredException):
        ModelValidator.validate_string(
            fieldname="value",
            value=value,
            min_length=1,
            max_length=50,
            nullable=False
        )


def test_validate_string_field_not_a_string():
    # given
    value = 1

    # when + then
    with pytest.raises(errors.DbModelFieldTypeError):
        ModelValidator.validate_string(
            fieldname="value",
            value=value,
            min_length=1,
            max_length=50,
            nullable=False
        )


def test_validate_string_length():
    # given
    value_to_short = "Test"
    value_to_long = "T" * 51

    # when + then
    with pytest.raises(errors.DbModelFieldLengthException):
        ModelValidator.validate_string(
            fieldname="value",
            value=value_to_short,
            min_length=5,
            max_length=50,
            nullable=False
        )

    with pytest.raises(errors.DbModelFieldLengthException):
        ModelValidator.validate_string(
            fieldname="value",
            value=value_to_long,
            min_length=1,
            max_length=50,
            nullable=False
        )


def test_validate_email():
    # given
    email = "example.email@gmail.com"

    # when + then
    ModelValidator.validate_email(
        fieldname="value",
        email=email,
        max_length=100
    )  # assert no Exception


def test_validate_email_field_is_none_and_nullable():
    # given
    email = None

    # when + then
    ModelValidator.validate_email(
        fieldname="value",
        email=email,
        max_length=100,
        nullable=True
    )  # assert no Exception


def test_validate_email_field_is_none_and_not_nullable():
    # given
    email = None

    # when + then
    with pytest.raises(errors.DbModelFieldRequieredException):
        ModelValidator.validate_email(
            fieldname="value",
            email=email,
            max_length=100,
            nullable=False
        )


def test_validate_email_field_is_not_email():
    # given
    email = "this is no valid email.com"

    # when + then
    with pytest.raises(errors.DbModelFieldEmailInvalidException):
        ModelValidator.validate_email(
            fieldname="value",
            email=email,
            max_length=100,
            nullable=False
        )


def test_validate_float():
    # given
    value = 5.

    # when + then
    ModelValidator.validate_float(
        fieldname="value",
        value=value,
        min_=1.,
        max_=6.,
        nullable=False
    )  # assert no Exception


def test_validate_float_field_is_none_and_nullable():
    # given
    value = None

    # when + then
    ModelValidator.validate_float(
        fieldname="value",
        value=value,
        min_=1.,
        max_=6.,
        nullable=True
    )  # assert no Exception


def test_validate_float_field_is_none_and_not_nullable():
    # given
    value = None

    # when + then
    with pytest.raises(errors.DbModelFieldRequieredException):
        ModelValidator.validate_float(
            fieldname="value",
            value=value,
            min_=1.,
            max_=6.,
            nullable=False
        )  # assert no Exception


def test_validate_float_field_is_not_nummeric():
    # given
    value = "5"

    # when + then
    with pytest.raises(errors.DbModelFieldTypeError):
        ModelValidator.validate_float(
            fieldname="value",
            value=value,
            min_=1.,
            max_=6.,
            nullable=False
        )


def test_validate_float_field_value_not_valid():
    # given
    value_to_low = -1.
    value_to_high = 11.

    # when + then
    with pytest.raises(errors.DbModelFieldValueError):
        ModelValidator.validate_float(
            fieldname="value",
            value=value_to_low,
            min_=0,
            max_=10,
            nullable=False
        )

    with pytest.raises(errors.DbModelFieldValueError):
        ModelValidator.validate_float(
            fieldname="value",
            value=value_to_high,
            min_=0.,
            max_=10.,
            nullable=False
        )


def test_validate_float_field_value_not_valid_only_oneway():
    # given
    value_to_low = -1.
    value_to_high = 11.

    # when + then
    ModelValidator.validate_float(
        fieldname="value",
        value=value_to_low,
        min_=None,
        max_=10,
        nullable=False
    )  # assert no Exception

    ModelValidator.validate_float(
        fieldname="value",
        value=value_to_high,
        min_=0.,
        max_=None,
        nullable=False
    )  # assert no Exception

    with pytest.raises(errors.DbModelFieldValueError):
        ModelValidator.validate_float(
            fieldname="value",
            value=value_to_low,
            min_=0.,
            max_=None,
            nullable=False
        )

    with pytest.raises(errors.DbModelFieldValueError):
        ModelValidator.validate_float(
            fieldname="value",
            value=value_to_high,
            min_=None,
            max_=10,
            nullable=False
        )


def test_validate_integer():
    # given
    value = 5

    # when + then
    ModelValidator.validate_integer(
        fieldname="value",
        value=value,
        min_=1.,
        max_=6.,
        nullable=False
    )  # assert no Exception


def test_validate_integer_field_is_none_and_nullable():
    # given
    value = None

    # when + then
    ModelValidator.validate_integer(
        fieldname="value",
        value=value,
        min_=1,
        max_=6,
        nullable=True
    )  # assert no Exception


def test_validate_integer_field_is_none_and_not_nullable():
    # given
    value = None

    # when + then
    with pytest.raises(errors.DbModelFieldRequieredException):
        ModelValidator.validate_integer(
            fieldname="value",
            value=value,
            min_=1,
            max_=6,
            nullable=False
        )  # assert no Exception


def test_validate_integer_field_is_not_integer():
    # given
    value = "5"
    value_float = 5.

    # when + then
    with pytest.raises(errors.DbModelFieldTypeError):
        ModelValidator.validate_integer(
            fieldname="value",
            value=value,
            min_=1,
            max_=6,
            nullable=False
        )

    with pytest.raises(errors.DbModelFieldTypeError):
        ModelValidator.validate_integer(
            fieldname="value",
            value=value_float,
            min_=1,
            max_=6,
            nullable=False
        )


def test_validate_integer_field_value_not_valid():
    # given
    value_to_low = -1
    value_to_high = 11

    # when + then
    with pytest.raises(errors.DbModelFieldValueError):
        ModelValidator.validate_integer(
            fieldname="value",
            value=value_to_low,
            min_=0,
            max_=10,
            nullable=False
        )

    with pytest.raises(errors.DbModelFieldValueError):
        ModelValidator.validate_integer(
            fieldname="value",
            value=value_to_high,
            min_=0,
            max_=10,
            nullable=False
        )


def test_validate_integer_field_value_not_valid_only_oneway():
    # given
    value_to_low = -1
    value_to_high = 11

    # when + then
    ModelValidator.validate_integer(
        fieldname="value",
        value=value_to_low,
        min_=None,
        max_=10,
        nullable=False
    )  # assert no Exception

    ModelValidator.validate_integer(
        fieldname="value",
        value=value_to_high,
        min_=0,
        max_=None,
        nullable=False
    )  # assert no Exception

    with pytest.raises(errors.DbModelFieldValueError):
        ModelValidator.validate_integer(
            fieldname="value",
            value=value_to_low,
            min_=0,
            max_=None,
            nullable=False
        )

    with pytest.raises(errors.DbModelFieldValueError):
        ModelValidator.validate_integer(
            fieldname="value",
            value=value_to_high,
            min_=None,
            max_=10,
            nullable=False
        )


def test_validate_boolean():
    # given
    value = True

    # when + then
    ModelValidator.validate_boolean(
        fieldname="value",
        value=value,
        nullable=False
    )  # assert no Exception


def test_validate_boolean_field_is_none_and_nullable():
    # given
    value = None

    # when + then
    ModelValidator.validate_boolean(
        fieldname="value",
        value=value,
        nullable=True
    )  # assert no Exception


def test_validate_boolean_field_is_none_and_not_nullable():
    # given
    value = None

    # when + then
    with pytest.raises(errors.DbModelFieldRequieredException):
        ModelValidator.validate_boolean(
            fieldname="value",
            value=value,
            nullable=False
        )


def test_validate_boolean_field_is_not_boolean():
    # given
    value = "True"

    # when + then
    with pytest.raises(errors.DbModelFieldTypeError):
        ModelValidator.validate_boolean(
            fieldname="value",
            value=value,
            nullable=False
        )
