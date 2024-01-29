from flask import Flask

from db import db
from core.models.db_models import Category


def test_create(app: Flask):
    # setting up test variables
    OBJ_NAME = "ObjectName"

    # execute code to test
    with app.app_context():
        obj = Category(name=OBJ_NAME)

        db.session.add(obj)
        db.session.commit()

        added_obj = Category.query.get(obj.id)

    # test code results
    assert added_obj is not None
    assert added_obj.name == OBJ_NAME
