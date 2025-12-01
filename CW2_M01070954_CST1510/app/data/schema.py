def create_users_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user'
    );
    """)
    conn.commit()
    print("Users table created successfully!")


def create_cyber_incidents_table(conn):
    cursor = conn.cursor()
    
    # ❗ REMOVE THIS IN PRODUCTION — it deletes your data!
    # cursor.execute("DROP TABLE IF EXISTS cyber_incidents")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cyber_incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        incident_type TEXT,
        severity TEXT NOT NULL,
        status TEXT,
        description TEXT,
        reported_by TEXT
    );
    """)
    conn.commit()
    print("Cyber incidents table created successfully!")


def create_datasets_metadata_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS datasets_metadata (
        dataset_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        rows INTEGER,
        columns INTEGER,
        uploaded_by TEXT,
        upload_date TEXT
    );
    """)
    conn.commit()
    print("Datasets metadata table created successfully!")


def create_it_tickets_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS it_tickets (
        ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
        submitted_by TEXT NOT NULL,
        issue_type TEXT,
        priority TEXT NOT NULL,
        status TEXT,
        description TEXT,
        created_at TEXT
    );
    """)
    conn.commit()
    print("IT tickets table created successfully!")


def create_all_tables(conn):
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)
