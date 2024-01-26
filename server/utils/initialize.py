from flask import Flask

from core.models.user import User, Role
from db import db


def initialize_database(app: Flask) -> None:
    """Create standard user, roles, ..."""
    with app.app_context():
        role_names = ["standard", "admin", "staff"]
        init_roles = [Role(name=name) for name in role_names]
        init_roles = [
            init_role
            for init_role in init_roles
            if not init_role.query.filter_by(name=init_role.name).first()
        ]

        if len(init_roles) > 0:
            db.session.add_all(init_roles)

        user_roles = Role.query.filter(Role.name.in_(role_names)).all()

        init_user = User(
            email="root.email@gmail.com",
            username="CoolerTeddy",
            password="init_password"
        )
        init_user.roles.extend(user_roles)

        if not init_user.query.filter_by(
                username=init_user.username).first():
            db.session.add(init_user)
        db.session.commit()
