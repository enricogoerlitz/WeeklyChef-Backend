"""Flask configurations"""


class FlaskConfig:
    SQLALCHEMY_DATABASE_URI = "mysql://serviceuser:devpassword@127.0.0.1:3307/weeklychef"  # noqa
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "f1ae9b76935d89426cec6993698e865c1a12574ac9deb393dcdbc8f21eb76998"  # noqa
