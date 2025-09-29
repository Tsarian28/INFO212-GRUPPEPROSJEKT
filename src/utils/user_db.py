import sqlite3
from utils.helpers import get_default_answers

def initialize_user_database(db_path="users.db"):
    """
    Initialize the SQLite database for storing user information.

    Args:
        db_path (str): Path to the SQLite database file.
    """
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Create a table for storing user information if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            preferences TEXT,
            history TEXT
        )
    """)
    connection.commit()
    connection.close()


def create_user(username, password, db_path="users.db"):
    """
    Create a new user profile and store it in the SQLite database.

    Args:
        username (str): The username for the new user.
        password (str): The password for the new user.
        db_path (str): Path to the SQLite database file.

    Returns:
        dict: A dictionary representing the new user profile, or None if creation failed.
    """
    # Default preferences and history
    preferences = get_default_answers()
    history = []

    # Serialize preferences and history as strings for storage
    preferences_str = str(preferences)
    history_str = str(history)

    # Insert the new user into the database
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (username, password, preferences, history)
            VALUES (?, ?, ?, ?)
        """, (username, password, preferences_str, history_str))
        connection.commit()
    except sqlite3.IntegrityError:
        print(f"Error: Username '{username}' already exists.")
        return None
    finally:
        connection.close()

    # Return the created user profile as a dictionary
    return {
        "username": username,
        "preferences": preferences,
        "history": history
    }


def get_user(username, db_path="users.db"):
    """
    Retrieve a user profile from the SQLite database.

    Args:
        username (str): The username of the user to retrieve.
        db_path (str): Path to the SQLite database file.

    Returns:
        dict: A dictionary representing the user profile, or None if the user does not exist.
    """
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT username, preferences, history
        FROM users
        WHERE username = ?
    """, (username,))
    row = cursor.fetchone()
    connection.close()

    if row:
        return {
            "username": row[0],
            "preferences": eval(row[1]),  # Deserialize preferences
            "history": eval(row[2])  # Deserialize history
        }
    else:
        print(f"Error: User '{username}' not found.")
        return None