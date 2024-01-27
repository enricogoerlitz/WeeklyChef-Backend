from flask_restx import Namespace


ns = Namespace(
    name="Recipe",
    description=__name__,
    path="/api/v1/"
)
