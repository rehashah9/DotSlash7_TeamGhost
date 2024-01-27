from dotenv import load_dotenv
load_dotenv()
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
import logging
# from app.routes.execute_raw.main import excute_raw_app
# from engine.app.routes.main import steampipe_app
# from app.routes.query.socket_user_query import socket_user_query
logging.basicConfig(level=logging.INFO
                    )


# app = Flask(__name__)
# socketio = SocketIO(app)
# app.register_blueprint(excute_raw_app, url_prefix='/execute_raw')
# app.register_blueprint(steampipe_app, url_prefix='/steampipe')
# app.register_blueprint(socket_user_query,url_prefix='/socket')
from app import create_app, socketio

app = create_app(debug=True)

if __name__ == '__main__':
    socketio.run(app)