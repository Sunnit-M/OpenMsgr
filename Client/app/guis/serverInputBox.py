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
        self.Censor = tk.Label(self.root, text="", font=("Arial", 18), bg="white")
        self.Censor.pack(side="left", padx=5,in_=self.Entry_Pass)

        self.ConnectButton = tk.Button(self.root, text="Confirm", font=("Arial", 14), bg="green", fg="white",
                                       command=self.Confirm)
        self.ConnectButton.pack(pady=20)
        
        threading.Thread(target=self.Looped, daemon=True).start()
        
        self.root.mainloop()

    def Looped(self):
        while True:
            self.Censor.config(text="*" * len(self.Entry_Pass.get())) 

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
