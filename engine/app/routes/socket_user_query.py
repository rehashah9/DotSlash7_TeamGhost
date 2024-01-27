from flask import session,request
from flask_socketio import emit, join_room, leave_room
import re
from .. import socketio
from uuid import uuid4
from app.helpers.steampipe import steampipe
from ai.query_builder.aws_query_builder import aws_query_builder
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    session['user_id'] = str(uuid4())
    emit('status', {'msg': session.get('user_id') + ' has connected.'})


@socketio.on('user_query')
def joined(data):
    user_query = data.get('query')
    user_query_service = data.get('service')

    steampipe_sql_query = aws_query_builder[user_query_service].query(user_query)
    variables = {
        "connection_name": request.headers["Auth"]
    }

    formatted_query = re.sub(r"{{(.*?)}}", lambda x: variables.get(x.group(1), x.group(0)), steampipe_sql_query)

    steampipe_output = steampipe.execute_cli(formatted_query)
    open("steampipe_output.txt", "w").write(steampipe_output)
    print(steampipe_output)
    emit('user_query_status', {'user_query': user_query})










@socketio.on('send_text_in_chunks')
def handle_send_text_in_chunks(data):
    text_to_send = "Hellllllllllooooooooo"
    chunk_size = data.get('chunk_size', 1)

    for i in range(0, len(text_to_send), chunk_size):
        chunk = text_to_send[i:i + chunk_size]
        socketio.emit('receive_text_chunk', {'chunk': chunk})


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)


@socketio.on('disconnect')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('user_id') + ' has disconnected.'}, room=room)
