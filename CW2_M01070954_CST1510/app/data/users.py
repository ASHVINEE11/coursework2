from app.data.db import connect_database
import sqlite3

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

# ===== Test block =====
if __name__ == "__main__":
    print("Testing user functions...")
    
    username = "testuser"
    password_hash = "hashedpassword123"

    # Safe insert
    insert_user(username, password_hash)

    # Fetch and display user
    user = get_user_by_username(username)
    print("User fetched:", user)

