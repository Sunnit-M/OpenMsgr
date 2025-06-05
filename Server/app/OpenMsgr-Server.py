from flask import Flask, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import os
import eventlet

eventlet.monkey_patch()

app = Flask(__name__)

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
        print(f"Group creation failed: '{group_id}' already exists.")
        emit('group_create_status', False)
    else:
        groups[group_id] = {'password': password, 'messages': [], 'users': []}
        print(f"Group created: '{group_id}' with password '{password}'")
        emit('group_create_status', True)

@socketio.on('join_group')
def group_join(data):
    group_id = data['ID']
    password = data['pass']
    username = data['username']

    if group_id in groups:
        if groups[group_id]['password'] == password:
            groups[group_id]['users'].append(username)
            join_room(group_id)
            print(f"User '{username}' joined group '{group_id}'")
            emit('group_join_status', True)
            emit('receive_message', groups[group_id]['messages'], room=group_id)
        else:
            print(f"User '{username}' failed to join group '{group_id}': wrong password")
            emit('group_join_status', False)
    else:
        print(f"User '{username}' tried to join non-existent group '{group_id}'")
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
            print(f"Message in '{group_id}' from '{username}': {message}")
            emit('receive_message', {'user': username, 'message': message}, room=group_id)
        else:
            print(f"User '{username}' failed to send message to '{group_id}': wrong password")
            emit('send_message_status', False)
    else:
        print(f"User '{username}' tried to send message to non-existent group '{group_id}'")
        emit('send_message_status', False)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Server starting on 0.0.0.0:{port}")
    socketio.run(app, host="0.0.0.0", port=port)




