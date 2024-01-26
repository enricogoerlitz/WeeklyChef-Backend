""""""
from flask_restx import Api

authorizations = {
    "Bearer": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}

# http://localhost:8080/swagger-docs
api = Api(
    version="1.0",
    title="WeeklyChef API v1.0",
    description="This is the monolith WeeklyChef API Version, "
                + "which contains all routes",
    authorizations=authorizations,
    doc="/swagger-docs",
)
