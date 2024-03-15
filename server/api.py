import os

from flask_restx import Api
from dotenv import load_dotenv


load_dotenv()


authorizations = {
    "Bearer Auth": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}

# http://localhost:{PORT}/swagger-docs
# Bearer {token} // so login!
api = Api(
    version=os.environ.get("SWAGGER_API_VERSION"),
    title=os.environ.get("SWAGGER_API_TITLE"),
    description=os.environ.get("SWAGGER_API_DESCRIPTION"),
    authorizations=authorizations,
    security="Bearer Auth",
    doc="/swagger-docs",
)
