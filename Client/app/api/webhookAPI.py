import socketio
import threading



class SocketClient:
    def __init__(self, gui, group_id, password, username, create_group=False):
        self.sio = socketio.Client()
        self.gui = gui
        self.group_id = group_id
        self.password = password
        self.username = username
        self.create_group = create_group

        @self.sio.event
        def connect():
            if self.create_group:
                self.sio.emit('create_group', {
                    'ID': self.group_id,
                    'pass': self.password
                })
            # Join group after connecting
            self.sio.emit('join_group', {
                'ID': self.group_id,
                'pass': self.password,
                'username': self.username
            })

        @self.sio.on('receive_message')
        def on_receive_message(msg):
            # msg can be a list (on join) or dict (on new message)
            if isinstance(msg, list):
                for m in msg:
                    self.gui.add_new_item(f"{m['user']}: {m['message']}")
            elif isinstance(msg, dict):
                self.gui.add_new_item(f"{msg['user']}: {msg['message']}")

        @self.sio.on('group_join_status')
        def on_join_status(status):
            if not status:
                self.gui.add_new_item("Failed to join group (wrong password or group does not exist)")

        @self.sio.on('group_create_status')
        def on_create_status(status):
            if status:
                ServerHostGUI(self.group_id, self.password)
                self.gui.add_new_item("Group created successfully!")
            else:
                self.gui.add_new_item("Group already exists.")

        @self.sio.event
        def disconnect():
            self.gui.add_new_item("Disconnected from server.")

        # Connect to server (force websocket transport)
        threading.Thread(
            target=lambda: self.sio.connect(
                'https://openmsgr.onrender.com/',
                transports=['websocket']
            ),
            daemon=True
        ).start()

    def send_message(self, message):
        self.sio.emit('send_message', {
            'ID': self.group_id,
            'pass': self.password,
            'username': self.username,
            'message': message
        })

    def disconnect(self):
        self.sio.disconnect()
        