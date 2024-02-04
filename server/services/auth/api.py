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
    title="WeeklyChef API v1.0 Auth-Service",
    description="WeeklyChef Mircoservice Auth-Service.",
    authorizations=authorizations,
    doc="/swagger-docs",
)
