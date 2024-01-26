"""
Helper for basic CRUD operations
"""
from typing import Any
from db import db


def handle_get(
        model: db.Model,
        id: Any
) -> Any:
    return model.query.get(id)


def handle_get_list(model: db.Model) -> list[Any]:
    return model.query.all()


def handle_update(
        model: db.Model,
        id: Any,
        update_data: dict
) -> Any:
    obj = model.query.get(id)
    for key, value in update_data.items():
        if hasattr(obj, key):
            setattr(obj, key, value)
    db.session.commit()
    return obj


def handle_delete(
        model: db.Model,
        id: Any
) -> Any:
    obj = model.query.get(id)
    model.query.delete(obj)
