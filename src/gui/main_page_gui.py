'''
gui/main_page_gui.py

Class: MainPageGUI

Methods:

build_ui() → shows “Create Workout Plan” button.

on_create_workout() → choose Questionnaire or Chatbot → open new GUI window.
'''


import tkinter as tk
from logic.users import UserManager

class MainPageGUI:
    def __init__(self, root, username, on_logout):
        self.root = root
        self.username = username
        self.on_logout = on_logout  # callback to App

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        tk.Label(self.frame, text=f"Welcome, {self.username}!").pack()

        self.workouts_frame = tk.Frame(self.frame)
        self.workouts_frame.pack()
        self.display_workouts()

        tk.Button(self.frame, text="Create Workout Plan", command=self.create_workout).pack()
        tk.Button(self.frame, text="Logout", command=self.logout).pack()

    def display_workouts(self):
        for widget in self.workouts_frame.winfo_children():
            widget.destroy()
        plans = UserManager.get_workouts(self.username)
        if plans:
            tk.Label(self.workouts_frame, text="Your Workout Plans:").pack()
            for i, plan in enumerate(plans, 1):
                tk.Label(self.workouts_frame, text=f"{i}. {plan}").pack()
        else:
            tk.Label(self.workouts_frame, text="No saved workouts yet.").pack()

    def create_workout(self):
        UserManager.add_workout(self.username, "Prototype Full-Body Routine")
        self.display_workouts()

    def logout(self):
        self.on_logout()  # let App handle switching
