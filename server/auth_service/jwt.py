from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity
)


jwt_manager = JWTManager()


def jwt_add_user(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        request["user"] = get_jwt_identity()
        return f(*args, **kwargs)
    return wrapper


def userrole_required(required_roles: list[str]):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user_roles = request.user.roles if hasattr(request, 'user') and hasattr(request.user, 'roles') else []
            if any(role in user_roles for role in required_roles):
                return f(*args, **kwargs)
            else:
                return jsonify(message='Unauthorized. Role required.'), 403
        return wrapper
    return decorator


# Create an endpoint for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = find_user_by_username(username)

    if user and password == user.password:
        # Identity can be any data that is json serializable
        access_token = create_access_token(identity=user.to_dict())
        return jsonify(access_token=access_token), 200

    return jsonify(message='Invalid credentials'), 401
