# INFO212-GRUPPEPROSJEKT

# 🏋️ Training Planner – INFO212  

A Tkinter-based training planner where users can:  
- Log in / register  
- Track training days & progress  
- Create workout plans via a questionnaire  
- Save workouts with names to a SQLite database  
- View saved workouts in a scrollable tab  

---

## 🚦 Developer Guide – How to Add or Update Features  

When extending the app, follow these steps so everything still works:  

1. **Update the logic first (if needed)**  
   - Add/change data handling in `src/logic/`.  
   - Example: adding a new questionnaire question → update `logic/questionnaire.py`.  
   - If the database needs new columns → update `UserManager.init_db()` and reset/migrate `users.db`.  

2. **Update the GUI layer**  
   - Display changes in `src/gui/`.  
   - Add a new tab → create a new class in `tabs_gui.py` and hook it in `main_page_gui.py`.  
   - Add a new questionnaire question → make sure `questionnaire.py` (logic) and `questionnaire_gui.py` (display) are in sync.  

3. **Keep responsibilities separate**  
   - `src/gui/` → only handles display and user interaction.  
   - `src/logic/` → rules, calculations, database.  
   - `src/utils/` → generic helpers, no GUI or DB code.  

4. **Always run the app from the project root**  
   ```bash
   python3 src/main.py

5. **Check database schema after changes**
    in terminal: sqlite3 users.db ".schema workouts"


## 🗂️ Project Structure

### Main Entry
- `src/main.py` → Starts the program, calls `UserManager.init_db()`, launches login flow.

---

### GUI Layer (`src/gui/`)
Tkinter interface only.

- `login_gui.py` → Login & registration.  
- `main_page_gui.py` → Sets up the Notebook (tabs).  
- `tabs_gui.py` → Contains tab classes:  
  - `WelcomeTab` → greeting  
  - `ChecklistTab` → weekly training checklist  
  - `ProgressTab` → simple progress bar placeholder  
  - `WorkoutsTab` → questionnaire + saved plans (scrollable)  
- `questionnaire_gui.py` → Renders questionnaire (radio buttons + entry).  

---

### Logic Layer (`src/logic/`)
App rules & persistence.

- `users.py` → database manager  
  - `users` table → usernames + hashed passwords  
  - `workouts` table → `(id, username, name, plan)` where `plan` is JSON  
- `questionnaire.py` → defines questionnaire questions.  
- `training_plan.py` → (future expansion) generate workout routines.  

---

### Utils (`src/utils/`)
Generic helpers.

- `helpers.py` → reusable functions for use later
---

## 🔄 Flow Summary
1. `main.py` → runs `UserManager.init_db()` → launches `LoginGUI`.  
2. `LoginGUI` → authenticates user → opens `MainPageGUI`.  
3. `MainPageGUI` → shows 4 tabs: **Welcome, Checklist, Progress, Workouts**.  
4. In **Workouts tab**:  
   - Click **Create Workout Plan** → shows `QuestionnaireGUI`.  
   - Submit → asks for a workout name → saves `(username, name, plan)` in DB.  
   - Questionnaire disappears → saved workouts refresh in a scrollable list.  
5. Data is persisted in `users.db` → plans remain after logout/restart.  

---

## 💾 Data Persistence
Managed entirely by `logic/users.py`:  
- `users` table → stores usernames and SHA-256 hashed passwords.  
- `workouts` table → stores each workout plan (name + JSON answers).  

➡️ The GUI just displays data — it doesn’t own it. Even if you close/restart the app, the database keeps everything.  
