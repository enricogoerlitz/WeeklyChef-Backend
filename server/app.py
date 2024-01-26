"""General Flask-Run file"""

from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required

from config import FlaskConfig
from database.db import db
from utils.init_db import db_init

# test
from auth_service.jwt import (
    jwt_manager,
    jwt_add_user,
    userrole_required
)
from core.models.user import Role


app = Flask(__name__)
app.config.from_object(FlaskConfig)


db.init_app(app)
jwt_manager.init_app(app)


@app.route('/protected', methods=['GET'])
@jwt_required()
@jwt_add_user
@userrole_required(["admin", "editor"])
def protected():
    return jsonify(logged_in_as=request.user.to_dict()), 200


with app.app_context():
    db.create_all()
    role = Role.query.filter_by(name="admin").first()

    # usr = User(email="rico.goerlitz@gmail5.com", password="passwordTest")  # noqa
    # usr.roles.append(role)

    # db.session.add(usr)
    # db.session.commit()

    # print(Role.query.filter_by(name="admin").first())
    # print(User.query.filter(User.email.like('rico.goerlitz%')).first())


db_init(app=app)


if __name__ == "__main__":
    app.run(
        debug=True,
        threaded=True,
        port=3000
    )
