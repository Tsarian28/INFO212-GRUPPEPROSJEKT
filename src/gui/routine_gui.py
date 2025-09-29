'''
Class: RoutineGUI

Methods:

build_ui(routines) → show the options (list, buttons, etc.).
'''
import tkinter as tk

class RoutineGUI:
    """
    A placeholder class for displaying workout routines.
    """

    def __init__(self, root, routines, on_exit):
        """
        Initialize the Routine GUI.

        Args:
            root (tk.Tk): The root Tkinter window.
            routines (list): A list of workout routines to display.
            on_exit (function): A callback to return to the main page.
        """
        self.root = root
        self.routines = routines or ["Prototype routine 1", "Prototype routine 2"]
        self.on_exit = on_exit
        self._create_widgets()

    def _create_widgets(self):
        """
        Create and display the routine widgets.
        """
        label = tk.Label(self.root, text="Here are your workout routines:")
        label.pack(pady=10)

        for routine in self.routines:
            tk.Label(self.root, text=routine).pack()

        exit_button = tk.Button(self.root, text="Back to Main Page", command=self.on_exit)
        exit_button.pack(pady=10)
