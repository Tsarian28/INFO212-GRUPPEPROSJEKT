# INFO212 Treningsapp Final:

## Important Information for Grader

We have two branches that were expanded upon in Sprint 3:  
- `feature/hjem-cards-forbedring`  
- `adrian/progressbar`

During this sprint our priority got a little sidetracked, as we had a hiccup in the design of our project. The home page that has the inlogging could also be used to generate a plan; however, we decided to redesign these instead of fixing the bugs of the calendar, which would align more with the user stories we had. Because of this, our priority ranking and sprint were not as thorough as we would’ve liked them to be.

We also didn’t plan enough to combine the two branches to have a working final, thrown-together branch. In the weeks following the exam and during the winter vacation, we want to continue working on this project and making it into a workout generation plan that has no bugs and a better design.

Overall, this course has been very helpful in learning more about how to use GIT and planning and scheduling a plan for a group programming project.


A Flask web app for planning, generating, and logging workouts with a built-in calendar.

---

## Setup

```bash
git clone https://github.com/Tsarian28/INFO212-GRUPPEPROSJEKT.git
cd INFO212-GRUPPEPROSJEKT
python -m venv .venv
source .venv/bin/activate        # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
python app.py
```
## usage
Create a new user (username + password).
Add or generate workouts.
Try Weekly Plan to build a full program.
Open Calendar to view and schedule sessions.
Log out when done.

## structure:
- app.py                 # main Flask app
- models.py              # database helpers
- plan_logic.py          # smart training plan generator
- templates/             # HTML templates
- static/                # CSS and images
- instance/app.db        # auto-created local database

## Notes
The database is created automatically in /instance.
Delete instance/ to reset.
Run locally only; debug mode is on by default.

