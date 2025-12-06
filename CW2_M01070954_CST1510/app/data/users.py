from app.data.db import connect_database
import sqlite3
from app.data.schema import create_users_table
from pathlib import Path
DATA_DIR = Path("C:/Users/ashvi/OneDrive - Middlesex University/Desktop/CW2 CST1510")



def get_user_by_username(username):
    """Retrieve user by username."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def insert_user(username, password_hash, role='user'):
    """Insert new user safely, avoiding duplicates."""
    try:
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, role)
        )
        conn.commit()
        print(f"User '{username}' inserted successfully.")
    except sqlite3.IntegrityError:
        print(f"User '{username}' already exists, skipping insert.")
    finally:
        conn.close()

