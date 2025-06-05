import tkinter as tk
from tkinter import simpledialog

class Menu:
    def __init__(self):
        # fix the callback type to be a function that takes no arguments
        self.CreateServer_Callback :callable = None
        self.JoinServer_Callback :callable = None
        
        
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
        
        self.CreateServer_Callback()

    def JoinServer_Clicked(self):
        if (self.userName.get() == "Insert Name Here" or self.userName.get() == ""):
            self.Entry_Name.configure(fg="red")
            return
        
        self.JoinServer_Callback()


    def OnNameEntryClicked(self, event):
        self.Entry_Name.configure(fg="black")
        self.Entry_Name.delete(0, tk.END)
