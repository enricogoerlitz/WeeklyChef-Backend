"""
Execution file für Microservice
"""
import os

from dotenv import load_dotenv

from server.services.auth.config import create_app


load_dotenv()

DEBUG = os.environ.get("DEBUG")
THREADED = True
PORT = 5001


if __name__ == "__main__":

    app = create_app()

    app.run(
        debug=DEBUG,
        threaded=THREADED,
        port=PORT
    )
