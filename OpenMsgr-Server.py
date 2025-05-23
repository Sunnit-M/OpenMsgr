from flask import Flask, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = "KEY"

socketio = SocketIO(app, cors_allowed_origins="*")

groups = {}

@socketio.on('connect')
def handle_connect():
    print("Client connected")
    send("Connected to server")

@socketio.on('create_group')
def group_create(data):
    group_id = data['ID']
    password = data['pass']

    if group_id in groups:
        emit('group_create_staus',False)

    else:
        groups[group_id] = {'password': password, 'messages':[], 'users': []}
        emit('group_create_status',True)

@socketio.on('join_group')
def group_join(data):
    group_id = data['ID']
    password = data['pass']
    username = data['username']

    if group_id in groups:
        if groups[group_id]['password'] == password:
            groups[group_id]['users'].append(username)
            join_room(group_id)
            emit('group_join_status', True)
            emit('receive_message', groups[group_id]['messages'], room=group_id)
        else:
            emit('group_join_status', False)

@socketio.on('send_message')
def send_message(data):
    group_id = data['ID']
    password = data['pass']
    message = data['message']
    username = data['username']

    if group_id in groups:
        if groups[group_id]['password'] == password:
            groups[group_id]['messages'].append({'user': username, 'message': message})
            emit('receive_message', {'user': username, 'message': message}, room=group_id)
        else:
            emit('send_message_status', False)




