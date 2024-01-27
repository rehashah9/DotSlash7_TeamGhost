from flask import Blueprint

routes = Blueprint('routes', __name__)

from . import route_steampipe, socket_user_query,route_execute_raw, route_connection