'''
gui/questionnaire_gui.py

Class: QuestionnaireGUI

Methods:

build_ui() → show questions (from logic.questionnaire.Questionnaire).

on_submit() → send answers to logic.training_plan.generate_from_questionnaire().

Display routine in RoutineGUI.
'''
import tkinter as tk
from tkinter import messagebox


class QuestionnaireGUI(tk.Frame):
    def __init__(self, parent, questions, on_submit):
        super().__init__(parent)
        self.questions = questions
        self.on_submit = on_submit
        self.answers = {}
        self._create_widgets()

    def _create_widgets(self):
        tk.Label(self, text="Spørsmål til treningsplanleggeren",
                 font=("Arial", 14, "bold")).pack(pady=10)

        for q in self.questions:
            tk.Label(self, text=q["text"]).pack(anchor="w", padx=10, pady=5)

            if q["type"] == "radio":
                var = tk.StringVar(value=q["default"])
                for option in q["options"]:
                    tk.Radiobutton(self, text=option, variable=var,
                                   value=option).pack(anchor="w", padx=20)
                self.answers[q["key"]] = var

            elif q["type"] == "entry":
                entry = tk.Entry(self)
                entry.insert(0, q["default"])
                entry.pack(anchor="w", padx=20)
                self.answers[q["key"]] = entry

        tk.Button(self, text="Send inn svar",
                  command=self._handle_submit).pack(pady=10)

    def _handle_submit(self):
        results = {}
        for key, widget in self.answers.items():
            if isinstance(widget, tk.StringVar):
                results[key] = widget.get()
            else:
                results[key] = widget.get()

        # Call back to whoever created the questionnaire
        self.on_submit(results)

        messagebox.showinfo("Svar registrert", f"Takk for svarene!\n\n{results}")
