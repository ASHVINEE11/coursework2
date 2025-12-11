import pandas as pd
from app.data.db import connect_database

# CRUD operations

def insert_ticket(conn, ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours):
    """
    Insert a new IT ticket into the database.

    Args:
        conn: Database connection
        ticket_id: Unique ticket identifier
        priority: Priority level (Low, Medium, High, Critical)
        description: Ticket description
        status: Current status (Open, Resolved, In progress, Waiting for User)
        assigned_to: IT support staff assigned
        created_at: Timestamp when ticket was created
        resolution_time_hours: Resolution time in hours

    Returns:
        int: ID of the inserted ticket
    """
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO it_tickets
        (ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours))
    conn.commit()
    ticket_rowid = cursor.lastrowid
    conn.close()
    return ticket_rowid

def get_all_tickets():
    """Get all IT tickets as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM it_tickets ORDER BY created_at DESC",
        conn
    )
    conn.close()
    return df

    
    

    

def update_ticket_status(conn, ticket_id, new_status):
    """
    Update the status of a ticket."""
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE it_tickets SET status = ? WHERE ticket_id = ?",
        (new_status, ticket_id)
    )
    conn.commit()
    return cursor.rowcount


def delete_ticket(conn, ticket_id):
    """
    Delete a ticket from the database. """

    
    # TODO: Write DELETE SQL: DELETE FROM cyber_incidents WHERE id = ?
    # TODO: Execute and commit
    # TODO: Return cursor.rowcount
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM it_tickets WHERE ticket_id = ?",
        (ticket_id)
        )
    conn.commit()
    return cursor.rowcount

# Analytical queries (The Big 6)
def get_tickets_by_priority(conn):
    """
    Count tickets by priority.
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    query = """
    SELECT priority, COUNT(*) as count
    FROM it_tickets
    GROUP BY priority
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_avg_resolution_by_status(conn):
    """
    Average resolution time by status."""
    query = """
    SELECT status, AVG(resolution_time_hours) as avg_resolution
    FROM it_tickets
    GROUP BY status
    ORDER BY avg_resolution DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_tickets_by_assignee(conn):
    """ count tickets assigned to each IT support staff."""
    query = """
    SELECT assigned_to, COUNT(*) as count
    FROM it_tickets
    GROUP BY assigned_to
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

# Test: Run analytical queries
if __name__ == "__main__":
    conn = connect_database()

    print("\nTickets by priority:")
    df_by_priority = get_tickets_by_priority(conn)
    print(df_by_priority)

    print("\nAverage solution time by status:")
    df_avg_resolution = get_avg_resolution_by_status(conn)
    print(df_avg_resolution)

    print("\nTickets by assignee")
    df_tickets_by_assignee = get_tickets_by_assignee(conn)
    print(df_tickets_by_assignee)

    conn.close()

