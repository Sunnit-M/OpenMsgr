import tkinter as tk
from tkinter import ttk

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

        # Pass create_group to SocketClient
        self.socket_client = SocketClient(self, self.group_id, self.password, self.username, create_group=create_group)

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