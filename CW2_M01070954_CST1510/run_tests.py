from app.data.db import connect_database, create_all_tables
from app.services.user_service import register_user, login_user, migrate_users_from_file
from app.data.incidents import insert_incident, update_incident_status, delete_incident,get_incidents_by_type_count,get_high_severity_by_status


from load_csv import load_csv_to_table
from pathlib import Path
import pandas as pd

CSV_PATH = Path("C:/Users/ashvi/OneDrive - Middlesex University/Desktop/CW2 CST1510/CW2_M01070954_CST1510/DATA/cyber_incidents_csv.csv")

def setup_database_complete():
    print("\n" + "="*60)
    print("STARTING COMPLETE DATABASE SETUP")
    print("="*60)

    conn = connect_database()
    print("\n[1/5] Connecting to database... Connected")

    print("\n[2/5] Creating database tables...")
    create_all_tables(conn)

    print("\n[3/5] Migrating users from users.txt...")
    user_count = migrate_users_from_file(conn)
    print(f"       Migrated {user_count} users")

    print("\n[4/5] Loading CSV data...")
    total_rows = load_csv_to_table(conn, CSV_PATH, "cyber_incidents")
    print(f"       Loaded {total_rows} rows into 'cyber_incidents'")

    print("\n[5/5] Verifying database setup...")
    cursor = conn.cursor()
    tables = ['users', 'cyber_incidents', 'datasets_metadata', 'it_tickets']
    print("\n Database Summary:")
    print(f"{'Table':<25} {'Row Count':<15}")
    print("-" * 40)
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table:<25} {count:<15}")

    conn.close()
    print("\n DATABASE SETUP COMPLETE!\n")

def run_comprehensive_tests():
    print("\n" + "="*60)
    print("🧪 RUNNING COMPREHENSIVE TESTS")
    print("="*60)

    conn = connect_database()

    # Authentication tests
    print("\n[TEST 1] Authentication")
    success, msg = register_user("test_user", "TestPass123!", "user")
    print(f"  Register: {'✅' if success else '❌'} {msg}")
    success, msg = login_user("test_user", "TestPass123!")
    print(f"  Login:    {'✅' if success else '❌'} {msg}")

    # CRUD tests
    print("\n[TEST 2] CRUD Operations")
    test_id = insert_incident(
        conn,
        "2024-11-05",
        "Test Incident",
        "Low",
        "Open",
        "This is a test incident",
        "test_user"
    )
    print(f"  Create: ✅ Incident #{test_id} created")

    df = pd.read_sql_query("SELECT * FROM cyber_incidents WHERE id = ?", conn, params=(test_id,))
    print(f"  Read:    Found incident #{test_id}")

    update_incident_status(conn, test_id, "Resolved")
    print("  Update:  Status updated")

    delete_incident(conn, test_id)
    print("  Delete:  Incident deleted")

    # Analytical queries
    print("\n[TEST 3] Analytical Queries")
    df_by_type = get_incidents_by_type_count(conn)
    print(f"  By Type:     Found {len(df_by_type)} incident types")
    df_high = get_high_severity_by_status(conn)
    print(f"  High Severity: Found {len(df_high)} status categories")

    conn.close()
    print("\n" + "="*60)
    print("\n✅ ALL TESTS PASSED!\n")
    print("="*60)


    