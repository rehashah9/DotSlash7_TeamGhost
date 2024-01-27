from flask import session,request, Blueprint, jsonify
from flask_socketio import emit, join_room, leave_room
import re
from uuid import uuid4
from ..helpers.steampipe import steampipe
from .. import socketio
from ..helpers.database.db import main_db
from sqlalchemy import create_engine, MetaData, Table, select, update, insert
from . import routes
import json

route_connection = Blueprint('route_connection', __name__)



@routes.route('/connection', methods=['POST'])
def handle_config():
    data = request.get_json()

    try:
        user_id = data['user_id']

        # user_table = main_db.metadata.tables['user']
        connection_table = main_db.metadata.tables['connection']
        engine = main_db.engine
    
        insert_query = (
            insert(connection_table)
            .values(
                connection_data=data['connection_data'], 
                connection_plugin=data['connection_plugin'], 
                connection_name=data['connection_name'],
                user_id=user_id
            )
        )

        with engine.connect() as connection:
            result = connection.execute(insert_query)
            connection.commit()


        steampipe.create_connection()
        
        
        return {'status': 'success', 'message': 'Profile updated successfully'}
    
    # Check Exception for Unique Constraint Violation (Duplicate Entry)
    except Exception as e:
        print(e)
        return {'status': 'error', 'message': 'Profile update failed'}


@routes.route('/connection', methods=['GET'])
def handle_config_get():
    try:
        user_id = request.args.get('organization_id')

        connection_table = main_db.metadata.tables['connection']
        engine = main_db.engine

        select_query = connection_table.select().where(connection_table.c.user_id == user_id)


        with engine.connect() as conn:
            result = conn.execute(select_query)
            connections_db = result.fetchall()

        connections = []

        for x in connections_db:
            connection = {
                'id': x[0],
                'name': x[4],
                # 'connection_data': x[3],
                'connection_plugin': x[2],
                'user_id': x[1]
            }

            connections.append(connection)

        return {'status': 'success', 'message': 'Profile updated successfully', 'data': connections}
    
    # Check Exception for Unique Constraint Violation (Duplicate Entry)
    except Exception as e:
        print(e)
        return {'status': 'error', 'message': 'Profile update failed'}