import os
from pathlib import Path

from flask import Flask, jsonify
from flask_cors import CORS

from pause import models
from pause.pause import api


def create_app(config=None):
    app = Flask(__name__)
    default_database = f"sqlite:///{Path(__file__).with_name('pause.db')}"
    app.config.from_mapping(
        DATABASE_URL=os.getenv(
            "DB_CONNECTION",
            os.getenv("DATABASE_URL", default_database),
        ),
        CORS_ORIGINS=os.getenv("CORS_ORIGINS", "*"),
    )

    if config:
        app.config.update(config)

    models.configure_database(app.config["DATABASE_URL"])
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": app.config["CORS_ORIGINS"],
            },
        },
    )
    app.register_blueprint(api, url_prefix="/api/pause")

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    return app


app = create_app()
