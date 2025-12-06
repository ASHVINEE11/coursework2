import sqlite3
from pathlib import Path

DB_PATH = Path("DATA") / "intelligence_platform.db"

def connect_database(db_path=DB_PATH):
    return sqlite3.connect(str(db_path))

def ensure_reported_by_column():
    """Add 'reported_by' column to cyber_incidents if missing."""
    conn = connect_database()
    cursor = conn.cursor()

    # Check existing columns
    cursor.execute("PRAGMA table_info(cyber_incidents)")
    columns = [col[1] for col in cursor.fetchall()]

    if "reported_by" not in columns:
        cursor.execute("ALTER TABLE cyber_incidents ADD COLUMN reported_by TEXT")
        conn.commit()
        print("✅ 'reported_by' column added to cyber_incidents.")
    else:
        print("✅ 'reported_by' column already exists.")

    conn.close()

if __name__ == "__main__":
    ensure_reported_by_column()
