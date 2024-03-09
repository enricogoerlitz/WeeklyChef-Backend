from flask import Flask

from server.core.models.db_models.user import Role, User
from server.db import db


def initialize_dummy_database(app: Flask) -> None:
    """Create standard user, roles, ..."""
    with app.app_context():
        # >>> AUTH / USER INIT
        # ROLES
        role_names = ["standard", "admin", "staff"]
        init_roles = [Role(name=name) for name in role_names]
        init_roles = [
            init_role
            for init_role in init_roles
            if not init_role.query.filter_by(name=init_role.name).first()
        ]

        if len(init_roles) > 0:
            db.session.add_all(init_roles)

        admin_role = Role.query.filter_by(name="admin").first()
        staff_role = Role.query.filter_by(name="staff").first()
        std_role = Role.query.filter_by(name="standard").first()

        all_roles = [admin_role, staff_role, std_role]
        staff_roles = [staff_role, std_role]

        # USERS
        superuser = User(
            email="root.email@gmail.com",
            username="CoolerTeddy",
            password="password"
        )
        staff_user = User(
            email="root2.email@gmail.com",
            username="CoolerTeddy2",
            password="password"
        )
        std_user = User(
            email="root3.email@gmail.com",
            username="CoolerTeddy3",
            password="password"
        )
        superuser.roles.extend(all_roles)
        staff_user.roles.extend(staff_roles)
        std_user.roles.append(std_role)

        init_users = [superuser, staff_user, std_user]

        db.session.add_all(init_users)

        db.session.commit()
