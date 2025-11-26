def create_users_table(conn):
    """Create users table."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    """)
    conn.commit()
    print("well done! You have been able to create user table")

def create_cyber_incident_table(conn):
    
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users cyber_incidents (
            incident_id INTEGER PRIMARY KEY AUTOINCREMENT,
            severity TEXT NOT NULL,
            category TEXT
            status TEXT
            description TEXT
            reported by: TEXT (username of reporter),
            date: TEXT (format: YYYY-MM-DD))""")
            
    conn.commit()
    print("well done! cyber_incidents table has been created succesfully!")


 def create_datasets_metadata_table(conn):
    
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users datasets_metadata (
            datasets_metadata_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            rows INTEGER
            column INTEGER
            uploaded_by TEXT
            upload_Date DATE)""")
            
    conn.commit()
    print("well done! datasets_metadate table has been created succesfully!")

def create_it_tickets_table(conn):
    
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users it_tickets (
            datasets_metadata_id INTEGER PRIMARY KEY AUTOINCREMENT,
            priority TEXT NOT NULL,
            rows INTEGER
            column INTEGER
            uploaded_by TEXT
            upload_Date DATE)""")
            
    conn.commit()
    print("well done! datasets_metadate table has been created succesfully!")






    
    
