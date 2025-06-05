class ServerHostGUI:
    def __init__(self,ID, Port):
        self.root = tk.Tk()
        self.root.config(background='lightgrey')
        self.root.title(f"Group - {ID}")
        self.root.geometry("400x300")
        tk.Label(self.root, text="Server Information", font=("Arial", 16, "bold"), bg="lightgrey").pack(pady=10)
        tk.Label(self.root, text=f"Group ID: {ID}", font=("Arial", 12), bg="lightgrey").pack(pady=5)
    
        self.root.mainloop()