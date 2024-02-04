import os

from dotenv import load_dotenv

from config.auth import create_app


load_dotenv()


DEBUG = os.environ.get("DEBUG")
THREADED = True
HOST = "0.0.0.0"
PORT = 5001


if __name__ == "__main__":
    auth_app = create_app()

    auth_app.run(
        debug=DEBUG,
        threaded=THREADED,
        host=HOST,
        port=PORT
    )
