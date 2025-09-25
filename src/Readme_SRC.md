Main source code for your program.

main.py
- Entry point of the app.
- Should only handle starting the program and calling the GUI (e.g. from gui.main_window import run_app).


# GUI (Graphical User Interface)

This folder contains everything related to the program's interface.

- `main_window.py` → Launches the main GUI window.
- `components.py` → Holds reusable UI components (buttons, forms, layouts).
- `dialogs.py` → Optional dialogs/popups (e.g. settings, about).
- `__init__.py` → Marks this folder as a Python package.

The GUI **only handles display and user interaction**. Any logic/calculations should be placed in `logic/` or `utils/`.

# Utils (Helper Functions)

This folder contains small helper utilities that can be reused across the project.

- `helpers.py` → General-purpose helper functions such as:
  - File handling (load/save data)
  - Formatting strings, dates, numbers
  - Input validation

Utils **should not depend on GUI code**. They are general and reusable.

# Logic (Core Functionality)

This folder contains the **core logic** of the training program.  
The logic is separate from the GUI so the program’s rules and calculations can be tested and reused independently.

### Example files:
- `training.py` → Functions and classes that generate or update training plans.
- `data_manager.py` → Handles saving and loading program data (e.g., JSON, CSV, database).
- `stats.py` → Calculates statistics, progress tracking, or reports.

### Guidelines:
- Logic files should **not contain any GUI code**.
- The GUI (`src/gui/`) calls these functions and displays the results.
- Keeping logic separate makes it easier to test, debug, and extend.
