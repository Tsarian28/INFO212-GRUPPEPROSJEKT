'''
logic/users.py

Functions or class: UserManager

Methods:

create_user(username, password) (store hashed password).

authenticate(username, password) (check credentials).

Uses SQLite (or JSON for prototype).
'''

import hashlib
import sqlite3
import os

DB_FILE = "users.db"

class UserManager:
    @staticmethod
    def init_db():
        """Create users table if not exists"""
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            plan TEXT,
            FOREIGN KEY(username) REFERENCES users(username)
        )
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def create_user(username, password):
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users VALUES (?, ?)", (username, UserManager.hash_password(password)))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    @staticmethod
    def authenticate(username, password):
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        conn.close()
        return row and row[0] == UserManager.hash_password(password)

    @staticmethod
    def get_workouts(username):
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT plan FROM workouts WHERE username = ?", (username,))
        plans = [row[0] for row in cur.fetchall()]
        conn.close()
        return plans

    @staticmethod
    def add_workout(username, plan):
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("INSERT INTO workouts (username, plan) VALUES (?, ?)", (username, plan))
        conn.commit()
        conn.close()
