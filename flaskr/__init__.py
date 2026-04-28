from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

socketio = SocketIO()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'tower-defense-secret-key'

    # Autoriser le frontend React (port 5173)
    CORS(app, origins=["http://localhost:5173"])
    socketio.init_app(app, cors_allowed_origins=["http://localhost:5173"])

    # Importer et enregistrer les routes HTTP
    from .routes import main_bp
    app.register_blueprint(main_bp)

    # Importer les événements WebSocket (les enregistre automatiquement)
    from . import events  # noqa: F401

    return app
