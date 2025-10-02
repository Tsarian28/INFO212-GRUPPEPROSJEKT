'''
The tabs class file that organizes what each tab on the main page should be
Future implementation:
- for each subtab, have a separate file with other tabs on the page for organization purposes
'''

import tkinter as tk
from tkinter import ttk
from logic.users import UserManager
from logic.questionnaire import Questionnaire
from gui.questionnaire_gui import QuestionnaireGUI
import json
from tkinter import simpledialog

class WelcomeTab:
    def __init__(self, notebook, username):
        tab = tk.Frame(notebook)

        try:
            photo = tk.PhotoImage(file="icon.png")
            label = tk.Label(
                tab,
                text=f"Velkommen til Treningsappen, {username}",
                image=photo,
                compound="bottom",
                font=("Arial", 16, "bold")
            )
            label.image = photo
        except Exception:
            label = tk.Label(
                tab,
                text=f"Velkommen til Treningsappen, {username}",
                font=("Arial", 16, "bold")
            )
        label.pack(pady=20)

        tk.Label(tab, text="Bruk fanene øverst for å navigere").pack()

        notebook.add(tab, text="Velkommen")


class ChecklistTab:
    def __init__(self, notebook):
        tab = tk.Frame(notebook)

        tk.Label(tab, text="Hvilke dager har du trent?",
                 font=("Arial", 14, "bold")).pack(pady=10)

        self.vars = {}
        self.days = ["Mandag", "Tirsdag", "Onsdag",
                     "Torsdag", "Fredag", "Lørdag", "Søndag"]

        for d in self.days:
            v = tk.BooleanVar()
            self.vars[d] = v
            tk.Checkbutton(tab, text=d, variable=v,
                           anchor="w").pack(anchor="w", padx=20)

        tk.Button(tab, text="Vis i konsoll",
                  command=self.print_selected).pack(pady=10)

        notebook.add(tab, text="Sjekkliste")

    def print_selected(self):
        print("Valgte dager:")
        for d in self.days:
            print(f"{d}: {'✅' if self.vars[d].get() else '—'}")


class ProgressTab:
    def __init__(self, notebook):
        tab = tk.Frame(notebook)

        tk.Label(tab, text="Her kan du se progresjon fra økt til økt",
                 font=("Arial", 14, "bold")).pack(pady=10)

        pb = ttk.Progressbar(tab, orient="horizontal",
                             mode="determinate", length=280)
        pb.pack(pady=20)

        notebook.add(tab, text="Progresjon")


class WorkoutsTab:
    def __init__(self, notebook, username):
        self.username = username
        self.tab = tk.Frame(notebook)

        # Scrollable canvas setup
        self.canvas = tk.Canvas(self.tab)
        self.scrollbar = tk.Scrollbar(self.tab, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # 🔑 Separate frames
        self.questionnaire_frame = tk.Frame(self.scrollable_frame)
        self.questionnaire_frame.pack(fill="x", pady=5)

        self.workouts_frame = tk.Frame(self.scrollable_frame)
        self.workouts_frame.pack(fill="both", expand=True, pady=10)

        # Button to create new workout (opens questionnaire)
        tk.Button(self.tab, text="Create Workout Plan",
                  command=self.create_workout).pack(pady=10)

        # Add tab to notebook
        notebook.add(self.tab, text="Workouts")

        # Show saved workouts initially
        self.display_workouts()

    def display_workouts(self):
        """Show all saved workouts for this user, nicely formatted."""
        for widget in self.workouts_frame.winfo_children():
            widget.destroy()

        workouts = UserManager.get_workouts(self.username)
        if workouts:
            tk.Label(self.workouts_frame, text="Your Workout Plans:",
                     font=("Arial", 14, "bold")).pack(pady=5)

            for w in workouts:
                frame = tk.Frame(self.workouts_frame, relief="groove", borderwidth=2, padx=10, pady=5)
                frame.pack(fill="x", padx=10, pady=5)

                tk.Label(frame, text=w["name"], font=("Arial", 12, "bold")).pack(anchor="w")

                try:
                    answers = json.loads(w["plan"])
                    for key, value in answers.items():
                        tk.Label(frame, text=f"- {key}: {value}").pack(anchor="w")
                except Exception:
                    tk.Label(frame, text=w["plan"]).pack(anchor="w")
        else:
            tk.Label(self.workouts_frame, text="No saved workouts yet.").pack()

    def create_workout(self):
        """Show questionnaire in its own frame (separate from workouts list)."""
        for widget in self.questionnaire_frame.winfo_children():
            widget.destroy()

        questions = Questionnaire().get_questions()
        questionnaire = QuestionnaireGUI(
            self.questionnaire_frame,
            questions,
            self._save_workout  # callback when submitted
        )
        questionnaire.pack(fill="both", expand=True, padx=10, pady=10)

    def _save_workout(self, answers):
        workout_name = simpledialog.askstring("Workout Name", "Gi et navn til treningsplanen din:")
        if not workout_name:
            workout_name = f"Workout {len(UserManager.get_workouts(self.username)) + 1}"

        plan_json = json.dumps(answers, ensure_ascii=False)
        UserManager.add_workout(self.username, workout_name, plan_json)

        # 🔑 Clear questionnaire frame
        for widget in self.questionnaire_frame.winfo_children():
            widget.destroy()

        # Refresh workouts list
        self.display_workouts()
