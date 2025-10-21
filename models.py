from __future__ import annotations
import sqlite3
from pathlib import Path
from typing import Dict, List

DB_PATH = Path("instance/app.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS workouts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    sets INTEGER NOT NULL,
    duration_min INTEGER NOT NULL,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS exercises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    workout_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    sets INTEGER NOT NULL,
    reps INTEGER NOT NULL,
    weight REAL DEFAULT 0,
    FOREIGN KEY(workout_id) REFERENCES workouts(id) ON DELETE CASCADE
);
"""

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    with get_conn() as conn:
        conn.executescript(SCHEMA)

def user_create(username: str, password_hash: str) -> int:
    with get_conn() as conn:
        cur = conn.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        return cur.lastrowid

def user_get_by_username(username: str):
    with get_conn() as conn:
        return conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

def user_get(user_id: int):
    with get_conn() as conn:
        return conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()

def workout_create(user_id: int, name: str, sets: int, duration_min: int, notes: str | None, exercises: List[dict]) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO workouts (user_id, name, sets, duration_min, notes) VALUES (?, ?, ?, ?, ?)",
            (user_id, name, sets, duration_min, notes)
        )
        wid = cur.lastrowid
        if exercises:
            conn.executemany(
                "INSERT INTO exercises (workout_id, name, sets, reps, weight) VALUES (?, ?, ?, ?, ?)",
                [(wid, e.get("name",""), int(e.get("sets",0)), int(e.get("reps",0)), float(e.get("weight",0))) for e in exercises]
            )
        return wid

def workout_list(user_id: int):
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM workouts WHERE user_id = ? ORDER BY created_at DESC, id DESC", (user_id,)).fetchall()
        ids = [r["id"] for r in rows]
        ex_by_w = {wid: [] for wid in ids}
        if ids:
            q = f"SELECT * FROM exercises WHERE workout_id IN ({','.join(['?']*len(ids))}) ORDER BY id"
            for ex in conn.execute(q, ids).fetchall():
                ex_by_w[ex["workout_id"]].append(ex)
        result = []
        for r in rows:
            item = dict(r)
            item["exercises"] = [dict(x) for x in ex_by_w.get(r["id"], [])]
            result.append(item)
        return result

def workout_stats(user_id: int) -> Dict[str, int]:
    with get_conn() as conn:
        row = conn.execute("SELECT COUNT(*) as count, COALESCE(SUM(duration_min),0) as total_min FROM workouts WHERE user_id = ?", (user_id,)).fetchone()
        return {"count": row["count"], "total_min": row["total_min"]}

def workout_delete(user_id: int, workout_id: int) -> None:
    with get_conn() as conn:
        conn.execute("DELETE FROM workouts WHERE id = ? AND user_id = ?", (workout_id, user_id))
