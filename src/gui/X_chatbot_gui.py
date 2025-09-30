'''
gui/chatbot_gui.py

Class: ChatbotGUI

Methods:

build_ui() → simple text chat interface.

on_message() → send user text to logic.chatbot.get_response().

Once done → call logic.training_plan.generate_from_chatbot().
'''
import tkinter as tk

class ChatbotGUI:
    """
    A placeholder class for the chatbot GUI.
    This will handle the chatbot interface.
    """

    def __init__(self, root, on_exit):
        """
        Initialize the Chatbot GUI.

        Args:
            root (tk.Tk): The root Tkinter window.
            on_exit (function): A callback function to return to the main page.
        """
        self.root = root
        self.on_exit = on_exit
        self._create_widgets()

    def _create_widgets(self):
        """
        Create and display the chatbot widgets.
        """
        label = tk.Label(self.root, text="Chatbot functionality will be implemented in the next version.")
        label.pack(pady=20)

        exit_button = tk.Button(self.root, text="Back to Main Page", command=self.on_exit)
        exit_button.pack(pady=10)