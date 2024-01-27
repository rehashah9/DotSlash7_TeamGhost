from flask import Flask
from flask_socketio import SocketIO
from flask import session
from flask_socketio import emit, join_room, leave_room
import logging

socketio = SocketIO()


def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'
    logging.info("Flask Server Started")
    from .routes import routes as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)


    return app