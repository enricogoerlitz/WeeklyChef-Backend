import os
import time

from server.config.auth import create_app


DEBUG = os.environ.get("DEBUG")
THREADED = True
HOST = "0.0.0.0"
PORT = 5001


time.sleep(3)
app = create_app()

if __name__ == "__main__":
    app.run(
        debug=DEBUG,
        threaded=THREADED,
        host=HOST,
        port=PORT
    )
