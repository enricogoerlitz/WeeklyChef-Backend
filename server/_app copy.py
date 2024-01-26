# """General Flask-Run file"""

# from flask import Flask, jsonify, request
# from flask_jwt_extended import jwt_required

# # from config import FlaskConfig
# from db import db
# from utils.initialize import initialize_database

# # test
# from services.auth.jwt import (
#     jwt_manager,
#     jwt_add_user,
#     userrole_required
# )

# from services.heathcheck.routes.heathcheck import bp as bp_heathcheck
# from services.auth.routes.auth import bp as bp_auth
# from services.auth.routes.user import bp as bp_user


# app = Flask(__name__)
# app.config.from_object(FlaskConfig)


# # register pages
# app.register_blueprint(bp_heathcheck)
# app.register_blueprint(bp_auth)
# app.register_blueprint(bp_user)


# # init app
# db.init_app(app)
# jwt_manager.init_app(app)



# @app.errorhandler(500)
# def internal_server_error(error):
#     err_msg = error if app.debug else "Unexpected internal error."
#     return {"error": err_msg}, 500


# with app.app_context():
#     db.create_all()
#     initialize_database(app=app)


# def create_app() -> Flask:
    
