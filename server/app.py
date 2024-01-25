"""General Flask-Run file"""

from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required

from config import FlaskConfig
from server.database.db import db

# test
from server.auth_service.jwt import (
    jwt_manager,
    jwt_add_user,
    userrole_required
)


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


if __name__ == "__main__":
    app.run(
        debug=True,
        threaded=True,
        port=3000
    )
