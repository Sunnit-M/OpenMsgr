import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import socketio
import threading

# --- Socket.IO Client Setup ---
class SocketClient:
    def __init__(self, gui, group_id, password, username):
        self.sio = socketio.Client()
        self.gui = gui
        self.group_id = group_id
        self.password = password
        self.username = username

        @self.sio.event
        def connect():
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
                self.gui.add_new_item("Group created successfully!")
            else:
                self.gui.add_new_item("Group already exists.")

        @self.sio.event
        def disconnect():
            self.gui.add_new_item("Disconnected from server.")

        # Connect to server (change URL if needed)
        threading.Thread(target=lambda: self.sio.connect('http://localhost:5000'), daemon=True).start()

    def send_message(self, message):
        self.sio.emit('send_message', {
            'ID': self.group_id,
            'pass': self.password,
            'username': self.username,
            'message': message
        })

    def disconnect(self):
        self.sio.disconnect()

# --- GUI for Messages ---
class MessagesGUI:
    def __init__(self, data, create_group=False):
        self.username = data.get('username', '')
        self.group_id = data.get('IP', '')
        self.password = str(data.get('port', ''))
        self.root = tk.Tk()
        self.root.config(background='lightgrey')
        self.root.title("Messages")
        self.root.geometry("500x600")

        header = tk.Label(self.root, text="Messages", font=("Arial", 16, "bold"), bg="lightgrey", fg="black")
        header.pack(pady=10)

        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(self.frame, bg="white", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scroll = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scroll.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.scrollFrame = ttk.Frame(self.canvas)
        self.canvas.create_window(0, 0, window=self.scrollFrame, anchor="nw")

        self.Entry_Message = tk.Entry(self.root, font=("Arial", 12), justify="left")
        self.Entry_Message.pack(fill="x", padx=20, pady=10)

        self.add_button = tk.Button(self.root, text="Send", font=("Arial", 12), bg="blue", fg="white",
                                    command=self.send_message)
        self.add_button.pack(pady=10)

        self.running = True

        # Socket.IO client
        self.socket_client = SocketClient(self, self.group_id, self.password, self.username)

        # If creating a group, emit create_group event
        if create_group:
            self.socket_client.sio.emit('create_group', {
                'ID': self.group_id,
                'pass': self.password
            })

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def add_new_item(self, text):
        new_label = tk.Label(
            self.scrollFrame,
            text=text,
            font=("Arial", 16),
            bg="white",
            anchor="w",
            wraplength=self.canvas.winfo_width() - 20
        )
        new_label.pack(pady=5, fill="x", padx=10)
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.yview_moveto(1.0)

    def send_message(self):
        message = self.Entry_Message.get()
        if message.strip():
            self.socket_client.send_message(message)
            self.Entry_Message.delete(0, tk.END)

    def on_close(self):
        self.running = False
        self.socket_client.disconnect()
        self.root.destroy()

# ---------- Menu and Info ----------
class Menu:
    def __init__(self):
        self.root = tk.Tk()
        self.root.config(background='lightgrey')
        self.root.title("OpenMsgr Main")
        self.root.geometry("300x300")
        self.userName = tk.StringVar()

        self.Label_Name = tk.Label(self.root, text="Enter Your Name:", font=("Arial", 14), bg="lightgrey")
        self.Label_Name.pack(pady=10)
        self.Entry_Name = tk.Entry(self.root, font=("Arial", 12), justify="center", textvariable=self.userName)
        self.Entry_Name.pack(fill="x", padx=20, pady=10)
        self.Entry_Name.insert(0, "Insert Name Here")
        self.Entry_Name.bind("<FocusIn>", self.OnNameEntryClicked)

        self.Button_CreateGroup = tk.Button(self.root, text="Create Group", font=("Arial", 12), bg="blue", fg="white",
                                            command=self.CreateServer_Clicked)
        self.Button_CreateGroup.pack(fill="x", padx=20, pady=10)

        self.Button_JoinGroup = tk.Button(self.root, text="Join Group", font=("Arial", 12), bg="green", fg="white",
                                          command=self.JoinServer_Clicked)
        self.Button_JoinGroup.pack(fill="x", padx=20, pady=10)

        self.root.mainloop()

    def CreateServer_Clicked(self):
        if (self.userName.get() == "Insert Name Here" or self.userName.get() == ""):
            self.Entry_Name.configure(fg="red")
            return
        ServerInfoBox(self.CreateGroup, self.userName.get())

    def JoinServer_Clicked(self):
        if (self.userName.get() == "Insert Name Here" or self.userName.get() == ""):
            self.Entry_Name.configure(fg="red")
            return
        ServerInfoBox(self.ConnectToServer, self.userName.get())

    def ConnectToServer(self, data):
        # Join existing group
        MessagesGUI(data, create_group=False)

    def OnNameEntryClicked(self, event):
        self.Entry_Name.configure(fg="black")
        self.Entry_Name.delete(0, tk.END)

    def CreateGroup(self, data):
        # Create a new group
        MessagesGUI(data, create_group=True)

class ServerInfoBox:
    def __init__(self, callback, username=""):
        self.username = username
        self.callback = callback
        self.root = tk.Tk()
        self.root.config(background='lightgrey')
        self.root.title("Server InfoBox")
        self.root.geometry("400x400")
        tk.Label(self.root, text="Group ID:", font=("Arial", 14), bg="lightgrey").pack(pady=10)
        self.Entry_GroupID = tk.Entry(self.root, font=("Arial", 14), justify="left")
        self.Entry_GroupID.pack(fill="x", padx=20, pady=5)
        tk.Label(self.root, text="Password:", font=("Arial", 14), bg="lightgrey").pack(pady=10)
        self.Entry_Pass = tk.Entry(self.root, font=("Arial", 14), justify="left", fg="white")
        self.Entry_Pass.pack(fill="x", padx=20, pady=5)

        self.ConnectButton = tk.Button(self.root, text="Confirm", font=("Arial", 14), bg="green", fg="white",
                                       command=self.Confirm)
        self.ConnectButton.pack(pady=20)
        self.root.mainloop()

    def Confirm(self):
        if (not self.Entry_Pass.get().isdigit()):
            return

        data = {
            "username": self.username,
            "IP": self.Entry_GroupID.get(),
            "port": int(self.Entry_Pass.get())
        }

        self.root.destroy()
        self.callback(data)

class ServerHostGUI:
    def __init__(self, IP, Port):
        self.root = tk.Tk()
        self.root.config(background='lightgrey')
        self.root.title(f"Server Hosted On IP: {IP} Port: {Port}")
        self.root.geometry("400x300")
        tk.Label(self.root, text="Server Information", font=("Arial", 16, "bold"), bg="lightgrey").pack(pady=10)
        tk.Label(self.root, text=f"IP Address: {IP}", font=("Arial", 12), bg="lightgrey").pack(pady=5)
        tk.Label(self.root, text=f"Port: {Port}", font=("Arial", 12), bg="lightgrey").pack(pady=5)
        import socket
        tk.Label(self.root, text=f"Hostname: {socket.gethostname()}", font=("Arial", 12), bg="lightgrey").pack(pady=5)
        tk.Label(self.root, text="Instructions:", font=("Arial", 14, "bold"), bg="lightgrey").pack(pady=10)
        tk.Label(
            self.root,
            text="The server is running. You can now send and receive messages.\n"
                 "Close this window to stop the server.",
            font=("Arial", 12),
            bg="lightgrey",
            wraplength=350,
            justify="center"
        ).pack(pady=10)
        self.root.mainloop()

if __name__ == "__main__":
    Menu()