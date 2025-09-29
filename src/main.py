import tkinter as tk
from gui.login_gui import LoginGUI
from gui.main_page_gui import MainPageGUI
from logic.users import UserManager

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Workout App")
        self.show_login()

    def show_login(self):
        self.clear_root()
        LoginGUI(self.root, on_success=self.show_main)

    def show_main(self, username):
        self.clear_root()
        MainPageGUI(self.root, username, on_logout=self.show_login)

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    UserManager.init_db()
    App().run()
