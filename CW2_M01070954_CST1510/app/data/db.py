import sqlite3
from pathlib import Path
from .schema import create_all_tables


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
def initialize_tables():
    """
    Connect to the database and create all tables.
    """
    conn = connect_database()
    create_all_tables(conn)
    conn.close()

# complete databse setup

def setup_database_complete():
    """
    Complete database setup:
    1. Connect to database
    2. Create all tables
    3. Migrate users from users.txt
    4. Load CSV data for all domains
    5. Verify setup
    """
    print("\n" + "="*60)
    print("STARTING COMPLETE DATABASE SETUP")
    print("="*60)

    # Step 1: Connect
    print("\n[1/5] Connecting to database...")
    conn = connect_database()
    print("       Connected")

    # Step 2: Create tables
    print("\n[2/5] Creating database tables...")
    create_all_tables(conn)

    # Step 3: Migrate users
    print("\n[3/5] Migrating users from users.txt...")
    from app.services.user_service import migrate_users_from_file
    user_count = migrate_users_from_file(conn)
    print(f"       Migrated {user_count} users")

    # Step 4: Load CSV data
    print("\n[4/5] Loading CSV data...")
    from load_csv import load_csv_to_table
    from pathlib import Path
    csv_path = Path(r"C:\Users\ashvi\OneDrive - Middlesex University\Desktop\CW2 CST1510\CW2_M01070954_CST1510\DATA\cyber_incidents_csv.csv")
    table_name = "cyber_incidents"
    total_rows = load_csv_to_table(conn, csv_path, table_name)

    # Step 5: Verify
    print("\n[5/5] Verifying database setup...")
    cursor = conn.cursor()

    # Count rows in each table
    tables = ['users', 'cyber_incidents', 'datasets_metadata', 'it_tickets']
    print("\n Database Summary:")
    print(f"{'Table':<25} {'Row Count':<15}")
    print("-" * 40)

    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table:<25} {count:<15}")

    conn.close()

    print("\n" + "="*60)
    print(" DATABASE SETUP COMPLETE!")
    print("="*60)
    print(f"\n Database location: {DB_PATH.resolve()}")
    print("\nYou're ready for Week 9 (Streamlit web interface)!")

# Run the complete setup
setup_database_complete()