from __future__ import annotations
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from wtforms import StringField, IntegerField, TextAreaField, SelectField, PasswordField
from wtforms.validators import DataRequired, NumberRange, Length
from flask_wtf import FlaskForm
import json, os
import models
from plan_logic import generate_plan

app = Flask(__name__)
app.config.update(SECRET_KEY="change-me-please")

os.makedirs("instance", exist_ok=True)
with app.app_context():
    models.init_db()

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, row):
        self.id = row["id"]
        self.username = row["username"]
        self.password_hash = row["password_hash"]
    @staticmethod
    def from_username(username: str):
        row = models.user_get_by_username(username)
        return User(row) if row else None
    @staticmethod
    def from_id(user_id: int):
        row = models.user_get(user_id)
        return User(row) if row else None

@login_manager.user_loader
def load_user(user_id):
    return User.from_id(int(user_id))

class WorkoutForm(FlaskForm):
    name = StringField("Navn", validators=[DataRequired(), Length(max=100)])
    sets = IntegerField("Sett", validators=[DataRequired(), NumberRange(min=1, max=100)])
    duration_min = IntegerField("Varighet (min)", validators=[DataRequired(), NumberRange(min=1, max=600)])
    notes = TextAreaField("Notater", validators=[Length(max=500)])

class LoginForm(FlaskForm):
    username = StringField("Brukernavn", validators=[DataRequired(), Length(max=50)])
    password = PasswordField("Passord", validators=[DataRequired(), Length(min=3, max=200)])

class QuizForm(FlaskForm):
    goal = SelectField("Mål", choices=[("hypertrofi","Hypertrofi"),("styrke","Styrke"),("spenst","Spenst"),("utholdenhet","Utholdenhet")], validators=[DataRequired()])
    level = SelectField("Nivå", choices=[("nybegynner","Nybegynner"),("middels","Middels"),("avansert","Avansert")], validators=[DataRequired()])
    gear = SelectField("Utstyr", choices=[("fullt_gym","Fullt gym"),("kroppsvekt","Kroppsvekt"),("hjemme_enkle","Hjemme – enkle")], validators=[DataRequired()])

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/workouts")
@login_required
def workouts():
    form = WorkoutForm()
    workouts = models.workout_list(current_user.id)
    stats = models.workout_stats(current_user.id)
    quiz = QuizForm()
    return render_template("index.html", form=form, workouts=workouts, stats=stats, quiz=quiz)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data
        existing = models.user_get_by_username(username)
        if existing:
            user = User(existing)
            if bcrypt.check_password_hash(user.password_hash, password):
                login_user(user)
                return redirect(url_for("workouts"))
            else:
                flash("Feil passord", "error")
        else:
            pw_hash = bcrypt.generate_password_hash(password).decode()
            uid = models.user_create(username, pw_hash)
            login_user(User.from_id(uid))
            return redirect(url_for("workouts"))
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/workouts/create", methods=["POST"])
@login_required
def create_workout():
    form = WorkoutForm()
    ex_json = request.form.get("exercises_json", "[]")
    try:
        exercises = json.loads(ex_json)
        if not isinstance(exercises, list):
            exercises = []
    except Exception:
        exercises = []
    if form.validate_on_submit():
        models.workout_create(
            current_user.id,
            form.name.data,
            form.sets.data,
            form.duration_min.data,
            form.notes.data or None,
            exercises=exercises
        )
    workouts = models.workout_list(current_user.id)
    return render_template("workouts_list.html", workouts=workouts)

@app.route("/workouts/delete", methods=["POST"])
@login_required
def delete_workout():
    wid = int(request.form.get("workout_id", "0"))
    models.workout_delete(current_user.id, wid)
    workouts = models.workout_list(current_user.id)
    return render_template("workouts_list.html", workouts=workouts)

@app.route("/stats")
@login_required
def stats_partial():
    stats = models.workout_stats(current_user.id)
    return render_template("_stats.html", stats=stats)

@app.route("/questionnaire", methods=["POST"])
@login_required
def questionnaire():
    goal = request.form.get("goal","hypertrofi")
    level = request.form.get("level","nybegynner")
    gear = request.form.get("gear","fullt_gym")
    plan = generate_plan(goal, level, gear)
    return render_template("_plan_result.html", plan=plan, goal=goal, level=level, gear=gear)

if __name__ == "__main__":
    app.run(debug=True)
