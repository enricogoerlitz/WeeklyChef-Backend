from flask_sqlalchemy.model import Model
from server.db import db


def create_obj(obj: Model):
    db.session.add(obj)
    db.session.commit()

    return obj
