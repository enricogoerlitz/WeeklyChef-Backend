# flake8: noqa
from server.core.models.db_models.unit import Unit
from server.db import db


def create_unit(name: str = "UnitName"):
    obj = Unit(name=name)

    db.session.add(obj)
    db.session.commit()

    return obj


# TEST GET


# TEST GET-LIST


# TEST-POST


# TEST UPDATE


# TEST DELETE
