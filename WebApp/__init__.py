from flask import Flask
import os

from .route import main

def create_app():
    SECRET_KEY = os.getenv("SECRET_KEY")
    app = Flask(__name__)
    app.config["DEBUG"] = True
    app.config["use_reloader"] = False
    app.secret_key = SECRET_KEY
    app.register_blueprint(main)

    #socketio.init_app(app, cors_allowed_origins="*", ping_timeout=30, ping_interval=25, async_mode='eventlet')

    return app