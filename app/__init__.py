import eventlet

eventlet.monkey_patch()

import time
import threading

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os
from flask_cors import CORS
from flask_socketio import SocketIO

db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins="*", async_mode="eventlet")


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    socketio.init_app(app)

    from app.presentation.routes import main_bp
    app.register_blueprint(main_bp)

    from app.business.models import restaurant, product, menu, customer, order, address
    from app.business.models import motorcycle, driver, shift, issue, photo

    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'uploads')
    CORS(app)

    with app.app_context():
        db.create_all()

    # ⬇️ Aquí defines y lanzas la función que emite notificaciones

    return app
