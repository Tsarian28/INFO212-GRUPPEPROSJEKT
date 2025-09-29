'''
gui/questionnaire_gui.py

Class: QuestionnaireGUI

Methods:

build_ui() → show questions (from logic.questionnaire.Questionnaire).

on_submit() → send answers to logic.training_plan.generate_from_questionnaire().

Display routine in RoutineGUI.
'''
import tkinter as tk


class QuestionnaireGUI:
    """
    A placeholder class for the questionnaire GUI.
    This will handle the questionnaire interface.
    """

    def __init__(self, root, questions, on_submit):
        """
        Initialize the Questionnaire GUI.

        Args:
            root (tk.Tk): The root Tkinter window.
            questions (list): A list of questions to display.
            on_submit (function): A callback function to handle the answers.
        """
        self.root = root
        self.questions = questions
        self.on_submit = on_submit
        self.answers = {}
        self._create_widgets()

    def _create_widgets(self):
        """
        Create and display the questionnaire widgets.
        """
        for idx, question in enumerate(self.questions):
            label = tk.Label(self.root, text=question["question"])
            label.grid(row=idx, column=0, padx=10, pady=5)
            entry = tk.Entry(self.root)
            entry.grid(row=idx, column=1, padx=10, pady=5)
            self.answers[question["key"]] = entry

        submit_button = tk.Button(self.root, text="Submit", command=self._handle_submit)
        submit_button.grid(row=len(self.questions), column=0, columnspan=2, pady=10)

    def _handle_submit(self):
        """
        Handle the submission of answers.
        """
        answers = {key: entry.get() for key, entry in self.answers.items()}
        self.on_submit(answers)