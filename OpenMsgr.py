import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog


class MessagesGUI:
    def __init__(self, data):
        self.username = data.get('username', '')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((data["IP"], data["port"]))

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

        self.add_button = tk.Button(self.root, text="Send", font=("Arial", 12), bg="blue", fg="white", command=self.send_message)
        self.add_button.pack(pady=10)

        self.running = True

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
        message = self.username + ": " + message
        if message.strip():
            self.socket.sendall(message.encode())
            self.add_new_item(message)  # Show your own message instantly
            self.Entry_Message.delete(0, tk.END)


    def on_close(self):
        self.running = False
        self.socket.close()
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
        self.Entry_Name.bind("<FocusIn>",self.OnNameEntryClicked)

        self.Button_CreateGroup = tk.Button(self.root, text="Create Group", font=("Arial", 12), bg="blue", fg="white", command=self.CreateServer_Clicked)
        self.Button_CreateGroup.pack(fill="x", padx=20, pady=10)

        self.Button_JoinGroup = tk.Button(self.root, text="Join Group", font=("Arial", 12), bg="green", fg="white", command=self.JoinServer_Clicked)
        self.Button_JoinGroup.pack(fill="x", padx=20, pady=10)

        self.root.mainloop()

    def CreateServer_Clicked(self):
        if(self.userName.get() == "Insert Name Here" or self.userName.get() == ""):
            self.Entry_Name.configure(fg="red")
            return
        ServerInfoBox(self.CreateSocketServer, self.userName.get())

    def JoinServer_Clicked(self):
        if(self.userName.get() == "Insert Name Here" or self.userName.get() == ""):
            self.Entry_Name.configure(fg="red")
            return
        ServerInfoBox(self.ConnectToServer, self.userName.get())

    def ConnectToServer(self, data):
        MessagesGUI(data)

    def OnNameEntryClicked(self,event):
        self.Entry_Name.configure(fg="black")
        self.Entry_Name.delete(0,tk.END)


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

        self.ConnectButton = tk.Button(self.root, text="Confirm", font=("Arial", 14), bg="green", fg="white", command=self.Confirm)
        self.ConnectButton.pack(pady=20)
        self.root.mainloop()

    def Confirm(self):
        if(not self.Entry_Pass.get().isdigit()):
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