## General Rules
- Place display code in `src/gui/`  
- Place app rules and persistence in `src/logic/`  
- Place generic helpers in `src/utils/`  
- Always run the app from the project root:  
  ```bash
  python3 src/main.py


## Project Structure
Main Entry
src/main.py → starts the program, initializes the database, launches login flow

# GUI Layer (src/gui/)
Tkinter interface:
login_gui.py → login and registration
main_page_gui.py → sets up the notebook tabs
tabs_gui.py → contains tab classes (WelcomeTab, ChecklistTab, ProgressTab, WorkoutsTab)
questionnaire_gui.py → renders questionnaire
# Logic Layer (src/logic/)
Application logic and persistence:
users.py → manages database (users and workouts tables)
questionnaire.py → defines questionnaire questions
training_plan.py → future expansion for generating routines
Generic helpers:
# Flow Summary
main.py → initializes DB and launches login GUI
LoginGUI → authenticates user and opens MainPageGUI
MainPageGUI → shows four tabs: Welcome, Checklist, Progress, Workouts
Workouts tab:
Create Workout Plan → opens questionnaire
Submitting asks for a workout name, saves (username, name, plan) in DB
Saved workouts are shown in a scrollable list
All data is stored in users.db and persists across sessions LOCALLY
