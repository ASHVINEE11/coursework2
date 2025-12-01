import sqlite3
from pathlib import Path
from app.data.schema import create_all_tables

# Path to database
DB_PATH = Path("DATA") / "intelligence_platform.db"

# Connect to database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Drop old table
cursor.execute("DROP TABLE IF EXISTS cyber_incidents")
print("Old cyber_incidents table dropped!")

# Recreate all tables (using your fixed schema.py)
create_all_tables(conn)
print("All tables recreated successfully!")

conn.close()
