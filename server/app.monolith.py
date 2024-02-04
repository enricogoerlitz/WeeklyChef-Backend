import sys
sys.path.append("..")
sys.path.append("../..")

from config.monolith import create_app  # noqa


if __name__ == "__main__":
    app = create_app()

    app.run(
        debug=True,
        threaded=True,
        host="0.0.0.0",
        port=8080
    )
