'''
Class: LoginGUI

Methods:

build_ui() → renders login + create user form.

on_login() → calls logic.users.authenticate().

on_register() → calls logic.users.create_user().

Emits: success event → tells app to switch to MainPageGUI.

'''

import tkinter as tk
from logic.users import UserManager

class LoginGUI:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success  # callback to App
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        tk.Label(self.frame, text="Username").pack()
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.pack()

        tk.Label(self.frame, text="Password").pack()
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.pack()

        tk.Button(self.frame, text="Login", command=self.on_login).pack()
        tk.Button(self.frame, text="Register", command=self.on_register).pack()

    def on_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if UserManager.authenticate(username, password):
            self.on_success(username)  # let App handle switching
        else:
            tk.Label(self.frame, text="Invalid login!", fg="red").pack()

    def on_register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if UserManager.create_user(username, password):
            tk.Label(self.frame, text="User created! Please log in.", fg="green").pack()
        else:
            tk.Label(self.frame, text="Username already exists!", fg="red").pack()
