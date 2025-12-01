import sqlite3
from pathlib import Path

# Absolute path to the database relative to this file
DB_PATH = Path(__file__).parent.parent.parent / "DATA" / "intelligence_platform.db"

def connect_database(db_path=DB_PATH):
    """
    Connect to the SQLite database.
    Creates the DATA folder and database file if they don't exist.
    """
    # Ensure the DATA folder exists
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Connect to the SQLite database (creates file if it doesn't exist)
    conn = sqlite3.connect(str(db_path))
    return conn
