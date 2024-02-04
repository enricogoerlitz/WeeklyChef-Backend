import os

from dotenv import load_dotenv

from config.recipe import create_app


load_dotenv()


DEBUG = os.environ.get("DEBUG")
THREADED = True
HOST = "0.0.0.0"
PORT = 5002


if __name__ == "__main__":
    app = create_app()

    app.run(
        debug=DEBUG,
        threaded=THREADED,
        host=HOST,
        port=PORT
    )
