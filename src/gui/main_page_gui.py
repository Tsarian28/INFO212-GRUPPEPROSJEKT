'''
Class MainPageGUI
Organizes set up of app window and set up of tabs 

'''


import tkinter as tk
from tkinter import ttk
from gui.tabs_gui import WelcomeTab, ChecklistTab, ProgressTab, WorkoutsTab


class MainPageGUI:
    def __init__(self, root, username, on_logout):
        self.root = root
        self.username = username
        self.on_logout = on_logout

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)

        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill="both", expand=True)

        # Build all tabs
        WelcomeTab(self.notebook, self.username)
        ChecklistTab(self.notebook)
        ProgressTab(self.notebook)
        WorkoutsTab(self.notebook, self.username)

        tk.Button(self.frame, text="Logout", command=self.logout).pack(pady=10)

    def logout(self):
        self.frame.destroy()
        self.on_logout()
