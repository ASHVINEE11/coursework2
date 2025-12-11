import pandas as pd
from app.data.db import connect_database

# CRUD operations

def insert_incident(conn, timestamp, category, severity, status, description):
    """
    Insert a new cyber incident into the database.

    Args:
        conn: Database connection
        timestamp: Incident date (YYYY-MM-DD)
        category: Type of incident
        severity: Severity level
        status: Current status
        description: Incident description
        reported_by: Username of reporter

    Returns:
        int: ID of the inserted incident
    """
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cyber_incidents
        (timestamp, category, severity, status, description)
        VALUES (?, ?, ?, ?, ?)
    """, (timestamp, category, severity, status, description))
    conn.commit()
    incident_id = cursor.lastrowid
    conn.close()
    return incident_id

def get_all_incidents():
    """Get all incidents as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents ORDER BY timestamp DESC",
        conn
    )
    conn.close()
    return df

    
    

    

def update_incident_status(conn, incident_id, new_status):
    """
    Update the status of an incident.

    TODO: Implement UPDATE operation.
    """
    # TODO: Write UPDATE SQL: UPDATE cyber_incidents SET status = ? WHERE id = ?
    # TODO: Execute and commit
    # TODO: Return cursor.rowcount
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE cyber_incidents SET status = ? WHERE id = ?",
        (new_status, incident_id)
        )
    conn.commit()
    return cursor.rowcount

def delete_incident(conn, incident_id):
    """
    Delete an incident from the database.

    TODO: Implement DELETE operation.
    """
    # TODO: Write DELETE SQL: DELETE FROM cyber_incidents WHERE id = ?
    # TODO: Execute and commit
    # TODO: Return cursor.rowcount
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM cyber_incidents WHERE id = ?",
        (incident_id)
        )
    conn.commit()
    return cursor.rowcount

# Analytical queries (The Big 6)
def get_incidents_by_type_count(conn):
    """
    Count incidents by type.
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    query = """
    SELECT category, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY category
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_high_severity_by_status(conn):
    """
    Count high severity incidents by status.
    Uses: SELECT, FROM, WHERE, GROUP BY, ORDER BY
    """
    query = """
    SELECT status, COUNT(*) as count
    FROM cyber_incidents
    WHERE severity = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_incident_types_with_many_cases(conn, min_count=5):
    """
    Find incident types with more than min_count cases.
    Uses: SELECT, FROM, GROUP BY, HAVING, ORDER BY
    """
    query = """
    SELECT category, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY category
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_count,))
    return df

# Test: Run analytical queries
if __name__ == "__main__":
    conn = connect_database()

    print("\n Incidents by Type:")
    df_by_type = get_incidents_by_type_count(conn)
    print(df_by_type)

    print("\n High Severity Incidents by Status:")
    df_high_severity = get_high_severity_by_status(conn)
    print(df_high_severity)

    print("\n Incident Types with Many Cases (>5):")
    df_many_cases = get_incident_types_with_many_cases(conn, min_count=5)
    print(df_many_cases)

    conn.close()

