import pandas as pd
from app.data.db import connect_database

# ---------------------------------------------------------
# CRUD OPERATIONS
# ---------------------------------------------------------

def insert_dataset(conn, dataset_id, name, rows, columns, uploaded_by, upload_date):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO datasets_metadata
        (dataset_id, name, `rows`, `columns`, uploaded_by, upload_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (dataset_id, name, rows, columns, uploaded_by, upload_date))
    
    conn.commit()
    dataset_rowid = cursor.lastrowid
    conn.close()
    return dataset_rowid


def get_all_datasets():
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM datasets_metadata ORDER BY upload_date DESC",
        conn
    )
    conn.close()
    return df


def update_dataset_name(conn, dataset_id, new_name):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE datasets_metadata SET name = ? WHERE dataset_id = ?",
        (new_name, dataset_id)
    )
    conn.commit()
    return cursor.rowcount


def delete_dataset(conn, dataset_id):
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM datasets_metadata WHERE dataset_id = ?",
        (dataset_id,)
    )
    conn.commit()
    return cursor.rowcount

# ---------------------------------------------------------
# ANALYTICAL QUERIES
# ---------------------------------------------------------

def get_datasets_by_uploader(conn):
    query = """
    SELECT uploaded_by, COUNT(*) AS count
    FROM datasets_metadata
    GROUP BY uploaded_by
    ORDER BY count DESC
    """
    return pd.read_sql_query(query, conn)


def get_avg_rows_by_uploader(conn):
    query = """
    SELECT uploaded_by, AVG(`rows`) AS average_rows
    FROM datasets_metadata
    GROUP BY uploaded_by
    ORDER BY average_rows DESC
    """
    return pd.read_sql_query(query, conn)


def get_largest_datasets(conn, limit=5):
    query = f"""
    SELECT *
    FROM datasets_metadata
    ORDER BY rows DESC
    LIMIT {limit}
    """
    return pd.read_sql_query(query, conn)


# ---------------------------------------------------------
# TEST BLOCK
# ---------------------------------------------------------

if __name__ == "__main__":
    conn = connect_database()

    print("\nDatasets by uploader:")
    print(get_datasets_by_uploader(conn))

    print("\nAverage rows by uploader:")
    print(get_avg_rows_by_uploader(conn))

    print("\n5 largest datasets:")
    print(get_largest_datasets(conn))

    conn.close()