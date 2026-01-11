from flask import Flask
import os

def create_app():
    app = Flask(__name__)

    app.config["UPLOAD_FOLDER"] = "static/uploads"
    app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
    app.config["DATABASE"] = os.getenv("DATABASE_PATH", "instance/database.db")

    from .routes import bp
    app.register_blueprint(bp)

    from .db import init_db
    init_db(app)

    return app
